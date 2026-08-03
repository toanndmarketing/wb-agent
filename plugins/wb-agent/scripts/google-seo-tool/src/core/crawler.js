/**
 * Crawler Engine — HTTP crawler với cheerio HTML parser
 * Dùng cho tất cả modules crawl-based (technical audit, outbound links, internal links...)
 */
const axios = require('axios');
const cheerio = require('cheerio');

/**
 * Fetch + parse HTML page
 * @param {string} url
 * @param {object} options
 * @returns {Promise<{$: CheerioAPI, html: string, statusCode: number, headers: object, url: string}>}
 */
async function fetchPage(url, options = {}) {
    const {
        userAgent = 'Mozilla/5.0 (compatible; AgentSEOTool/1.0)',
        timeout = 15000,
        maxRedirects = 5
    } = options;

    const response = await axios.get(url, {
        headers: {
            'User-Agent': userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        },
        timeout,
        maxRedirects,
        validateStatus: () => true // Accept all status codes
    });

    const $ = cheerio.load(response.data || '');
    return {
        $,
        html: response.data || '',
        statusCode: response.status,
        headers: response.headers,
        url: response.request?.res?.responseUrl || url
    };
}

/**
 * HEAD request — chỉ check status code, không download body
 * @param {string} url
 * @returns {Promise<{statusCode: number, redirectUrl: string|null}>}
 */
async function headCheck(url, options = {}) {
    const { timeout = 10000, userAgent = 'Mozilla/5.0 (compatible; AgentSEOTool/1.0)' } = options;
    try {
        const response = await axios.head(url, {
            headers: { 'User-Agent': userAgent },
            timeout,
            maxRedirects: 5,
            validateStatus: () => true
        });
        return {
            statusCode: response.status,
            redirectUrl: response.headers.location || null
        };
    } catch (e) {
        if (e.code === 'ECONNABORTED') return { statusCode: 408, redirectUrl: null };
        if (e.code === 'ENOTFOUND') return { statusCode: 0, redirectUrl: null };
        // Fallback sang GET nếu HEAD bị server reject
        try {
            const response = await axios.get(url, {
                headers: { 'User-Agent': userAgent },
                timeout,
                maxRedirects: 5,
                validateStatus: () => true,
                // Chỉ download headers, cancel ngay khi nhận được
                maxContentLength: 1024
            });
            return { statusCode: response.status, redirectUrl: null };
        } catch (e2) {
            return { statusCode: 0, redirectUrl: null };
        }
    }
}

/**
 * Parse sitemap XML — hỗ trợ cả sitemap index và sitemap đơn
 * @param {string} sitemapUrl
 * @returns {Promise<Array<{url: string, lastmod: string}>>}
 */
async function parseSitemap(sitemapUrl, options = {}) {
    const { concurrency = 5 } = options;
    const response = await axios.get(sitemapUrl, {
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; AgentSEOTool/1.0)' },
        timeout: 30000
    });

    const sitemapData = response.data;
    const urls = [];
    const locRegex = /<loc>(.*?)<\/loc>/;
    const lastmodRegex = /<lastmod>(.*?)<\/lastmod>/;

    if (sitemapData.includes('<sitemapindex')) {
        // Sitemap index — fetch sub-sitemaps
        const sitemapRegex = /<sitemap>([\s\S]*?)<\/sitemap>/g;
        const subUrls = [];
        let match;
        while ((match = sitemapRegex.exec(sitemapData)) !== null) {
            const locMatch = locRegex.exec(match[1]);
            if (locMatch) subUrls.push(locMatch[1].trim());
        }

        for (let i = 0; i < subUrls.length; i += concurrency) {
            const batch = subUrls.slice(i, i + concurrency);
            await Promise.all(batch.map(async (subUrl) => {
                try {
                    const subRes = await axios.get(subUrl, { timeout: 30000 });
                    const urlRegex = /<url>([\s\S]*?)<\/url>/g;
                    let uMatch;
                    while ((uMatch = urlRegex.exec(subRes.data)) !== null) {
                        const lMatch = locRegex.exec(uMatch[1]);
                        if (lMatch) {
                            const lmMatch = lastmodRegex.exec(uMatch[1]);
                            urls.push({
                                url: lMatch[1].trim(),
                                lastmod: lmMatch ? lmMatch[1].trim() : new Date().toISOString()
                            });
                        }
                    }
                } catch (e) {
                    console.error(`  [WARN] Failed to fetch sub-sitemap ${subUrl}: ${e.message}`);
                }
            }));
        }
    } else {
        // Single sitemap
        const urlRegex = /<url>([\s\S]*?)<\/url>/g;
        let match;
        while ((match = urlRegex.exec(sitemapData)) !== null) {
            const locMatch = locRegex.exec(match[1]);
            if (locMatch) {
                const lmMatch = lastmodRegex.exec(match[1]);
                urls.push({
                    url: locMatch[1].trim(),
                    lastmod: lmMatch ? lmMatch[1].trim() : new Date().toISOString()
                });
            }
        }
    }

    return urls;
}

/**
 * Batch process URLs với concurrency control
 * @param {string[]} urls
 * @param {Function} processor - async (url) => result
 * @param {object} options
 * @returns {Promise<Array>}
 */
async function batchProcess(urls, processor, options = {}) {
    const { concurrency = 5, delay = 200, onProgress = null } = options;
    const results = [];
    let completed = 0;

    for (let i = 0; i < urls.length; i += concurrency) {
        const batch = urls.slice(i, i + concurrency);
        const batchResults = await Promise.all(
            batch.map(async (url) => {
                try {
                    return await processor(url);
                } catch (e) {
                    return { url, error: e.message };
                }
            })
        );
        results.push(...batchResults);
        completed += batch.length;
        if (onProgress) onProgress(completed, urls.length);
        if (delay > 0 && i + concurrency < urls.length) {
            await new Promise(r => setTimeout(r, delay));
        }
    }

    return results;
}

/**
 * Extract tất cả links từ HTML
 * @param {CheerioAPI} $
 * @param {string} baseUrl
 * @returns {{internal: Array, external: Array}}
 */
function extractLinks($, baseUrl) {
    const base = new URL(baseUrl);
    const internal = [];
    const external = [];

    $('a[href]').each((_, el) => {
        const href = $(el).attr('href');
        if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) return;

        try {
            const resolved = new URL(href, baseUrl);
            const rel = $(el).attr('rel') || '';
            const text = $(el).text().trim().substring(0, 100);
            const linkData = {
                href: resolved.href,
                text,
                rel,
                nofollow: rel.includes('nofollow'),
                sponsored: rel.includes('sponsored'),
                ugc: rel.includes('ugc')
            };

            if (resolved.hostname === base.hostname) {
                internal.push(linkData);
            } else {
                external.push(linkData);
            }
        } catch {
            // Skip invalid URLs
        }
    });

    return { internal, external };
}

module.exports = { fetchPage, headCheck, parseSitemap, batchProcess, extractLinks };
