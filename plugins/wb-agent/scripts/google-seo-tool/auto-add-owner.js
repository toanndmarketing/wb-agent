const fs = require('fs').promises;
const { existsSync, readFileSync } = require('fs');
const path = require('path');
const readline = require('readline');
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

// Path configs
const OAUTH_CREDENTIALS_FILE = path.join(__dirname, 'oauth-credentials.json');
const TOKENS_FILE = path.join(__dirname, 'oauth-tokens.json');
const SERVICE_ACCOUNT_FILE = path.join(__dirname, 'service-account.json');

// Scopes required for Search Console management
const SCOPES = ['https://www.googleapis.com/auth/webmasters'];

async function run() {
    console.log('==================================================');
    console.log('Google Search Console Auto Owner Assigner');
    console.log('==================================================');

    // 1. Get Service Account Email
    if (!existsSync(SERVICE_ACCOUNT_FILE)) {
        throw new Error(`[CRITICAL] service-account.json not found at ${SERVICE_ACCOUNT_FILE}. Please place your service account JSON file in the project root.`);
    }
    const serviceAccountContent = await fs.readFile(SERVICE_ACCOUNT_FILE, 'utf8');
    const serviceAccountData = JSON.parse(serviceAccountContent);
    const targetEmail = serviceAccountData.client_email;
    if (!targetEmail) {
        throw new Error('[CRITICAL] Could not find client_email in service-account.json. Please check your service account key file.');
    }
    console.log(`Target Service Account Email to add: ${targetEmail}\n`);

    // 2. Check OAuth Credentials
    if (!existsSync(OAUTH_CREDENTIALS_FILE)) {
        throw new Error(`[CRITICAL] oauth-credentials.json not found at ${OAUTH_CREDENTIALS_FILE}. To run this tool, you need OAuth2 credentials from Google Cloud Console (APIs & Services > Credentials > OAuth client ID) placed in the project root.`);
    }

    const credentialsContent = await fs.readFile(OAUTH_CREDENTIALS_FILE, 'utf8');
    const credentials = JSON.parse(credentialsContent);
    const clientType = credentials.installed ? 'installed' : 'web';
    const { client_id, client_secret, redirect_uris } = credentials[clientType] || credentials.web || {};
    
    if (!client_id || !client_secret) {
        throw new Error('[CRITICAL] Invalid oauth-credentials.json structure. Missing client_id or client_secret.');
    }

    const redirectUri = redirect_uris ? redirect_uris[0] : 'urn:ietf:wg:oauth:2.0:oob';
    const oauth2Client = new google.auth.OAuth2(client_id, client_secret, redirectUri);

    // 3. Authenticate User
    if (existsSync(TOKENS_FILE)) {
        const tokensContent = await fs.readFile(TOKENS_FILE, 'utf8');
        const tokens = JSON.parse(tokensContent);
        oauth2Client.setCredentials(tokens);
        console.log('Loaded existing authentication tokens.');
    } else {
        const authUrl = oauth2Client.generateAuthUrl({
            access_type: 'offline',
            scope: SCOPES,
            prompt: 'consent'
        });

        console.log('Authorize this app by visiting this URL:');
        console.log('\x1b[36m%s\x1b[0m', authUrl);
        console.log('');

        const code = await askQuestion('Enter the code from that page here: ');
        try {
            const { tokens } = await oauth2Client.getToken(code);
            oauth2Client.setCredentials(tokens);
            await fs.writeFile(TOKENS_FILE, JSON.stringify(tokens, null, 2), 'utf8');
            console.log('Tokens acquired and saved successfully.');
        } catch (e) {
            throw new Error(`[CRITICAL] Failed to get tokens: ${e.message}`);
        }
    }

    // 4. List Search Console sites
    const webmasters = google.webmasters({ version: 'v3', auth: oauth2Client });
    let sites = [];
    try {
        console.log('Retrieving your Search Console sites...');
        const response = await webmasters.sites.list();
        sites = response.data.siteEntry || [];
        console.log(`Found ${sites.length} sites in your account.`);
    } catch (e) {
        throw new Error(`[CRITICAL] Failed to list sites: ${e.message}`);
    }

    if (sites.length === 0) {
        console.log('No sites found. Make sure your account has verified properties.');
        return;
    }

    // 5. Add Service Account as Owner to all sites
    console.log('\nStarting to assign OWNER permission to all sites:');
    let successCount = 0;
    let failCount = 0;

    for (const site of sites) {
        const siteUrl = site.siteUrl;
        console.log(`Processing: ${siteUrl}`);
        
        try {
            await webmasters.permissions.insert({
                siteUrl: siteUrl,
                requestBody: {
                    email: targetEmail,
                    role: 'owner'
                }
            });
            console.log(`  -> \x1b[32mSUCCESS\x1b[0m: Added ${targetEmail} as Owner.`);
            successCount++;
        } catch (e) {
            console.error(`  -> \x1b[31mFAILED\x1b[0m: ${e.message}`);
            failCount++;
        }
        // Small delay to avoid API rate limits
        await new Promise(resolve => setTimeout(resolve, 300));
    }

    console.log('==================================================');
    console.log(`Done! Success: ${successCount}, Failed: ${failCount}`);
    console.log('==================================================');
}

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }));
}

run().catch(err => {
    console.error('Unhandled error:', err);
    process.exit(1);
});
