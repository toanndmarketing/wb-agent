/**
 * Module: Top Pages Performance Dashboard
 * Tổng hợp top pages theo 4 chiều: clicks, impressions, CTR, position
 */
const { getSearchConsoleClient } = require('../core/auth');
const { extractDomain, getDateRange } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, fmtCTR, fmtPos, shortUrl } = require('../core/reporter');

async function run(config) {
    const { siteUrl, days, rowLimit } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');

    printHeader('Top Pages Dashboard', config);
    const domain = extractDomain(siteUrl);

    const { searchconsole } = await getSearchConsoleClient();
    const { startDate, endDate } = getDateRange(days);

    console.log(`  Query range: ${startDate} → ${endDate}`);

    const res = await searchconsole.searchanalytics.query({
        siteUrl,
        requestBody: { startDate, endDate, dimensions: ['page'], rowLimit }
    });

    const pages = (res.data.rows || []).map(row => ({
        page: row.keys[0],
        clicks: row.clicks,
        impressions: row.impressions,
        ctr: row.ctr,
        position: row.position
    }));

    console.log(`  → ${pages.length} pages retrieved`);

    // Sort theo 4 chiều
    const TOP_N = 20;
    const topClicks = [...pages].sort((a, b) => b.clicks - a.clicks).slice(0, TOP_N);
    const topImpressions = [...pages].sort((a, b) => b.impressions - a.impressions).slice(0, TOP_N);
    const topCTR = [...pages].filter(p => p.impressions > 50).sort((a, b) => b.ctr - a.ctr).slice(0, TOP_N);
    const topPosition = [...pages].filter(p => p.impressions > 50).sort((a, b) => a.position - b.position).slice(0, TOP_N);

    // Tổng hợp stats
    const totalClicks = pages.reduce((s, p) => s + p.clicks, 0);
    const totalImpressions = pages.reduce((s, p) => s + p.impressions, 0);
    const avgCTR = totalImpressions > 0 ? totalClicks / totalImpressions : 0;
    const avgPosition = pages.length > 0 ? pages.reduce((s, p) => s + p.position, 0) / pages.length : 0;

    const reportData = {
        meta: { siteUrl, startDate, endDate, days, totalPages: pages.length, generatedAt: new Date().toISOString() },
        summary: { totalClicks, totalImpressions, avgCTR, avgPosition },
        topClicks, topImpressions, topCTR, topPosition
    };

    const files = getReportFilename('top-pages', domain);
    await saveJsonReport(files.json, reportData);

    // Markdown
    const makeTable = (rows) => mdTable(
        ['#', 'Page', 'Clicks', 'Impressions', 'CTR', 'Position'],
        ['_rank', 'page', 'clicks', 'impressions', 'ctr', 'position'],
        rows.map((r, i) => ({ ...r, _rank: i + 1 })),
        {
            page: (v) => `[${shortUrl(v, siteUrl)}](${v})`,
            ctr: fmtCTR,
            position: fmtPos
        }
    );

    let md = `# 📊 Top Pages Dashboard — ${domain}\n\n`;
    md += `- **Period**: ${startDate} → ${endDate} (${days} days)\n`;
    md += `- **Total Pages**: ${pages.length}\n`;
    md += `- **Total Clicks**: ${totalClicks.toLocaleString()}\n`;
    md += `- **Total Impressions**: ${totalImpressions.toLocaleString()}\n`;
    md += `- **Avg CTR**: ${fmtCTR(avgCTR)}\n`;
    md += `- **Avg Position**: ${avgPosition.toFixed(1)}\n\n`;

    md += `## 🏆 Top ${TOP_N} by Clicks\n\n${makeTable(topClicks)}\n`;
    md += `## 👁️ Top ${TOP_N} by Impressions\n\n${makeTable(topImpressions)}\n`;
    md += `## 🎯 Top ${TOP_N} by CTR (min 50 impressions)\n\n${makeTable(topCTR)}\n`;
    md += `## 📍 Top ${TOP_N} by Position (min 50 impressions)\n\n${makeTable(topPosition)}\n`;

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
