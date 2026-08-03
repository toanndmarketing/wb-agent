const fs = require('fs').promises;
const { existsSync, readFileSync } = require('fs');
const path = require('path');
const axios = require('axios');
const { google } = require('googleapis');

// Load environment variables from .env file natively if it exists
const dotenvPath = path.join(__dirname, '.env');
if (existsSync(dotenvPath)) {
    try {
        const envConfig = readFileSync(dotenvPath, 'utf8');
        envConfig.split(/\r?\n/).forEach(line => {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#')) {
                const [key, ...values] = trimmed.split('=');
                if (key) {
                    const val = values.join('=').trim().replace(/^['"]|['"]$/g, '');
                    process.env[key.trim()] = val;
                }
            }
        });
    } catch (e) {
        console.warn('[WARNING] Failed to parse .env file:', e.message);
    }
}

// Configuration
const SITEMAP_URL = process.env.SITEMAP_URL;
if (!SITEMAP_URL) {
    throw new Error('[CRITICAL] SITEMAP_URL environment variable is missing. Please configure it in your .env file.');
}
const KEY_FILE = process.env.GOOGLE_APPLICATION_CREDENTIALS || path.join(__dirname, 'service-account.json');

// Dynamically generate history file name based on sitemap domain
let domainName = 'default';
try {
    const sitemapUrlObj = new URL(SITEMAP_URL);
    domainName = sitemapUrlObj.hostname.replace('www.', '');
} catch (e) {
    console.error('[WARNING] Invalid Sitemap URL format, using default history file.');
}
const HISTORY_FILE = path.join(__dirname, `history-${domainName}.json`);
const MAX_URLS_PER_RUN = 100; // Google Indexing API default limit is 200/day


async function run() {
    console.log('==================================================');
    console.log(`Starting Google Indexing Tool - ${new Date().toISOString()}`);
    console.log(`Sitemap URL: ${SITEMAP_URL}`);
    console.log('==================================================');

    // 1. Check Service Account Key File
    if (!existsSync(KEY_FILE)) {
        throw new Error(`[CRITICAL] Google service account key file not found at: ${KEY_FILE}. Please download your service account JSON file and place it in the project root.`);
    }

    // 2. Load History Cache
    let history = {};
    if (existsSync(HISTORY_FILE)) {
        try {
            const data = await fs.readFile(HISTORY_FILE, 'utf8');
            history = JSON.parse(data);
            console.log(`Loaded ${Object.keys(history).length} URLs from history.`);
        } catch (e) {
            console.warn('[WARNING] Failed to parse history.json, resetting history.');
        }
    }

    // 3. Fetch Sitemap
    let sitemapData = '';
    try {
        console.log('Fetching sitemap...');
        const response = await axios.get(SITEMAP_URL);
        sitemapData = response.data;
        console.log('Sitemap fetched successfully.');
    } catch (e) {
        throw new Error(`[CRITICAL] Failed to fetch sitemap from ${SITEMAP_URL}: ${e.message}`);
    }

    // 4. Parse Sitemap URLs and LastModified
    // Format usually: <url><loc>...</loc><lastmod>...</lastmod></url>
    const urls = [];
    const locRegex = /<loc>(.*?)<\/loc>/;
    const lastmodRegex = /<lastmod>(.*?)<\/lastmod>/;

    if (sitemapData.includes('<sitemapindex')) {
        console.log('Detected sitemap index. Extracting sub-sitemaps...');
        const sitemapRegex = /<sitemap>([\s\S]*?)<\/sitemap>/g;
        const subSitemapUrls = [];
        let match;
        while ((match = sitemapRegex.exec(sitemapData)) !== null) {
            const locMatch = locRegex.exec(match[1]);
            if (locMatch) {
                subSitemapUrls.push(locMatch[1].trim());
            }
        }

        console.log(`Found ${subSitemapUrls.length} sub-sitemaps. Fetching in parallel (concurrency 5)...`);

        // Fetch sub-sitemaps in batches of 5 to avoid overloading
        const concurrency = 5;
        for (let i = 0; i < subSitemapUrls.length; i += concurrency) {
            const batch = subSitemapUrls.slice(i, i + concurrency);
            await Promise.all(batch.map(async (subUrl) => {
                console.log(`Fetching sub-sitemap: ${subUrl}`);
                try {
                    const subRes = await axios.get(subUrl);
                    const subData = subRes.data;
                    const urlRegex = /<url>([\s\S]*?)<\/url>/g;
                    let uMatch;
                    while ((uMatch = urlRegex.exec(subData)) !== null) {
                        const lMatch = locRegex.exec(uMatch[1]);
                        if (lMatch) {
                            const url = lMatch[1].trim();
                            const lmMatch = lastmodRegex.exec(uMatch[1]);
                            const lastmod = lmMatch ? lmMatch[1].trim() : new Date().toISOString();
                            urls.push({ url, lastmod });
                        }
                    }
                } catch (e) {
                    console.error(`Failed to fetch sub-sitemap ${subUrl}:`, e.message);
                }
            }));
        }
    } else {
        const urlRegex = /<url>([\s\S]*?)<\/url>/g;
        let match;
        while ((match = urlRegex.exec(sitemapData)) !== null) {
            const urlBlock = match[1];
            const locMatch = locRegex.exec(urlBlock);
            if (locMatch) {
                const url = locMatch[1].trim();
                const lastmodMatch = lastmodRegex.exec(urlBlock);
                const lastmod = lastmodMatch ? lastmodMatch[1].trim() : new Date().toISOString();
                urls.push({ url, lastmod });
            }
        }
    }

    console.log(`Found ${urls.length} URLs in total.`);

    if (urls.length === 0) {
        console.warn('[WARNING] No URLs extracted from sitemap. Check your sitemap format.');
        return;
    }

    // 5. Filter URLs that need indexing
    const urlsToSubmit = [];
    for (const item of urls) {
        const cached = history[item.url];
        // If not cached OR sitemap lastmod is newer than cached lastmod
        if (!cached || new Date(item.lastmod) > new Date(cached)) {
            urlsToSubmit.push(item);
        }
    }

    console.log(`Filtered: ${urlsToSubmit.length} URLs are new or updated.`);

    if (urlsToSubmit.length === 0) {
        console.log('All URLs are already indexed. Nothing to do!');
        return;
    }

    // Limit URLs submitted per run to avoid hitting Google quotas
    const batch = urlsToSubmit.slice(0, MAX_URLS_PER_RUN);
    console.log(`Submitting ${batch.length} URLs to Google Indexing API...`);

    // 6. Authenticate with Google
    let jwtClient;
    try {
        const keyContent = await fs.readFile(KEY_FILE, 'utf8');
        const keyData = JSON.parse(keyContent);
        jwtClient = new google.auth.JWT(
            keyData.client_email,
            null,
            keyData.private_key,
            ['https://www.googleapis.com/auth/indexing'],
            null
        );
        await jwtClient.authorize();
        console.log(`Authenticated as service account: ${keyData.client_email}`);
    } catch (e) {
        throw new Error(`[CRITICAL] Authentication failed: ${e.message}`);
    }

    // 7. Request Google Indexing for each URL
    const indexing = google.indexing({ version: 'v3', auth: jwtClient });
    let successCount = 0;
    let failCount = 0;

    for (const item of batch) {
        try {
            console.log(`Submitting: ${item.url}`);
            const res = await indexing.urlNotifications.publish({
                requestBody: {
                    url: item.url,
                    type: 'URL_UPDATED'
                }
            });
            
            if (res.status === 200) {
                console.log(` -> SUCCESS: Status ${res.data.urlNotificationMetadata?.latestUpdate?.notifyTime || 'OK'}`);
                // Update history cache
                history[item.url] = item.lastmod;
                successCount++;
            } else {
                console.warn(` -> WARNING: Unexpected status ${res.status}`);
                failCount++;
            }
        } catch (e) {
            console.error(` -> FAILED: ${e.message}`);
            // Check if quota exceeded
            if (e.message && e.message.includes('Quota exceeded')) {
                console.error('[CRITICAL] Google Indexing API Quota exceeded. Stopping execution.');
                break;
            }
            failCount++;
        }
        
        // Anti-throttling delay (100ms)
        await new Promise(resolve => setTimeout(resolve, 100));
    }

    // 8. Save updated history
    try {
        await fs.writeFile(HISTORY_FILE, JSON.stringify(history, null, 2), 'utf8');
        console.log(`Saved submission history to ${path.basename(HISTORY_FILE)}`);
    } catch (e) {
        console.error(`[ERROR] Failed to save ${path.basename(HISTORY_FILE)}:`, e.message);
    }

    console.log('==================================================');
    console.log(`Execution completed. Success: ${successCount}, Failed: ${failCount}`);
    console.log('==================================================');
}

run().catch(err => {
    console.error('Unhandled error in runtime:', err);
    process.exit(1);
});
