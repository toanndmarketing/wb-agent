#!/usr/bin/env node
/**
 * Agent SEO Tool — Unified CLI Entry Point
 *
 * Usage:
 *   node cli.js <command> [options]
 *
 * Commands:
 *   index          Submit URLs to Google Indexing API (legacy: index.js)
 *   analyze        GSC keyword analysis (legacy: gsc-analyzer.js)
 *   decay          Content decay detection
 *   top-pages      Top pages performance dashboard
 *   geo            Geo & device breakdown
 *   audit          Technical SEO audit (crawl-based)
 *   sitemap        Sitemap health check
 *   outbound       Outbound link audit
 *   internal       Internal link graph analysis
 *   mentions       Brand mention monitoring (requires Google CSE)
 *   broken-links   Broken link building scanner
 *   content-gap    Competitor content gap analysis (requires Google CSE)
 *   full-audit     Run all analysis modules
 *
 * Common Options:
 *   --site URL          Target site (GSC property URL)
 *   --sitemap URL       Sitemap URL
 *   --url URL           Target specific URL for single page audit & GSC Inspection
 *   --days N            Date range in days (default: 30)
 *   --limit N           Row limit for GSC API (default: 5000)
 *   --concurrency N     Crawler concurrency (default: 5)
 *   --max-pages N       Max pages to crawl (default: 200)
 *   --brand NAME        Brand name for mention monitoring
 *   --cse-key KEY       Google Custom Search API key
 *   --cse-id ID         Google Custom Search Engine ID
 */

// Load ENV first
const { loadEnv } = require('./src/core/env');
loadEnv();

const { buildConfig } = require('./src/core/config');
const { setOutputDir } = require('./src/core/reporter');

// Command registry
const COMMANDS = {
    'index': {
        description: 'Submit URLs to Google Indexing API',
        legacy: true,
        run: () => require('./index.js') // Legacy standalone
    },
    'analyze': {
        description: 'GSC keyword analysis (Striking Distance, CTR, Cannibalization)',
        legacy: true,
        run: () => require('./gsc-analyzer.js') // Legacy standalone
    },
    'decay': {
        description: 'Content decay detection — tìm trang sụt traffic',
        module: () => require('./src/modules/content-decay')
    },
    'rank-compare': {
        description: 'Compare keyword rank & traffic for 24h period (yesterday vs day before)',
        module: () => require('./src/modules/rank-comparison')
    },
    'rank-compare-5days': {
        description: 'Compare keyword rank & traffic for 5-day periods (current 5 days vs previous 5 days)',
        module: () => require('./src/modules/rank-comparison-5days')
    },
    'rank-compare-7days': {
        description: 'Compare keyword rank & traffic for 7-day periods (current 7 days vs previous 7 days)',
        module: () => require('./src/modules/rank-comparison-7days')
    },
    'rank-compare-3days': {
        description: 'Compare keyword rank & traffic for 3-day periods (current 3 days vs previous 3 days)',
        module: () => require('./src/modules/rank-comparison-3days')
    },
    'top-pages': {
        description: 'Top pages performance dashboard',
        module: () => require('./src/modules/top-pages')
    },
    'geo': {
        description: 'Geo & device performance breakdown',
        module: () => require('./src/modules/geo-device')
    },
    'audit': {
        description: 'Technical SEO audit (crawl-based, 12+ rules)',
        module: () => require('./src/modules/technical-audit')
    },
    'sitemap': {
        description: 'Sitemap health check',
        module: () => require('./src/modules/sitemap-health')
    },
    'onpage-research': {
        description: 'On-page keyword research for a specific URL',
        module: () => require('./src/modules/onpage-research')
    },
    'outbound': {
        description: 'Outbound link audit — tìm broken external links',
        module: () => require('./src/modules/outbound-audit')
    },
    'internal': {
        description: 'Internal link graph analysis — tìm orphan pages',
        module: () => require('./src/modules/internal-links')
    },
    'mentions': {
        description: 'Brand mention monitoring — tìm unlinked mentions',
        module: () => require('./src/modules/brand-mentions')
    },
    'broken-links': {
        description: 'Broken link building scanner',
        module: () => require('./src/modules/broken-link-build')
    },
    'content-gap': {
        description: 'Competitor content gap analysis',
        module: () => require('./src/modules/content-gap')
    },
    'full-audit': {
        description: 'Run ALL analysis modules → unified report',
        module: () => require('./src/pipelines/full-audit')
    }
};

// Parse command
const command = process.argv[2];

if (!command || command === '--help' || command === '-h') {
    printUsage();
    process.exit(0);
}

if (!COMMANDS[command]) {
    console.error(`\n  ❌ Unknown command: "${command}"\n`);
    printUsage();
    process.exit(1);
}

const cmd = COMMANDS[command];

if (cmd.legacy) {
    // Legacy commands run themselves
    cmd.run();
} else {
    // New modular commands
    const config = buildConfig();

    // Set custom output dir if provided
    if (config.outputDir) {
        setOutputDir(config.outputDir);
        console.log(`  📂 Output directory: ${config.outputDir}`);
    }

    const mod = cmd.module();

    mod.run(config)
        .then(() => {
            console.log('\n  ✅ Done!\n');
        })
        .catch(err => {
            console.error(`\n  ❌ Error: ${err.message}\n`);
            process.exit(1);
        });
}

function printUsage() {
    console.log(`
╔══════════════════════════════════════════════════╗
║         🤖 Agent SEO Tool v2.0                  ║
║         Automated SEO Analysis Suite             ║
╚══════════════════════════════════════════════════╝

Usage: node cli.js <command> [options]

📡 DATA COLLECTION:
  index          ${COMMANDS['index'].description}
  analyze        ${COMMANDS['analyze'].description}

📊 ON-PAGE ANALYSIS:
  decay          ${COMMANDS['decay'].description}
  rank-compare   ${COMMANDS['rank-compare'].description}
  rank-compare-5days ${COMMANDS['rank-compare-5days'].description}
  rank-compare-3days ${COMMANDS['rank-compare-3days'].description}
  top-pages      ${COMMANDS['top-pages'].description}
  geo            ${COMMANDS['geo'].description}
  audit          ${COMMANDS['audit'].description}
  sitemap        ${COMMANDS['sitemap'].description}
  onpage-research ${COMMANDS['onpage-research'].description}

🔗 OFF-PAGE ANALYSIS:
  outbound       ${COMMANDS['outbound'].description}
  internal       ${COMMANDS['internal'].description}
  mentions       ${COMMANDS['mentions'].description}
  broken-links   ${COMMANDS['broken-links'].description}
  content-gap    ${COMMANDS['content-gap'].description}

⚙️ PIPELINE:
  full-audit     ${COMMANDS['full-audit'].description}

Common Options:
  --site URL          Target GSC property URL
  --sitemap URL       Sitemap URL
  --url URL           Target specific URL for single page audit & GSC Inspection
  --days N            Date range (default: 30)
  --max-pages N       Max pages to crawl (default: 200)
  --output-dir PATH   Export reports to custom dir (e.g. project's .agent/seo-reports/)
  --brand NAME        Brand name for mentions
  --cse-key KEY       Google Custom Search API key
  --cse-id ID         Google Custom Search Engine ID

Examples:
  node cli.js audit --site https://example.com/ --max-pages 50
  node cli.js audit --site https://example.com/ --url https://example.com/page-url
  node cli.js full-audit --site https://example.com/
  node cli.js audit --site https://example.com/ --output-dir D:\\Project\\my-site\\.agent\\seo-reports
`);
}
