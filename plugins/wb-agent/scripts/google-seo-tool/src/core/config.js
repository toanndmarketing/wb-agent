/**
 * Config Manager — CLI args + ENV + defaults
 * Centralized config cho tất cả modules
 */

/**
 * Parse CLI arguments (--key value format)
 * @returns {object} parsed args
 */
function parseArgs() {
    const args = {};
    const argv = process.argv.slice(2);
    argv.forEach((val, index, array) => {
        if (val.startsWith('--')) {
            const key = val.slice(2);
            const nextVal = array[index + 1];
            if (nextVal && !nextVal.startsWith('--')) {
                args[key] = nextVal;
            } else {
                args[key] = true;
            }
        }
    });
    return args;
}

/**
 * Lấy config value theo thứ tự: CLI arg → ENV → default
 */
function getConfig(cliArgs, key, envKey, defaultValue) {
    return cliArgs[key] || process.env[envKey] || defaultValue;
}

/**
 * Tạo config object đầy đủ cho các modules
 * @param {object} cliOverrides - Override từ CLI
 * @returns {object} config
 */
function buildConfig(cliOverrides = {}) {
    const args = { ...parseArgs(), ...cliOverrides };

    const siteUrl = getConfig(args, 'site', 'SITE_URL', null);
    const sitemapUrl = getConfig(args, 'sitemap', 'SITEMAP_URL', null);
    const targetUrl = getConfig(args, 'url', 'TARGET_URL', null);

    return {
        // Target site
        siteUrl,
        sitemapUrl,
        targetUrl,

        // GSC Analysis
        days: parseInt(getConfig(args, 'days', 'DAYS', '30'), 10),
        rowLimit: parseInt(getConfig(args, 'limit', 'ROW_LIMIT', '5000'), 10),
        ctrThreshold: parseFloat(getConfig(args, 'ctr-threshold', 'CTR_THRESHOLD', '0.03')),
        cannibalizationThreshold: parseFloat(getConfig(args, 'cannibal-threshold', 'CANNIBAL_THRESHOLD', '0.10')),
        strikingMin: parseInt(getConfig(args, 'striking-min', 'STRIKING_MIN', '8'), 10),
        strikingMax: parseInt(getConfig(args, 'striking-max', 'STRIKING_MAX', '20'), 10),
        minImpressions: parseInt(getConfig(args, 'min-impressions', 'MIN_IMPRESSIONS', '50'), 10),

        // Crawler
        crawlConcurrency: parseInt(getConfig(args, 'concurrency', 'CRAWL_CONCURRENCY', '5'), 10),
        crawlDelay: parseInt(getConfig(args, 'delay', 'CRAWL_DELAY', '200'), 10),
        maxPages: parseInt(getConfig(args, 'max-pages', 'MAX_PAGES', '200'), 10),
        userAgent: getConfig(args, 'user-agent', 'USER_AGENT', 'Mozilla/5.0 (compatible; AgentSEOTool/1.0)'),

        // Brand mentions
        brand: getConfig(args, 'brand', 'BRAND_NAME', null),
        cseApiKey: getConfig(args, 'cse-key', 'GOOGLE_CSE_API_KEY', null),
        cseEngineId: getConfig(args, 'cse-id', 'GOOGLE_CSE_ENGINE_ID', null),
        serperApiKey: getConfig(args, 'serper-key', 'SERPER_API_KEY', null),

        // Broken link building
        targetUrls: args['target-urls'] ? args['target-urls'].split(',') : [],

        // Content gap
        competitors: args['competitors'] ? args['competitors'].split(',') : [],
        keyword: getConfig(args, 'keyword', 'KEYWORD', null),

        // Output
        outputFormat: getConfig(args, 'format', 'OUTPUT_FORMAT', 'both'), // md, json, both
        outputDir: getConfig(args, 'output-dir', 'OUTPUT_DIR', null), // Custom output dir (e.g. project's .agent/seo-reports/)

        // Raw args
        _args: args
    };
}

/**
 * Extract domain name từ URL
 */
function extractDomain(url) {
    if (!url) return 'unknown';
    try {
        if (url.startsWith('sc-domain:')) return url.replace('sc-domain:', '');
        return new URL(url).hostname.replace('www.', '');
    } catch {
        return 'unknown';
    }
}

/**
 * Tính date range cho GSC API (trừ 2 ngày do data latency)
 */
function getDateRange(days) {
    const today = new Date();
    const endDate = new Date(today.getTime() - 2 * 24 * 60 * 60 * 1000);
    const startDate = new Date(today.getTime() - (days + 2) * 24 * 60 * 60 * 1000);
    return {
        startDate: startDate.toISOString().split('T')[0],
        endDate: endDate.toISOString().split('T')[0]
    };
}

module.exports = { parseArgs, getConfig, buildConfig, extractDomain, getDateRange };
