/**
 * Module: Outbound Link Auditor
 * Phân tích tất cả link ra bên ngoài website → Phát hiện broken links, missing nofollow
 */
const { parseSitemap, fetchPage, headCheck, batchProcess, extractLinks } = require('../core/crawler');
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, shortUrl } = require('../core/reporter');

async function run(config) {
    const { sitemapUrl, siteUrl, crawlConcurrency, crawlDelay, maxPages, userAgent } = config;
    const targetSitemap = sitemapUrl || (siteUrl ? siteUrl.replace(/\/$/, '') + '/sitemap.xml' : null);
    if (!targetSitemap) throw new Error('[CRITICAL] --sitemap hoặc SITEMAP_URL là bắt buộc.');

    printHeader('Outbound Link Auditor', { ...config, sitemapUrl: targetSitemap });
    const domain = extractDomain(siteUrl || targetSitemap);

    // Step 1: Parse sitemap & crawl pages to extract external links
    console.log('  Step 1: Parsing sitemap...');
    const sitemapUrls = await parseSitemap(targetSitemap);
    const urls = sitemapUrls.slice(0, maxPages).map(u => u.url);
    console.log(`  → Scanning ${urls.length} pages for outbound links...\n`);

    const allExternalLinks = [];

    const pageResults = await batchProcess(urls, async (url) => {
        try {
            const { $ } = await fetchPage(url, { userAgent });
            const { external } = extractLinks($, url);
            return { url, externalLinks: external };
        } catch (e) {
            return { url, externalLinks: [], error: e.message };
        }
    }, {
        concurrency: crawlConcurrency,
        delay: crawlDelay,
        onProgress: (done, total) => process.stdout.write(`\r  Crawling: ${done}/${total}`)
    });
    console.log('\n');

    // Aggregate external links
    const externalLinkMap = new Map(); // href → {sourcePpages, text, nofollow, ...}
    pageResults.forEach(({ url: sourceUrl, externalLinks }) => {
        externalLinks.forEach(link => {
            if (!externalLinkMap.has(link.href)) {
                externalLinkMap.set(link.href, { ...link, sourcePages: [sourceUrl], count: 1 });
            } else {
                const existing = externalLinkMap.get(link.href);
                if (!existing.sourcePages.includes(sourceUrl)) {
                    existing.sourcePages.push(sourceUrl);
                }
                existing.count++;
            }
        });
    });

    const uniqueExternalLinks = Array.from(externalLinkMap.values());
    console.log(`  → Found ${uniqueExternalLinks.length} unique outbound links`);

    // Step 2: Check status of external links
    console.log('  Step 2: Checking outbound link health...\n');
    const checkedLinks = await batchProcess(
        uniqueExternalLinks,
        async (linkData) => {
            const { statusCode } = await headCheck(linkData.href, { userAgent });
            return { ...linkData, statusCode };
        },
        {
            concurrency: crawlConcurrency,
            delay: crawlDelay,
            onProgress: (done, total) => process.stdout.write(`\r  Checking: ${done}/${total}`)
        }
    );
    console.log('\n');

    // Categorize
    const brokenLinks = checkedLinks.filter(l => l.statusCode === 404 || l.statusCode === 410 || l.statusCode === 0);
    const redirectLinks = checkedLinks.filter(l => l.statusCode >= 300 && l.statusCode < 400);
    const nofollowMissing = checkedLinks.filter(l => !l.nofollow && l.statusCode === 200);
    const healthyLinks = checkedLinks.filter(l => l.statusCode === 200);

    // Links to external domains without nofollow (potential link juice leaks)
    const domainLeaks = {};
    nofollowMissing.forEach(l => {
        try {
            const extDomain = new URL(l.href).hostname;
            if (!domainLeaks[extDomain]) domainLeaks[extDomain] = [];
            domainLeaks[extDomain].push(l);
        } catch {}
    });
    const topLeakDomains = Object.entries(domainLeaks)
        .sort(([, a], [, b]) => b.length - a.length)
        .slice(0, 20)
        .map(([domain, links]) => ({ domain, linkCount: links.length, dofollow: true }));

    console.log(`  ✅ Healthy: ${healthyLinks.length}`);
    console.log(`  ❌ Broken: ${brokenLinks.length}`);
    console.log(`  ↪️ Redirects: ${redirectLinks.length}`);
    console.log(`  ⚠️ Dofollow (no nofollow): ${nofollowMissing.length}`);

    const files = getReportFilename('outbound-audit', domain);
    const reportData = {
        meta: { siteUrl: siteUrl || targetSitemap, pagesScanned: urls.length, totalOutbound: uniqueExternalLinks.length, generatedAt: new Date().toISOString() },
        summary: { healthy: healthyLinks.length, broken: brokenLinks.length, redirects: redirectLinks.length, dofollowNoNofollow: nofollowMissing.length },
        brokenLinks: brokenLinks.slice(0, 50),
        redirectLinks: redirectLinks.slice(0, 30),
        topLeakDomains
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🔗 Outbound Link Audit — ${domain}\n\n`;
    md += `- **Pages Scanned**: ${urls.length}\n`;
    md += `- **Total Outbound Links**: ${uniqueExternalLinks.length}\n\n`;
    md += `| Category | Count |\n| :--- | :---: |\n`;
    md += `| ✅ Healthy (200) | ${healthyLinks.length} |\n`;
    md += `| ❌ Broken (404/0) | ${brokenLinks.length} |\n`;
    md += `| ↪️ Redirect (3xx) | ${redirectLinks.length} |\n`;
    md += `| ⚠️ Dofollow (leaking juice) | ${nofollowMissing.length} |\n\n`;

    if (brokenLinks.length > 0) {
        md += `## ❌ Broken Outbound Links — Cần xoá hoặc thay thế\n\n`;
        md += mdTable(
            ['Status', 'External URL', 'Anchor Text', 'Found On'],
            ['statusCode', 'href', 'text', '_source'],
            brokenLinks.slice(0, 30).map(l => ({ ...l, _source: shortUrl(l.sourcePages[0], siteUrl) }))
        );
        md += '\n';
    }

    if (topLeakDomains.length > 0) {
        md += `## ⚠️ Top Dofollow Domains (Link Juice Leaks)\n\n`;
        md += `> Các domain nhận link dofollow nhiều nhất — xem xét thêm \`rel="nofollow"\` nếu không cần thiết.\n\n`;
        md += mdTable(
            ['Domain', 'Số lượng dofollow links'],
            ['domain', 'linkCount'],
            topLeakDomains
        );
    }

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
