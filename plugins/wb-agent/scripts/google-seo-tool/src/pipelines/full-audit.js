/**
 * Pipeline: Full Audit Orchestrator
 * Chạy tất cả analysis modules → Tổng hợp 1 báo cáo toàn diện
 */
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport } = require('../core/reporter');

// Import analysis modules (read-only, safe to auto-run)
// NOTE: outbound-audit, brand-mentions, broken-link-build, content-gap
//       are MANUAL-ONLY — they send requests to external sites or consume CSE quota.
//       Indexing Submitter is MANUAL-ONLY — it WRITES data to Google.
const contentDecay = require('../modules/content-decay');
const topPages = require('../modules/top-pages');
const geoDevice = require('../modules/geo-device');
const technicalAudit = require('../modules/technical-audit');
const sitemapHealth = require('../modules/sitemap-health');
const internalLinks = require('../modules/internal-links');

async function run(config) {
    const { siteUrl } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');

    printHeader('FULL SEO AUDIT PIPELINE', config);
    const domain = extractDomain(siteUrl);
    const startTime = Date.now();
    const results = {};
    const errors = {};

    // 6 modules an toàn: chỉ đọc GSC API hoặc crawl site mình
    const modules = [
        { name: 'content-decay', label: '📉 Content Decay', fn: contentDecay },
        { name: 'top-pages', label: '📊 Top Pages', fn: topPages },
        { name: 'geo-device', label: '🌍 Geo & Device', fn: geoDevice },
        { name: 'technical-audit', label: '🔧 Technical Audit', fn: technicalAudit },
        { name: 'sitemap-health', label: '🗺️ Sitemap Health', fn: sitemapHealth },
        { name: 'internal-links', label: '🕸️ Internal Links', fn: internalLinks }
    ];

    for (let i = 0; i < modules.length; i++) {
        const mod = modules[i];
        console.log(`\n${'═'.repeat(50)}`);
        console.log(`  [${i + 1}/${modules.length}] ${mod.label}`);
        console.log('═'.repeat(50));

        try {
            results[mod.name] = await mod.fn.run(config);
            console.log(`  ✅ ${mod.label} completed`);
        } catch (e) {
            console.error(`  ❌ ${mod.label} failed: ${e.message}`);
            errors[mod.name] = e.message;
        }
    }

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    // Build unified report
    const files = getReportFilename('full-audit', domain);
    const reportData = {
        meta: {
            siteUrl,
            domain,
            modulesRun: modules.length,
            modulesSuccess: Object.keys(results).length,
            modulesFailed: Object.keys(errors).length,
            elapsedSeconds: parseFloat(elapsed),
            generatedAt: new Date().toISOString()
        },
        errors,
        summary: {}
    };

    // Extract key metrics from each module
    if (results['technical-audit']?.meta) {
        reportData.summary.technicalScore = results['technical-audit'].meta.avgScore;
        reportData.summary.topIssues = (results['technical-audit'].topIssues || []).slice(0, 5);
    }
    if (results['sitemap-health']?.meta) {
        reportData.summary.sitemapHealth = results['sitemap-health'].meta.healthScore;
    }
    if (results['content-decay']?.decay) {
        reportData.summary.decayingPages = results['content-decay'].decay.length;
    }
    if (results['top-pages']?.summary) {
        reportData.summary.totalClicks = results['top-pages'].summary.totalClicks;
        reportData.summary.totalImpressions = results['top-pages'].summary.totalImpressions;
    }
    if (results['internal-links']?.summary) {
        reportData.summary.orphanPages = results['internal-links'].summary.orphanPages;
        reportData.summary.deadEnds = results['internal-links'].summary.deadEnds;
    }

    await saveJsonReport(files.json, reportData);

    // Unified Markdown
    let md = `# 🏆 Full SEO Audit Report — ${domain}\n\n`;
    md += `- **Generated**: ${new Date().toISOString()}\n`;
    md += `- **Duration**: ${elapsed}s\n`;
    md += `- **Modules**: ${Object.keys(results).length}/${modules.length} completed\n\n`;

    md += `## 📊 Executive Summary\n\n`;
    md += `| Metric | Value | Status |\n| :--- | :---: | :---: |\n`;

    if (reportData.summary.technicalScore != null) {
        const s = reportData.summary.technicalScore;
        md += `| Technical SEO Score | ${s}/100 | ${s >= 80 ? '🟢' : s >= 50 ? '🟡' : '🔴'} |\n`;
    }
    if (reportData.summary.sitemapHealth != null) {
        const s = reportData.summary.sitemapHealth;
        md += `| Sitemap Health | ${s}% | ${s >= 90 ? '🟢' : s >= 70 ? '🟡' : '🔴'} |\n`;
    }
    if (reportData.summary.totalClicks != null) {
        md += `| Total Clicks (period) | ${reportData.summary.totalClicks.toLocaleString()} | ℹ️ |\n`;
    }
    if (reportData.summary.totalImpressions != null) {
        md += `| Total Impressions | ${reportData.summary.totalImpressions.toLocaleString()} | ℹ️ |\n`;
    }
    if (reportData.summary.decayingPages != null) {
        const d = reportData.summary.decayingPages;
        md += `| Decaying Pages | ${d} | ${d === 0 ? '🟢' : d <= 5 ? '🟡' : '🔴'} |\n`;
    }
    if (reportData.summary.orphanPages != null) {
        md += `| Orphan Pages | ${reportData.summary.orphanPages} | ${reportData.summary.orphanPages === 0 ? '🟢' : '🟡'} |\n`;
    }
    if (reportData.summary.brokenOutbound != null) {
        const b = reportData.summary.brokenOutbound;
        md += `| Broken Outbound Links | ${b} | ${b === 0 ? '🟢' : '🔴'} |\n`;
    }
    md += '\n';

    // Top Issues
    if (reportData.summary.topIssues?.length > 0) {
        md += `## 🚨 Top Technical Issues\n\n`;
        reportData.summary.topIssues.forEach((issue, i) => {
            md += `${i + 1}. **${issue.issue}** — ${issue.count} pages (${issue.percent})\n`;
        });
        md += '\n';
    }

    // Errors
    if (Object.keys(errors).length > 0) {
        md += `## ⚠️ Module Errors\n\n`;
        Object.entries(errors).forEach(([name, msg]) => {
            md += `- **${name}**: ${msg}\n`;
        });
        md += '\n';
    }

    md += `---\n\n> Chi tiết từng module xem trong các file report riêng lẻ tại thư mục \`reports/\`.\n`;

    await saveMarkdownReport(files.md, md);

    console.log('\n══════════════════════════════════════════════════');
    console.log(`  🏆 FULL AUDIT COMPLETE — ${domain}`);
    console.log(`  Duration: ${elapsed}s`);
    console.log(`  Success: ${Object.keys(results).length}/${modules.length}`);
    console.log('══════════════════════════════════════════════════');

    return reportData;
}

module.exports = { run };
