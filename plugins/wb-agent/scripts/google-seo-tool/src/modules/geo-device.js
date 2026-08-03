/**
 * Module: Geo & Device Performance Breakdown
 * Phân tích hiệu suất SEO theo quốc gia và thiết bị
 */
const { getSearchConsoleClient } = require('../core/auth');
const { extractDomain, getDateRange } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, fmtCTR, fmtPos } = require('../core/reporter');

async function run(config) {
    const { siteUrl, days, rowLimit } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');

    printHeader('Geo & Device Breakdown', config);
    const domain = extractDomain(siteUrl);

    const { searchconsole } = await getSearchConsoleClient();
    const { startDate, endDate } = getDateRange(days);

    console.log(`  Query range: ${startDate} → ${endDate}`);

    // Query by Country
    console.log('  Fetching country data...');
    const countryRes = await searchconsole.searchanalytics.query({
        siteUrl,
        requestBody: { startDate, endDate, dimensions: ['country'], rowLimit: 250 }
    });
    const countries = (countryRes.data.rows || []).map(row => ({
        country: row.keys[0],
        clicks: row.clicks,
        impressions: row.impressions,
        ctr: row.ctr,
        position: row.position
    })).sort((a, b) => b.clicks - a.clicks);

    console.log(`  → ${countries.length} countries`);

    // Query by Device
    console.log('  Fetching device data...');
    const deviceRes = await searchconsole.searchanalytics.query({
        siteUrl,
        requestBody: { startDate, endDate, dimensions: ['device'], rowLimit: 10 }
    });
    const devices = (deviceRes.data.rows || []).map(row => ({
        device: row.keys[0],
        clicks: row.clicks,
        impressions: row.impressions,
        ctr: row.ctr,
        position: row.position
    })).sort((a, b) => b.clicks - a.clicks);

    console.log(`  → ${devices.length} device types`);

    // Query by Date (trend)
    console.log('  Fetching daily trend...');
    const dateRes = await searchconsole.searchanalytics.query({
        siteUrl,
        requestBody: { startDate, endDate, dimensions: ['date'], rowLimit: 1000 }
    });
    const dailyTrend = (dateRes.data.rows || []).map(row => ({
        date: row.keys[0],
        clicks: row.clicks,
        impressions: row.impressions,
        ctr: row.ctr,
        position: row.position
    })).sort((a, b) => a.date.localeCompare(b.date));

    // Calculate device share
    const totalDeviceClicks = devices.reduce((s, d) => s + d.clicks, 0);
    devices.forEach(d => {
        d.share = totalDeviceClicks > 0 ? ((d.clicks / totalDeviceClicks) * 100).toFixed(1) + '%' : '0%';
    });

    const reportData = {
        meta: { siteUrl, startDate, endDate, days, generatedAt: new Date().toISOString() },
        countries: countries.slice(0, 50),
        devices,
        dailyTrend
    };

    const files = getReportFilename('geo-device', domain);
    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🌍 Geo & Device Breakdown — ${domain}\n\n`;
    md += `**Period**: ${startDate} → ${endDate} (${days} days)\n\n`;

    md += `## 📱 Device Performance\n\n`;
    md += mdTable(
        ['Device', 'Clicks', 'Impressions', 'CTR', 'Position', 'Share'],
        ['device', 'clicks', 'impressions', 'ctr', 'position', 'share'],
        devices,
        { ctr: fmtCTR, position: fmtPos, device: (v) => `**${v}**` }
    );

    md += `\n## 🌐 Top ${Math.min(countries.length, 30)} Countries\n\n`;
    md += mdTable(
        ['Country', 'Clicks', 'Impressions', 'CTR', 'Avg Position'],
        ['country', 'clicks', 'impressions', 'ctr', 'position'],
        countries.slice(0, 30),
        { ctr: fmtCTR, position: fmtPos }
    );

    // Daily trend summary (first 7 + last 7 days)
    if (dailyTrend.length > 14) {
        md += `\n## 📅 Daily Trend (First 7 vs Last 7 days)\n\n`;
        const first7 = dailyTrend.slice(0, 7);
        const last7 = dailyTrend.slice(-7);
        const first7Clicks = first7.reduce((s, d) => s + d.clicks, 0);
        const last7Clicks = last7.reduce((s, d) => s + d.clicks, 0);
        const trendChange = first7Clicks > 0 ? ((last7Clicks - first7Clicks) / first7Clicks * 100).toFixed(1) : 'N/A';

        md += `| Metric | First 7 days | Last 7 days | Change |\n`;
        md += `| :--- | :---: | :---: | :---: |\n`;
        md += `| Total Clicks | ${first7Clicks} | ${last7Clicks} | ${trendChange}% |\n`;
        md += `| Avg Clicks/day | ${(first7Clicks / 7).toFixed(0)} | ${(last7Clicks / 7).toFixed(0)} | - |\n`;
    }

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
