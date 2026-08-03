/**
 * Module: Broken Link Building Scanner
 * Quét trang ngoài tìm broken links → Đề xuất thay thế bằng content của mình
 */
const { fetchPage, headCheck, extractLinks, batchProcess } = require('../core/crawler');
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, shortUrl } = require('../core/reporter');
const axios = require('axios');

async function run(config) {
    const { siteUrl, targetUrls, cseApiKey, cseEngineId, crawlConcurrency, crawlDelay, userAgent } = config;
    const niche = config._args?.niche || config.brand || '';

    printHeader('Broken Link Building Scanner', config);
    const domain = extractDomain(siteUrl);

    let prospectUrls = [...targetUrls];

    // Nếu không có target URLs, tìm resource pages qua Google CSE
    if (prospectUrls.length === 0 && cseApiKey && cseEngineId && niche) {
        console.log(`  No target URLs provided. Searching resource pages for niche: "${niche}"...`);
        const searchQueries = [
            `${niche} resources links`,
            `${niche} useful links recommended`,
            `${niche} "resource page"`
        ];

        for (const query of searchQueries) {
            try {
                const res = await axios.get('https://www.googleapis.com/customsearch/v1', {
                    params: { key: cseApiKey, cx: cseEngineId, q: query, num: 10 },
                    timeout: 15000
                });
                (res.data.items || []).forEach(item => {
                    if (!prospectUrls.includes(item.link)) prospectUrls.push(item.link);
                });
                await new Promise(r => setTimeout(r, 500));
            } catch (e) {
                console.error(`  Search error: ${e.message}`);
            }
        }
        console.log(`  → Found ${prospectUrls.length} prospect pages`);
    }

    if (prospectUrls.length === 0) {
        console.log('[WARNING] Cần cung cấp --target-urls hoặc --niche + Google CSE credentials');
        console.log('  Ví dụ: node cli.js broken-links --target-urls "https://example.com/resources,https://example2.com/links"');
        console.log('  Hoặc:  node cli.js broken-links --niche "két sắt" --cse-key KEY --cse-id ID');
        return { opportunities: [] };
    }

    // Crawl prospect pages → extract all outbound links → check for broken ones
    console.log(`\n  Step 1: Crawling ${prospectUrls.length} prospect pages...\n`);
    const allOpportunities = [];

    for (let i = 0; i < prospectUrls.length; i++) {
        const prospectUrl = prospectUrls[i];
        process.stdout.write(`\r  Scanning: ${i + 1}/${prospectUrls.length} — ${shortUrl(prospectUrl)}`);

        try {
            const { $ } = await fetchPage(prospectUrl, { userAgent });
            const { external } = extractLinks($, prospectUrl);

            // Check each external link
            const brokenOnPage = [];
            for (const link of external.slice(0, 30)) { // Limit per page to avoid overload
                try {
                    const { statusCode } = await headCheck(link.href, { timeout: 8000 });
                    if (statusCode === 404 || statusCode === 410 || statusCode === 0) {
                        brokenOnPage.push({
                            brokenUrl: link.href,
                            anchorText: link.text,
                            statusCode
                        });
                    }
                } catch {}
                await new Promise(r => setTimeout(r, 100));
            }

            if (brokenOnPage.length > 0) {
                allOpportunities.push({
                    prospectPage: prospectUrl,
                    prospectDomain: (() => { try { return new URL(prospectUrl).hostname; } catch { return '-'; } })(),
                    totalLinks: external.length,
                    brokenLinks: brokenOnPage
                });
            }
        } catch (e) {
            // Skip pages that can't be fetched
        }

        await new Promise(r => setTimeout(r, crawlDelay));
    }
    console.log('\n');

    const totalBroken = allOpportunities.reduce((s, o) => s + o.brokenLinks.length, 0);
    console.log(`  🎯 Found ${totalBroken} broken links across ${allOpportunities.length} pages`);

    const files = getReportFilename('broken-link-build', domain);
    const reportData = {
        meta: { siteUrl, prospectsScanned: prospectUrls.length, pagesWithBrokenLinks: allOpportunities.length, totalBrokenLinks: totalBroken, generatedAt: new Date().toISOString() },
        opportunities: allOpportunities
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🏗️ Broken Link Building Opportunities — ${domain}\n\n`;
    md += `- **Prospects scanned**: ${prospectUrls.length}\n`;
    md += `- **Pages with broken links**: ${allOpportunities.length}\n`;
    md += `- **Total broken links found**: ${totalBroken}\n\n`;
    md += `> **Chiến thuật**: Liên hệ webmaster của các trang này, thông báo broken link, và đề xuất content của bạn thay thế.\n\n`;

    allOpportunities.forEach((opp, idx) => {
        md += `### ${idx + 1}. ${opp.prospectDomain}\n`;
        md += `**Page**: [${shortUrl(opp.prospectPage)}](${opp.prospectPage})\n\n`;
        md += mdTable(
            ['Broken URL', 'Anchor Text', 'Status'],
            ['brokenUrl', 'anchorText', 'statusCode'],
            opp.brokenLinks,
            { brokenUrl: v => `\`${v.substring(0, 80)}\`` }
        );
        md += '\n';
    });

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
