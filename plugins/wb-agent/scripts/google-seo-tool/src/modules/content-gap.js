/**
 * Module: Competitor Content Gap Analysis
 * So sánh content mình vs top SERP results → Tìm chủ đề đối thủ có mà mình thiếu
 */
const axios = require('axios');
const { getSearchConsoleClient } = require('../core/auth');
const { fetchPage } = require('../core/crawler');
const { extractDomain, getDateRange } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, fmtPos, shortUrl } = require('../core/reporter');

async function run(config) {
    const { siteUrl, days, rowLimit, cseApiKey, cseEngineId, serperApiKey, strikingMin, strikingMax, userAgent } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');
    if (!serperApiKey && (!cseApiKey || !cseEngineId)) {
        throw new Error('[CRITICAL] Cần SERPER_API_KEY hoặc bộ đôi GOOGLE_CSE_API_KEY & GOOGLE_CSE_ENGINE_ID để phân tích SERP.');
    }

    printHeader('Competitor Content Gap Analysis', config);
    const domain = extractDomain(siteUrl);

    let targetKeywords = [];
    let startDate = '';
    let endDate = '';

    if (config.keyword) {
        console.log(`  [INFO] Chạy phân tích Content Gap trực tiếp cho từ khóa: "${config.keyword}"`);
        targetKeywords = [{
            query: config.keyword,
            page: config.targetUrl || siteUrl,
            clicks: 0,
            impressions: 100,
            position: 10
        }];
        const today = new Date();
        endDate = today.toISOString().split('T')[0];
        startDate = new Date(today.getTime() - days * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    } else {
        // Step 1: Lấy Striking Distance keywords từ GSC
        console.log('  Step 1: Fetching striking distance keywords from GSC...');
        const { searchconsole } = await getSearchConsoleClient();
        const dateRange = getDateRange(days);
        startDate = dateRange.startDate;
        endDate = dateRange.endDate;

        const gscRes = await searchconsole.searchanalytics.query({
            siteUrl,
            requestBody: { startDate, endDate, dimensions: ['query', 'page'], rowLimit }
        });

        const rows = (gscRes.data.rows || []).map(r => ({
            query: r.keys[0], page: r.keys[1],
            clicks: r.clicks, impressions: r.impressions, position: r.position
        }));

        // Lấy top keywords (striking distance + high impression)
        let minImpressions = config.minImpressions || 50;
        targetKeywords = rows
            .filter(r => r.position >= strikingMin && r.position <= strikingMax && r.impressions >= minImpressions)
            .sort((a, b) => b.impressions - a.impressions)
            .slice(0, 10); // Top 10 keywords to analyze

        if (targetKeywords.length === 0 && rows.length > 0) {
            console.log(`  [INFO] Không tìm thấy từ khóa với impressions >= ${minImpressions}. Thử hạ xuống impressions >= 5...`);
            minImpressions = 5;
            targetKeywords = rows
                .filter(r => r.position >= strikingMin && r.position <= strikingMax && r.impressions >= minImpressions)
                .sort((a, b) => b.impressions - a.impressions)
                .slice(0, 10);
        }
    }

    console.log(`  → ${targetKeywords.length} keywords selected for gap analysis`);

    if (targetKeywords.length === 0) {
        console.log('  No striking distance keywords found. Try adjusting --striking-min/max or --min-impressions');
        return { gaps: [] };
    }

    // Step 2: Cho mỗi keyword, search Google CSE → crawl top 3 results → compare content
    console.log('\n  Step 2: Analyzing SERPs and competitor content...\n');
    const gaps = [];

    for (let i = 0; i < targetKeywords.length; i++) {
        const kw = targetKeywords[i];
        process.stdout.write(`\r  Analyzing: ${i + 1}/${targetKeywords.length} — "${kw.query}"`);

        try {
            let serpResults = [];

            // Try Serper.dev first if key is available
            if (serperApiKey) {
                try {
                    const serperRes = await axios.post('https://google.serper.dev/search', {
                        q: kw.query,
                        num: 5
                    }, {
                        headers: {
                            'X-API-KEY': serperApiKey,
                            'Content-Type': 'application/json'
                        },
                        timeout: 15000
                    });
                    if (serperRes.data && serperRes.data.organic) {
                        serpResults = serperRes.data.organic.map(item => ({ title: item.title, link: item.link }));
                    }
                } catch (e) {
                    console.log(`\n  [WARNING] Serper.dev API failed: ${e.message}. Trying Google Custom Search...`);
                }
            }

            // Fallback to Google Custom Search JSON API
            if (serpResults.length === 0 && cseApiKey && cseEngineId) {
                try {
                    const searchRes = await axios.get('https://www.googleapis.com/customsearch/v1', {
                        params: { key: cseApiKey, cx: cseEngineId, q: kw.query, num: 5 },
                        timeout: 15000
                    });
                    serpResults = (searchRes.data.items || []).map(item => ({ title: item.title, link: item.link }));
                } catch (e) {
                    console.error(`\n  [ERROR] Google Custom Search failed: ${e.message}`);
                }
            }

            serpResults = serpResults
                .filter(item => {
                    try { return !new URL(item.link).hostname.includes(extractDomain(siteUrl)); } catch { return true; }
                })
                .slice(0, 3);

            // Crawl competitor pages
            const competitorAnalysis = [];
            for (const result of serpResults) {
                try {
                    const { $ } = await fetchPage(result.link, { userAgent, timeout: 10000 });
                    const h1 = $('h1').first().text().trim();
                    const h2s = [];
                    $('h2').each((_, el) => h2s.push($(el).text().trim()));
                    const bodyText = $('body').text().replace(/\s+/g, ' ').trim();
                    const wordCount = bodyText.split(/\s+/).length;

                    competitorAnalysis.push({
                        url: result.link,
                        title: result.title,
                        h1,
                        h2s: h2s.slice(0, 10),
                        wordCount,
                        domain: (() => { try { return new URL(result.link).hostname; } catch { return '-'; } })()
                    });
                } catch {}
            }

            // Crawl our own page
            let ourAnalysis = null;
            try {
                const { $ } = await fetchPage(kw.page, { userAgent, timeout: 10000 });
                const h2s = [];
                $('h2').each((_, el) => h2s.push($(el).text().trim()));
                const bodyText = $('body').text().replace(/\s+/g, ' ').trim();
                ourAnalysis = {
                    url: kw.page,
                    h1: $('h1').first().text().trim(),
                    h2s: h2s.slice(0, 10),
                    wordCount: bodyText.split(/\s+/).length
                };
            } catch {}

            // Find gaps: H2 topics competitors have but we don't
            const ourH2Set = new Set((ourAnalysis?.h2s || []).map(h => h.toLowerCase()));
            const competitorTopics = [];
            competitorAnalysis.forEach(comp => {
                comp.h2s.forEach(h2 => {
                    if (!ourH2Set.has(h2.toLowerCase())) {
                        competitorTopics.push({ topic: h2, source: comp.domain });
                    }
                });
            });

            // Avg competitor word count vs ours
            const avgCompWordCount = competitorAnalysis.length > 0
                ? Math.round(competitorAnalysis.reduce((s, c) => s + c.wordCount, 0) / competitorAnalysis.length)
                : 0;

            gaps.push({
                keyword: kw.query,
                ourPosition: kw.position,
                ourImpressions: kw.impressions,
                ourPage: kw.page,
                ourWordCount: ourAnalysis?.wordCount || 0,
                avgCompWordCount,
                wordCountGap: avgCompWordCount - (ourAnalysis?.wordCount || 0),
                missingTopics: competitorTopics.slice(0, 8),
                competitors: competitorAnalysis.map(c => ({ domain: c.domain, wordCount: c.wordCount, url: c.url }))
            });

            await new Promise(r => setTimeout(r, 1000)); // CSE rate limit
        } catch (e) {
            console.error(`\n  Error analyzing "${kw.query}": ${e.message}`);
        }
    }
    console.log('\n');

    console.log(`  → Analyzed ${gaps.length} keywords`);

    const files = getReportFilename('content-gap', domain);
    const reportData = {
        meta: { siteUrl, keywordsAnalyzed: gaps.length, generatedAt: new Date().toISOString() },
        gaps
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 📊 Competitor Content Gap Analysis — ${domain}\n\n`;
    md += `- **Keywords analyzed**: ${gaps.length}\n`;
    md += `- **Period**: ${startDate} → ${endDate}\n\n`;

    gaps.forEach((gap, idx) => {
        md += `## ${idx + 1}. Keyword: \`${gap.keyword}\`\n\n`;
        md += `| Metric | Your Page | Avg Competitors |\n| :--- | :---: | :---: |\n`;
        md += `| Position | ${gap.ourPosition.toFixed(1)} | Top 3 |\n`;
        md += `| Word Count | ${gap.ourWordCount} | ${gap.avgCompWordCount} |\n`;
        md += `| Word Gap | ${gap.wordCountGap > 0 ? `🔴 -${gap.wordCountGap} words` : `🟢 +${Math.abs(gap.wordCountGap)} words`} | - |\n`;
        md += `| Page | [${shortUrl(gap.ourPage, siteUrl)}](${gap.ourPage}) | - |\n\n`;

        if (gap.missingTopics.length > 0) {
            md += `**Missing Topics (H2s đối thủ có mà bạn thiếu):**\n\n`;
            gap.missingTopics.forEach(t => {
                md += `- "${t.topic}" *(from ${t.source})*\n`;
            });
            md += '\n';
        }
    });

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
