/**
 * Module: Internal Link Graph Analyzer
 * BFS crawl từ homepage → Xây bản đồ liên kết nội bộ → Phát hiện orphan pages
 */
const { fetchPage, parseSitemap, extractLinks } = require('../core/crawler');
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, shortUrl, buildAgentInstructions } = require('../core/reporter');

async function run(config) {
    const { siteUrl, sitemapUrl, crawlConcurrency, crawlDelay, maxPages, userAgent } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');

    printHeader('Internal Link Graph Analyzer', config);
    const domain = extractDomain(siteUrl);
    const baseUrl = siteUrl.replace(/\/$/, '');

    // BFS crawl
    const visited = new Set();
    const queue = [baseUrl + '/'];
    const graph = {}; // page → { inLinks: [], outLinks: [], title }
    let crawled = 0;

    console.log('  BFS crawling from homepage...\n');

    while (queue.length > 0 && crawled < maxPages) {
        // Process in batches
        const batchSize = Math.min(crawlConcurrency, queue.length, maxPages - crawled);
        const batch = queue.splice(0, batchSize);

        const results = await Promise.all(batch.map(async (url) => {
            const normalUrl = normalizeUrl(url);
            if (visited.has(normalUrl)) return null;
            visited.add(normalUrl);

            try {
                const { $, statusCode } = await fetchPage(url, { userAgent, timeout: 10000 });
                if (statusCode !== 200) return { url: normalUrl, links: [], title: '', statusCode };

                const title = $('title').first().text().trim();
                const { internal } = extractLinks($, url);
                const internalHrefs = internal.map(l => normalizeUrl(l.href)).filter(h => h);

                return { url: normalUrl, links: internalHrefs, title, statusCode };
            } catch {
                return { url: normalUrl, links: [], title: '', statusCode: 0 };
            }
        }));

        results.filter(Boolean).forEach(({ url, links, title, statusCode }) => {
            if (!graph[url]) graph[url] = { inLinks: [], outLinks: [], title, statusCode };
            graph[url].outLinks = links;
            graph[url].title = title;
            graph[url].statusCode = statusCode;

            // Update inLinks for target pages
            links.forEach(targetUrl => {
                if (!graph[targetUrl]) graph[targetUrl] = { inLinks: [], outLinks: [], title: '', statusCode: null };
                if (!graph[targetUrl].inLinks.includes(url)) {
                    graph[targetUrl].inLinks.push(url);
                }
            });

            // Add unvisited links to queue
            links.forEach(l => {
                if (!visited.has(l) && !queue.includes(l)) queue.push(l);
            });

            crawled++;
        });

        process.stdout.write(`\r  Crawled: ${crawled} | Queue: ${queue.length}`);
        if (crawlDelay > 0) await new Promise(r => setTimeout(r, crawlDelay));
    }
    console.log('\n');

    // Find orphan pages from sitemap
    let orphanPages = [];
    const targetSitemap = sitemapUrl || baseUrl + '/sitemap.xml';
    try {
        console.log('  Comparing with sitemap...');
        const sitemapUrls = await parseSitemap(targetSitemap);
        const sitemapSet = new Set(sitemapUrls.map(u => normalizeUrl(u.url)));
        const crawledSet = new Set(Object.keys(graph));

        // Pages in sitemap but not found during crawl (orphans)
        orphanPages = [...sitemapSet]
            .filter(url => !crawledSet.has(url) || (graph[url] && graph[url].inLinks.length === 0))
            .map(url => ({ url, inLinks: graph[url] ? graph[url].inLinks.length : 0, inSitemap: true }));

        console.log(`  → ${orphanPages.length} potential orphan pages`);
    } catch (e) {
        console.log(`  → Could not compare with sitemap: ${e.message}`);
    }

    // Analysis
    const pages = Object.entries(graph).map(([url, data]) => ({
        url,
        title: data.title,
        inLinks: data.inLinks.length,
        outLinks: data.outLinks.length,
        statusCode: data.statusCode
    }));

    const noInLinks = pages.filter(p => p.inLinks === 0 && p.statusCode === 200);
    const fewInLinks = pages.filter(p => p.inLinks > 0 && p.inLinks <= 2 && p.statusCode === 200);
    const manyOutLinks = pages.filter(p => p.outLinks > 50).sort((a, b) => b.outLinks - a.outLinks);
    const deadEnds = pages.filter(p => p.outLinks === 0 && p.statusCode === 200);

    const avgInLinks = pages.length > 0 ? (pages.reduce((s, p) => s + p.inLinks, 0) / pages.length).toFixed(1) : 0;
    const avgOutLinks = pages.length > 0 ? (pages.reduce((s, p) => s + p.outLinks, 0) / pages.length).toFixed(1) : 0;

    console.log(`  Total pages in graph: ${pages.length}`);
    console.log(`  Avg internal links per page: In=${avgInLinks}, Out=${avgOutLinks}`);
    console.log(`  Pages with 0 in-links: ${noInLinks.length}`);
    console.log(`  Dead-end pages (0 out-links): ${deadEnds.length}`);

    const files = getReportFilename('internal-links', domain);
    const reportData = {
        meta: { siteUrl, pagesCrawled: crawled, totalPagesInGraph: pages.length, avgInLinks, avgOutLinks, generatedAt: new Date().toISOString() },
        summary: { noInLinks: noInLinks.length, fewInLinks: fewInLinks.length, deadEnds: deadEnds.length, orphanPages: orphanPages.length },
        noInLinks: noInLinks.slice(0, 50),
        fewInLinks: fewInLinks.slice(0, 50),
        deadEnds: deadEnds.slice(0, 30),
        manyOutLinks: manyOutLinks.slice(0, 20),
        orphanPages: orphanPages.slice(0, 50)
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🕸️ Internal Link Graph — ${domain}\n\n`;
    md += `- **Pages Crawled**: ${crawled}\n`;
    md += `- **Total Pages in Graph**: ${pages.length}\n`;
    md += `- **Avg In-links/page**: ${avgInLinks}\n`;
    md += `- **Avg Out-links/page**: ${avgOutLinks}\n\n`;

    md += `## 📊 Summary\n\n`;
    md += `| Issue | Count | Action |\n| :--- | :---: | :--- |\n`;
    md += `| 🚫 No in-links (0) | ${noInLinks.length} | Thêm internal links trỏ đến |\n`;
    md += `| ⚠️ Few in-links (1-2) | ${fewInLinks.length} | Cần thêm links |\n`;
    md += `| 🛑 Dead-end pages (0 out-links) | ${deadEnds.length} | Thêm links ra ngoài |\n`;
    md += `| 👻 Orphan pages | ${orphanPages.length} | Không ai link đến |\n\n`;

    if (noInLinks.length > 0) {
        md += `## 🚫 Pages Without Any In-links\n\n`;
        md += mdTable(['Page', 'Out-links'], ['url', 'outLinks'], noInLinks.slice(0, 30), { url: v => `[${shortUrl(v, siteUrl)}](${v})` });
        md += '\n';
    }

    if (orphanPages.length > 0) {
        md += `## 👻 Orphan Pages (In sitemap but unreachable)\n\n`;
        md += mdTable(['Page', 'In-links'], ['url', 'inLinks'], orphanPages.slice(0, 30), { url: v => `[${shortUrl(v, siteUrl)}](${v})` });
        md += '\n';
    }

    if (deadEnds.length > 0) {
        md += `## 🛑 Dead-End Pages (No out-links)\n\n`;
        md += mdTable(['Page', 'In-links'], ['url', 'inLinks'], deadEnds.slice(0, 30), { url: v => `[${shortUrl(v, siteUrl)}](${v})` });
    }

    // Agent Instructions
    const agentActions = [];
    if (orphanPages.length > 0) {
        agentActions.push({
            priority: 'P1-HIGH',
            title: `Link đến ${orphanPages.length} orphan pages`,
            description: `Các trang này nằm trong sitemap nhưng không có internal link nào trỏ đến. Thêm link từ các trang liên quan.`,
            files: 'Sidebar, Footer, hoặc Related Posts components',
            details: orphanPages.slice(0, 5).map(p => shortUrl(p.url, siteUrl)).join(', ')
        });
    }
    if (noInLinks.length > 0) {
        agentActions.push({
            priority: 'P1-HIGH',
            title: `Thêm internal links cho ${noInLinks.length} trang cô lập`,
            description: `Các trang này không có link nội bộ nào trỏ đến. Googlebot có thể không crawl được.`,
            files: 'Navigation, breadcrumbs, hoặc contextual links',
            details: noInLinks.slice(0, 5).map(p => shortUrl(p.url, siteUrl)).join(', ')
        });
    }
    if (deadEnds.length > 0) {
        agentActions.push({
            priority: 'P2-MEDIUM',
            title: `Thêm outgoing links cho ${deadEnds.length} dead-end pages`,
            description: `Các trang này không có link nào ra. Thêm Related Posts hoặc CTA links.`,
            files: 'Page templates, Related section'
        });
    }

    md += buildAgentInstructions(agentActions);

    await saveMarkdownReport(files.md, md);
    return reportData;
}

function normalizeUrl(url) {
    try {
        const u = new URL(url);
        // Remove trailing slash, fragments, common tracking params
        let path = u.pathname.replace(/\/$/, '') || '/';
        const port = u.port ? `:${u.port}` : '';
        return `${u.protocol}//${u.hostname}${port}${path}`;
    } catch {
        return url;
    }
}

module.exports = { run };
