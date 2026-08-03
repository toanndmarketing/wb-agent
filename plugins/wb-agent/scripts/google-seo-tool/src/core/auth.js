/**
 * Auth Manager — Google Service Account Authentication
 * Shared across tất cả modules cần Google API
 */
const fs = require('fs').promises;
const { existsSync } = require('fs');
const path = require('path');
const { google } = require('googleapis');
const { ROOT_DIR } = require('./env');

const SCOPES = {
    indexing: ['https://www.googleapis.com/auth/indexing'],
    searchconsole: ['https://www.googleapis.com/auth/webmasters.readonly'],
    webmasters: ['https://www.googleapis.com/auth/webmasters']
};

/**
 * Tạo JWT client đã authenticated
 * @param {'indexing'|'searchconsole'|'webmasters'} scope
 * @returns {Promise<{jwtClient: object, email: string}>}
 */
async function authenticate(scope = 'searchconsole') {
    const keyFile = process.env.GOOGLE_APPLICATION_CREDENTIALS || path.join(ROOT_DIR, 'service-account.json');

    if (!existsSync(keyFile)) {
        throw new Error(`[CRITICAL] Service account key file not found at: ${keyFile}`);
    }

    const keyContent = await fs.readFile(keyFile, 'utf8');
    const keyData = JSON.parse(keyContent);

    const jwtClient = new google.auth.JWT(
        keyData.client_email,
        null,
        keyData.private_key,
        SCOPES[scope] || SCOPES.searchconsole,
        null
    );

    await jwtClient.authorize();
    return { jwtClient, email: keyData.client_email };
}

/**
 * Tạo Search Console API client đã authenticated
 * @returns {Promise<{searchconsole: object, email: string}>}
 */
async function getSearchConsoleClient() {
    const { jwtClient, email } = await authenticate('searchconsole');
    const searchconsole = google.searchconsole({ version: 'v1', auth: jwtClient });
    return { searchconsole, email };
}

/**
 * Tạo Indexing API client đã authenticated
 * @returns {Promise<{indexing: object, email: string}>}
 */
async function getIndexingClient() {
    const { jwtClient, email } = await authenticate('indexing');
    const indexing = google.indexing({ version: 'v3', auth: jwtClient });
    return { indexing, email };
}

module.exports = { authenticate, getSearchConsoleClient, getIndexingClient };
