/**
 * Module: On-page Keyword Research
 * Nghiên cứu từ khóa phụ cho 1 page cụ thể thông qua GSC, Google Suggest và LSI Competitor Analysis.
 */
const axios = require('axios');
const { getSearchConsoleClient } = require('../core/auth');
const { fetchPage } = require('../core/crawler');
const { extractDomain, getDateRange } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, shortUrl } = require('../core/reporter');

// Basic Vietnamese stop words for N-gram filtering
const VI_STOP_WORDS = new Set(['và', 'là', 'của', 'thì', 'mà', 'có', 'trong', 'với', 'cho', 'các', 'những', 'để', 'một', 'như', 'tại', 'đến', 'ở', 'được', 'người', 'khi', 'trên', 'đã', 'này', 'về', 'sẽ', 'từ', 'rằng', 'bằng', 'ra', 'nào', 'cũng', 'phải', 'theo', 'nhất', 'lại', 'nhiều', 'làm', 'hay', 'nhưng', 'còn', 'đang', 'đó', 'chỉ', 'sau', 'hơn', 'anh', 'em', 'chị', 'bạn', 'mình', 'tôi', 'rất', 'vào', 'bị', 'nên', 'cách', 'việc', 'đi', 'lên', 'xuống', 'thể']);

function tokenize(text) {
    return text.toLowerCase().replace(/[^\w\s\u00C0-\u024F\u1E00-\u1EFF]/g, ' ').split(/\s+/).filter(w => w.length > 1 && !VI_STOP_WORDS.has(w));
}

function getNgrams(tokens, n) {
    const ngrams = [];
    for (let i = 0; i < tokens.length - n + 1; i++) {
        ngrams.push(tokens.slice(i, i + n).join(' '));
    }
    return ngrams;
}

async function run(config) {
    const { siteUrl, targetUrl: url, keyword, days, cseApiKey, cseEngineId, serperApiKey, userAgent } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');
    if (!url) throw new Error('[CRITICAL] --url (Target Page) là bắt buộc cho onpage-research.');
    if (!keyword) throw new Error('[CRITICAL] --keyword (Main Keyword) là bắt buộc cho onpage-research.');

    printHeader('On-page Keyword Research', config);
    const domain = extractDomain(siteUrl);
    const dateRange = getDateRange(days || 30);
    const startDate = dateRange.startDate;
    const endDate = dateRange.endDate;

    const reportData = {
        meta: { siteUrl, targetUrl: url, mainKeyword: keyword, startDate, endDate, generatedAt: new Date().toISOString() },
        gscKeywords: [],
        suggestKeywords: [],
        lsiKeywords: [],
        competitorTopics: []
    };

    // ---------------------------------------------------------
    // Phase 1: GSC Striking Distance
    // ---------------------------------------------------------
    console.log('\n  [Phase 1] Fetching Striking Distance keywords from GSC...');
    try {
        const { searchconsole } = await getSearchConsoleClient();
        const gscRes = await searchconsole.searchanalytics.query({
            siteUrl,
            requestBody: { 
                startDate, 
                endDate, 
                dimensions: ['query'], 
                dimensionFilterGroups: [{
                    filters: [{ dimension: 'page', operator: 'equals', expression: url }]
                }],
                rowLimit: 2000 
            }
        });

        const rows = (gscRes.data.rows || []).map(r => ({
            query: r.keys[0],
            clicks: r.clicks,
            impressions: r.impressions,
            position: r.position
        }));

        // Filter: only keep if position > 3 (striking distance), sort by impressions
        reportData.gscKeywords = rows
            .filter(r => r.position > 3 && r.impressions >= 5)
            .sort((a, b) => b.impressions - a.impressions)
            .slice(0, 50); // top 50 striking distance

        console.log(`  → Found ${reportData.gscKeywords.length} striking distance keywords.`);
    } catch (e) {
        console.error(`  [ERROR] GSC Fetch Failed: ${e.message}`);
    }

    // ---------------------------------------------------------
    // Phase 2: Google Suggest (Long-tail)
    // ---------------------------------------------------------
    console.log('\n  [Phase 2] Fetching Google Autocomplete (Long-tail)...');
    try {
        const suggestUrl = `http://suggestqueries.google.com/complete/search?client=chrome&q=${encodeURIComponent(keyword)}&hl=vi&gl=vn`;
        const res = await axios.get(suggestUrl, { timeout: 10000 });
        if (res.data && res.data[1]) {
            reportData.suggestKeywords = res.data[1].filter(k => k !== keyword);
        }
        console.log(`  → Found ${reportData.suggestKeywords.length} suggest keywords.`);
    } catch (e) {
        console.error(`  [ERROR] Google Suggest Failed: ${e.message}`);
    }

    // ---------------------------------------------------------
    // Phase 3: Competitor Semantic Analysis (LSI)
    // ---------------------------------------------------------
    console.log('\n  [Phase 3] Analyzing Competitors for LSI/Semantic Keywords...');
    let serpResults = [];

    if (serperApiKey) {
        try {
            const serperRes = await axios.post('https://google.serper.dev/search', { q: keyword, num: 10 }, {
                headers: { 'X-API-KEY': serperApiKey, 'Content-Type': 'application/json' }, timeout: 15000
            });
            if (serperRes.data && serperRes.data.organic) {
                serpResults = serperRes.data.organic.map(item => ({ title: item.title, link: item.link }));
            }
        } catch (e) { console.log(`  [WARN] Serper API failed: ${e.message}`); }
    }

    if (serpResults.length === 0 && cseApiKey && cseEngineId) {
        try {
            const searchRes = await axios.get('https://www.googleapis.com/customsearch/v1', {
                params: { key: cseApiKey, cx: cseEngineId, q: keyword, num: 10 }, timeout: 15000
            });
            serpResults = (searchRes.data.items || []).map(item => ({ title: item.title, link: item.link }));
        } catch (e) { console.error(`  [ERROR] CSE failed: ${e.message}`); }
    }

    // Filter out our own domain
    serpResults = serpResults.filter(item => {
        try { return !new URL(item.link).hostname.includes(domain); } catch { return true; }
    }).slice(0, 10);

    if (serpResults.length > 0) {
        const ngramCounts = {};
        const allH2s = [];

        console.log(`  → Crawling ${serpResults.length} competitors...`);
        for (let i = 0; i < serpResults.length; i++) {
            const comp = serpResults[i];
            process.stdout.write(`\r    Crawling ${i+1}/${serpResults.length}: ${shortUrl(comp.link, comp.link)}`);
            try {
                const { $ } = await fetchPage(comp.link, { userAgent, timeout: 10000 });
                let compText = '';
                $('h2, h3, strong, b').each((_, el) => {
                    const text = $(el).text().trim();
                    if (text) {
                        compText += ' ' + text;
                        if (el.tagName.toLowerCase() === 'h2') {
                            allH2s.push({ topic: text, domain: new URL(comp.link).hostname });
                        }
                    }
                });
                
                const tokens = tokenize(compText);
                const n2 = getNgrams(tokens, 2);
                const n3 = getNgrams(tokens, 3);
                
                // Tránh count lặp trên cùng 1 trang (chỉ tính 1 lần / 1 trang nếu xuất hiện)
                const uniqueNgrams = new Set([...n2, ...n3]);
                uniqueNgrams.forEach(ng => {
                    ngramCounts[ng] = (ngramCounts[ng] || 0) + 1;
                });
            } catch (e) {
                // Ignore crawl errors
            }
        }
        console.log();

        // Lọc những cụm xuất hiện >= 3 đối thủ (hoặc >= 2 nếu ít kết quả)
        const minFrequency = Math.max(2, Math.floor(serpResults.length / 3));
        reportData.lsiKeywords = Object.keys(ngramCounts)
            .filter(ng => ngramCounts[ng] >= minFrequency)
            .sort((a, b) => ngramCounts[b] - ngramCounts[a])
            .map(ng => ({ keyword: ng, frequency: ngramCounts[ng] }))
            .slice(0, 30); // Lấy top 30 LSI

        // Lấy ngẫu nhiên vài H2 để tham khảo
        reportData.competitorTopics = allH2s.slice(0, 15);
    } else {
        console.log('  [WARN] Không lấy được SERP results (Thiếu SERPER_API_KEY hoặc GOOGLE_CSE). Bỏ qua Phase 3.');
    }

    // ---------------------------------------------------------
    // Output Report
    // ---------------------------------------------------------
    console.log('\n  [Phase 4] Generating Report...');
    const files = getReportFilename('onpage-research', domain);
    await saveJsonReport(files.json, reportData);

    let md = `# 🎯 On-page Keyword Research\n\n`;
    md += `- **Site**: ${siteUrl}\n`;
    md += `- **Target URL**: [${url}](${url})\n`;
    md += `- **Main Keyword**: \`${keyword}\`\n`;
    md += `- **Period**: ${startDate} → ${endDate}\n\n`;

    md += `## 1. Google Suggest (Mọi người cũng tìm kiếm)\n`;
    md += `> Các từ khóa mở rộng (Long-tail) do Google Autocomplete gợi ý, rất tốt để làm FAQ hoặc mở rộng ý.\n\n`;
    if (reportData.suggestKeywords.length > 0) {
        reportData.suggestKeywords.forEach(k => {
            md += `- ${k}\n`;
        });
    } else {
        md += `*Không có dữ liệu suggest.*\n`;
    }
    md += '\n';

    md += `## 2. GSC Striking Distance Keywords\n`;
    md += `> Các từ khóa đã có Impressions nhưng chưa vào Top 3. Cần rải thêm vào H2/H3 hoặc Image Alt để push rank.\n\n`;
    if (reportData.gscKeywords.length > 0) {
        md += `| Keyword | Position | Impressions | Clicks |\n| :--- | :---: | :---: | :---: |\n`;
        reportData.gscKeywords.forEach(r => {
            md += `| ${r.query} | ${r.position.toFixed(1)} | ${r.impressions} | ${r.clicks} |\n`;
        });
    } else {
        md += `*Không tìm thấy Striking Distance keyword nào cho URL này trong ${days || 30} ngày qua.*\n`;
    }
    md += '\n';

    md += `## 3. LSI / Semantic Keywords từ Đối thủ (Content Gap)\n`;
    md += `> Các cụm từ xuất hiện lặp lại nhiều lần ở các thẻ H2, H3, Strong của Top 10 đối thủ (Tần suất tính theo số trang đề cập).\n\n`;
    if (reportData.lsiKeywords.length > 0) {
        md += `| LSI Keyword (N-gram) | Tần suất xuất hiện (Số đối thủ) |\n| :--- | :---: |\n`;
        reportData.lsiKeywords.forEach(l => {
            md += `| ${l.keyword} | ${l.frequency} |\n`;
        });
    } else {
        md += `*Không phân tích được LSI (Có thể thiếu API Key SERP hoặc lỗi cào dữ liệu).*\n`;
    }
    md += '\n';

    md += `## 4. Tham khảo H2 Đối thủ\n\n`;
    if (reportData.competitorTopics.length > 0) {
        reportData.competitorTopics.forEach(t => {
            md += `- **${t.topic}** *(từ ${t.domain})*\n`;
        });
    } else {
        md += `*Không có dữ liệu H2.*\n`;
    }

    await saveMarkdownReport(files.md, md);
    console.log(`  ✅ Báo cáo lưu tại: ${files.md}`);

    return reportData;
}

module.exports = { run };
