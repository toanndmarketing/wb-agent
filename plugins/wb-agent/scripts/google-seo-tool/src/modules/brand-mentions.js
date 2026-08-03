/**
 * Module: Brand Mention Monitor
 * Tìm trang web nhắc đến brand nhưng KHÔNG link về mình → Cơ hội xin backlink
 * Sử dụng Google Custom Search JSON API (100 queries/ngày miễn phí)
 */
const axios = require('axios');
const { fetchPage, extractLinks } = require('../core/crawler');
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, shortUrl } = require('../core/reporter');

/**
 * Google Custom Search API
 */
async function googleSearch(query, apiKey, engineId, start = 1) {
    const url = `https://www.googleapis.com/customsearch/v1`;
    const res = await axios.get(url, {
        params: { key: apiKey, cx: engineId, q: query, start, num: 10 },
        timeout: 15000
    });
    return (res.data.items || []).map(item => ({
        title: item.title,
        link: item.link,
        snippet: item.snippet || ''
    }));
}

async function run(config) {
    const { siteUrl, brand, cseApiKey, cseEngineId, crawlConcurrency, crawlDelay, userAgent } = config;
    if (!brand) throw new Error('[CRITICAL] --brand hoặc BRAND_NAME là bắt buộc. Ví dụ: --brand "ketsatgiadinh"');
    if (!cseApiKey || !cseEngineId) {
        throw new Error('[CRITICAL] Cần GOOGLE_CSE_API_KEY và GOOGLE_CSE_ENGINE_ID. Tạo miễn phí tại https://programmablesearchengine.google.com/');
    }

    printHeader('Brand Mention Monitor', config);
    const domain = extractDomain(siteUrl);
    const ownDomain = domain;

    // Build search queries
    const queries = [
        `"${brand}" -site:${ownDomain}`,
        `"${brand}" review -site:${ownDomain}`,
        `"${brand}" đánh giá -site:${ownDomain}`
    ];

    console.log(`  Brand: "${brand}"`);
    console.log(`  Own domain: ${ownDomain}`);
    console.log(`  Searching ${queries.length} queries...\n`);

    // Search all queries
    const allResults = [];
    for (const query of queries) {
        try {
            console.log(`  🔍 Query: ${query}`);
            const results = await googleSearch(query, cseApiKey, cseEngineId);
            allResults.push(...results);
            console.log(`     → ${results.length} results`);
            await new Promise(r => setTimeout(r, 500)); // Rate limit
        } catch (e) {
            console.error(`     → Error: ${e.message}`);
        }
    }

    // Deduplicate by URL
    const uniqueResults = [];
    const seen = new Set();
    allResults.forEach(r => {
        if (!seen.has(r.link)) {
            seen.add(r.link);
            uniqueResults.push(r);
        }
    });

    console.log(`\n  → ${uniqueResults.length} unique pages mention "${brand}"`);

    // Check each page for existing backlinks to our site
    console.log('  Checking for existing backlinks...\n');
    const mentions = [];

    for (let i = 0; i < uniqueResults.length; i++) {
        const result = uniqueResults[i];
        process.stdout.write(`\r  Analyzing: ${i + 1}/${uniqueResults.length}`);

        try {
            const { $ } = await fetchPage(result.link, { userAgent, timeout: 10000 });
            const { external } = extractLinks($, result.link);

            const linksToUs = external.filter(l => {
                try {
                    return new URL(l.href).hostname.includes(ownDomain);
                } catch { return false; }
            });

            mentions.push({
                url: result.link,
                title: result.title,
                snippet: result.snippet,
                hasBacklink: linksToUs.length > 0,
                backlinkCount: linksToUs.length,
                mentionDomain: (() => { try { return new URL(result.link).hostname; } catch { return '-'; } })()
            });

            await new Promise(r => setTimeout(r, crawlDelay));
        } catch (e) {
            mentions.push({
                url: result.link,
                title: result.title,
                snippet: result.snippet,
                hasBacklink: null,
                backlinkCount: 0,
                mentionDomain: (() => { try { return new URL(result.link).hostname; } catch { return '-'; } })(),
                error: e.message
            });
        }
    }
    console.log('\n');

    const unlinkedMentions = mentions.filter(m => m.hasBacklink === false);
    const linkedMentions = mentions.filter(m => m.hasBacklink === true);
    const errorMentions = mentions.filter(m => m.hasBacklink === null);

    console.log(`  ✅ Already linked: ${linkedMentions.length}`);
    console.log(`  🎯 Unlinked mentions (opportunities!): ${unlinkedMentions.length}`);
    console.log(`  ⚠️ Could not check: ${errorMentions.length}`);

    const files = getReportFilename('brand-mentions', domain);
    const reportData = {
        meta: { brand, siteUrl, queriesUsed: queries.length, totalMentions: mentions.length, generatedAt: new Date().toISOString() },
        summary: { unlinked: unlinkedMentions.length, linked: linkedMentions.length, errors: errorMentions.length },
        unlinkedMentions,
        linkedMentions
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🔍 Brand Mention Monitor — "${brand}"\n\n`;
    md += `- **Brand searched**: "${brand}"\n`;
    md += `- **Own domain**: ${ownDomain}\n`;
    md += `- **Total mentions found**: ${mentions.length}\n`;
    md += `- **🎯 Unlinked mentions**: **${unlinkedMentions.length}** (outreach opportunities!)\n`;
    md += `- **✅ Already linked**: ${linkedMentions.length}\n\n`;

    if (unlinkedMentions.length > 0) {
        md += `## 🎯 Unlinked Mentions — Gửi Outreach Xin Backlink\n\n`;
        md += `> Các trang này nhắc đến "${brand}" nhưng CHƯA link về ${ownDomain}. Đây là cơ hội backlink tốt nhất!\n\n`;
        md += mdTable(
            ['Domain', 'Page Title', 'Snippet'],
            ['mentionDomain', 'title', 'snippet'],
            unlinkedMentions.map(m => ({
                ...m,
                title: `[${m.title.substring(0, 60)}](${m.url})`,
                snippet: m.snippet.substring(0, 100) + '...'
            }))
        );
        md += '\n';
    }

    if (linkedMentions.length > 0) {
        md += `## ✅ Already Linked Mentions\n\n`;
        md += mdTable(
            ['Domain', 'Page Title', 'Backlinks'],
            ['mentionDomain', 'title', 'backlinkCount'],
            linkedMentions.map(m => ({ ...m, title: `[${m.title.substring(0, 60)}](${m.url})` }))
        );
    }

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
