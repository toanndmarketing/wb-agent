/**
 * ENV Loader — Load .env file vào process.env
 * Extracted từ pattern chung của index.js, gsc-analyzer.js, auto-add-owner.js
 */
const { existsSync, readFileSync } = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..', '..');

function loadEnv() {
    const dotenvPath = path.join(ROOT_DIR, '.env');
    if (!existsSync(dotenvPath)) return;

    try {
        const envConfig = readFileSync(dotenvPath, 'utf8');
        envConfig.split(/\r?\n/).forEach(line => {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#')) {
                const [key, ...values] = trimmed.split('=');
                if (key) {
                    const val = values.join('=').trim().replace(/^['"]|['"]$/g, '');
                    if (!process.env[key.trim()]) {
                        process.env[key.trim()] = val;
                    }
                }
            }
        });
    } catch (e) {
        console.warn('[WARNING] Failed to parse .env file:', e.message);
    }
}

module.exports = { loadEnv, ROOT_DIR };
