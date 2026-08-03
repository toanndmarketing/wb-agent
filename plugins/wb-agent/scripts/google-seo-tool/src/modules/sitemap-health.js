/**
 * Module: Sitemap Health Checker
 * Kiểm tra tính toàn vẹn của Sitemap — phát hiện URLs chết, redirect, lỗi server
 */
const { parseSitemap, headCheck, batchProcess } = require('../core/crawler');
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, shortUrl, buildAgentInstructions } = require('../core/reporter');

async function run(config) {
    const { sitemapUrl, siteUrl, crawlConcurrency, crawlDelay, maxPages } = config;
    const targetSitemap = sitemapUrl || (siteUrl ? siteUrl.replace(/\/$/, '') + '/sitemap.xml' : null);
    if (!targetSitemap) throw new Error('[CRITICAL] --sitemap hoặc SITEMAP_URL là bắt buộc.');

    printHeader('Sitemap Health Checker', { ...config, sitemapUrl: targetSitemap });
    const domain = extractDomain(siteUrl || targetSitemap);

    console.log('  Parsing sitemap...');
    const sitemapUrls = await parseSitemap(targetSitemap);
    const urls = sitemapUrls.slice(0, maxPages);
    console.log(`  → ${sitemapUrls.length} URLs found, checking ${urls.length}`);

    console.log('  Checking URLs...\n');
    const results = await batchProcess(
        urls.map(u => u.url),
        async (url) => {
            const { statusCode, redirectUrl } = await headCheck(url);
            return { url, statusCode, redirectUrl };
        },
        {
            concurrency: crawlConcurrency,
            delay: crawlDelay,
            onProgress: (done, total) => {
                process.stdout.write(`\r  Progress: ${done}/${total} (${Math.round(done/total*100)}%)`);
            }
        }
    );
    console.log('\n');

    // Categorize
    const ok = results.filter(r => r.statusCode === 200);
    const redirects = results.filter(r => r.statusCode >= 300 && r.statusCode < 400);
    const notFound = results.filter(r => r.statusCode === 404 || r.statusCode === 410);
    const serverErrors = results.filter(r => r.statusCode >= 500);
    const timeouts = results.filter(r => r.statusCode === 408 || r.statusCode === 0);
    const other = results.filter(r => !ok.includes(r) && !redirects.includes(r) && !notFound.includes(r) && !serverErrors.includes(r) && !timeouts.includes(r));

    const healthScore = results.length > 0 ? Math.round((ok.length / results.length) * 100) : 0;

    console.log(`  Health Score: ${healthScore}%`);
    console.log(`  ✅ OK (200): ${ok.length}`);
    console.log(`  ↪️ Redirects (3xx): ${redirects.length}`);
    console.log(`  ❌ Not Found (404/410): ${notFound.length}`);
    console.log(`  💥 Server Errors (5xx): ${serverErrors.length}`);
    console.log(`  ⏱️ Timeouts: ${timeouts.length}`);

    const files = getReportFilename('sitemap-health', domain);
    const reportData = {
        meta: {
            sitemapUrl: targetSitemap,
            totalUrls: results.length,
            healthScore,
            generatedAt: new Date().toISOString()
        },
        summary: {
            ok: ok.length,
            redirects: redirects.length,
            notFound: notFound.length,
            serverErrors: serverErrors.length,
            timeouts: timeouts.length,
            other: other.length
        },
        issues: { redirects, notFound, serverErrors, timeouts }
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🗺️ Sitemap Health Report — ${domain}\n\n`;
    md += `- **Sitemap**: ${targetSitemap}\n`;
    md += `- **Health Score**: **${healthScore}%** ${healthScore >= 90 ? '🟢' : healthScore >= 70 ? '🟡' : '🔴'}\n`;
    md += `- **Total URLs**: ${results.length}\n\n`;

    md += `## 📊 Summary\n\n`;
    md += `| Status | Count | % |\n| :--- | :---: | :---: |\n`;
    md += `| ✅ OK (200) | ${ok.length} | ${(ok.length/results.length*100).toFixed(1)}% |\n`;
    md += `| ↪️ Redirects (3xx) | ${redirects.length} | ${(redirects.length/results.length*100).toFixed(1)}% |\n`;
    md += `| ❌ Not Found (404/410) | ${notFound.length} | ${(notFound.length/results.length*100).toFixed(1)}% |\n`;
    md += `| 💥 Server Errors (5xx) | ${serverErrors.length} | ${(serverErrors.length/results.length*100).toFixed(1)}% |\n`;
    md += `| ⏱️ Timeouts | ${timeouts.length} | ${(timeouts.length/results.length*100).toFixed(1)}% |\n\n`;

    if (notFound.length > 0) {
        md += `## ❌ Not Found (404/410) — Cần xoá khỏi sitemap\n\n`;
        md += mdTable(['URL', 'Status'], ['url', 'statusCode'], notFound, { url: v => `\`${shortUrl(v, siteUrl)}\`` });
        md += `\n`;
    }

    if (redirects.length > 0) {
        md += `## ↪️ Redirects (3xx) — Nên cập nhật URL trong sitemap\n\n`;
        md += mdTable(['URL', 'Status', 'Redirect To'], ['url', 'statusCode', 'redirectUrl'], redirects,
            { url: v => `\`${shortUrl(v, siteUrl)}\``, redirectUrl: v => v ? `\`${v}\`` : '-' });
        md += `\n`;
    }

    if (serverErrors.length > 0) {
        md += `## 💥 Server Errors (5xx) — Cần kiểm tra server\n\n`;
        md += mdTable(['URL', 'Status'], ['url', 'statusCode'], serverErrors, { url: v => `\`${shortUrl(v, siteUrl)}\`` });
    }

    // Agent Instructions
    const agentActions = [];
    if (notFound.length > 0) {
        agentActions.push({
            priority: 'P1-HIGH',
            title: `Xóa ${notFound.length} URLs chết khỏi sitemap`,
            description: `Các URL trả về 404/410 cần được xóa khỏi sitemap.xml hoặc tạo redirect 301.`,
            files: 'sitemap.xml hoặc next-sitemap config',
            details: notFound.map(n => n.url).slice(0, 10).join(', ')
        });
    }
    if (redirects.length > 0) {
        agentActions.push({
            priority: 'P2-MEDIUM',
            title: `Cập nhật ${redirects.length} URLs redirect trong sitemap`,
            description: `Thay thế URL cũ bằng URL đích của redirect trong sitemap.xml.`,
            files: 'sitemap.xml hoặc next-sitemap config'
        });
    }

    md += buildAgentInstructions(agentActions);

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
