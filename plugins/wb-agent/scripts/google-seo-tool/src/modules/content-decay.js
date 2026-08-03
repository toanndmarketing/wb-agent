/**
 * Module: Content Decay Detector
 * So sánh 2 khoảng thời gian GSC → Phát hiện trang sụt traffic
 */
const { getSearchConsoleClient } = require('../core/auth');
const { extractDomain, getDateRange } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, fmtCTR, fmtChange, shortUrl, buildAgentInstructions } = require('../core/reporter');

async function run(config) {
    const { siteUrl, days, rowLimit } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');

    printHeader('Content Decay Detector', config);
    const domain = extractDomain(siteUrl);

    const { searchconsole } = await getSearchConsoleClient();

    // Tính 2 khoảng thời gian: current vs previous
    const halfDays = Math.floor(days / 2);
    const current = getDateRange(halfDays);
    const previous = (() => {
        const today = new Date();
        const end = new Date(today.getTime() - (halfDays + 2) * 24 * 60 * 60 * 1000);
        const start = new Date(today.getTime() - (days + 2) * 24 * 60 * 60 * 1000);
        return {
            startDate: start.toISOString().split('T')[0],
            endDate: end.toISOString().split('T')[0]
        };
    })();

    console.log(`  Period 1 (Previous): ${previous.startDate} → ${previous.endDate}`);
    console.log(`  Period 2 (Current):  ${current.startDate} → ${current.endDate}`);

    // Fetch data cho cả 2 periods
    const fetchPeriod = async (startDate, endDate) => {
        const res = await searchconsole.searchanalytics.query({
            siteUrl,
            requestBody: { startDate, endDate, dimensions: ['page'], rowLimit }
        });
        return (res.data.rows || []).reduce((map, row) => {
            map[row.keys[0]] = { clicks: row.clicks, impressions: row.impressions, ctr: row.ctr, position: row.position };
            return map;
        }, {});
    };

    console.log('  Fetching previous period...');
    const prevData = await fetchPeriod(previous.startDate, previous.endDate);
    console.log(`  → ${Object.keys(prevData).length} pages`);

    console.log('  Fetching current period...');
    const currData = await fetchPeriod(current.startDate, current.endDate);
    console.log(`  → ${Object.keys(currData).length} pages`);

    // So sánh → tìm pages bị decay
    const allPages = new Set([...Object.keys(prevData), ...Object.keys(currData)]);
    const decayResults = [];
    const growthResults = [];

    allPages.forEach(page => {
        const prev = prevData[page] || { clicks: 0, impressions: 0 };
        const curr = currData[page] || { clicks: 0, impressions: 0 };

        if (prev.clicks < 5 && curr.clicks < 5) return; // Skip low-traffic pages

        const clickChange = prev.clicks > 0
            ? ((curr.clicks - prev.clicks) / prev.clicks) * 100
            : (curr.clicks > 0 ? 100 : 0);
        const impressionChange = prev.impressions > 0
            ? ((curr.impressions - prev.impressions) / prev.impressions) * 100
            : (curr.impressions > 0 ? 100 : 0);

        const entry = {
            page,
            prevClicks: prev.clicks,
            currClicks: curr.clicks,
            clickChange,
            prevImpressions: prev.impressions,
            currImpressions: curr.impressions,
            impressionChange
        };

        if (clickChange < -10) {
            entry.severity = clickChange < -50 ? '🔴 Critical' : clickChange < -25 ? '🟠 High' : '🟡 Medium';
            decayResults.push(entry);
        } else if (clickChange > 20 && curr.clicks > 10) {
            growthResults.push(entry);
        }
    });

    decayResults.sort((a, b) => a.clickChange - b.clickChange);
    growthResults.sort((a, b) => b.clickChange - a.clickChange);

    const topDecay = decayResults.slice(0, 50);
    const topGrowth = growthResults.slice(0, 20);

    console.log(`\n  📉 Decaying pages: ${decayResults.length}`);
    console.log(`  📈 Growing pages: ${growthResults.length}`);

    // Build report
    const files = getReportFilename('content-decay', domain);
    const reportData = {
        meta: { siteUrl, previousPeriod: previous, currentPeriod: current, generatedAt: new Date().toISOString() },
        decay: topDecay,
        growth: topGrowth
    };

    await saveJsonReport(files.json, reportData);

    // Markdown report
    let md = `# 📉 Content Decay Report — ${domain}\n\n`;
    md += `- **Previous**: ${previous.startDate} → ${previous.endDate}\n`;
    md += `- **Current**: ${current.startDate} → ${current.endDate}\n`;
    md += `- **Decaying pages found**: ${decayResults.length}\n`;
    md += `- **Growing pages found**: ${growthResults.length}\n\n`;

    md += `## 🔴 Top ${topDecay.length} Decaying Pages\n\n`;
    md += mdTable(
        ['Severity', 'Page', 'Clicks trước', 'Clicks sau', '% Thay đổi', 'Impressions %'],
        ['severity', 'page', 'prevClicks', 'currClicks', 'clickChange', 'impressionChange'],
        topDecay,
        {
            page: (v) => `[${shortUrl(v, siteUrl)}](${v})`,
            clickChange: fmtChange,
            impressionChange: fmtChange
        }
    );

    md += `\n## 📈 Top ${topGrowth.length} Growing Pages\n\n`;
    md += mdTable(
        ['Page', 'Clicks trước', 'Clicks sau', '% Thay đổi'],
        ['page', 'prevClicks', 'currClicks', 'clickChange'],
        topGrowth,
        {
            page: (v) => `[${shortUrl(v, siteUrl)}](${v})`,
            clickChange: fmtChange
        }
    );

    // Agent Instructions for decaying pages
    const agentActions = topDecay.slice(0, 10).map(d => ({
        priority: d.clickChange < -50 ? 'P0-CRITICAL' : d.clickChange < -25 ? 'P1-HIGH' : 'P2-MEDIUM',
        title: `Refresh content: ${shortUrl(d.page, siteUrl)}`,
        description: `Traffic giảm ${Math.abs(d.clickChange).toFixed(0)}% (${d.prevClicks}→${d.currClicks} clicks). Cần cập nhật nội dung, thêm thông tin mới, tối ưu title/meta.`,
        files: `Page route: ${shortUrl(d.page, siteUrl)}`
    }));

    md += buildAgentInstructions(agentActions);

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
