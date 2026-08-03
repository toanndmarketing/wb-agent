const axios = require('axios');
const { loadEnv } = require('./src/core/env');
loadEnv();

async function testSerper() {
    const serperKey = process.env.SERPER_API_KEY;
    if (!serperKey) {
        console.log('\n--- SERPER.DEV TEST: Skipped (SERPER_API_KEY is not defined in .env) ---');
        return;
    }

    console.log('\n--- SERPER.DEV TEST ---');
    console.log('Testing Serper.dev with Key:', `${serperKey.substring(0, 10)}...`);
    try {
        const res = await axios.post('https://google.serper.dev/search', {
            q: 'két sắt mini',
            num: 3
        }, {
            headers: {
                'X-API-KEY': serperKey,
                'Content-Type': 'application/json'
            },
            timeout: 10000
        });
        if (res.data && res.data.organic) {
            console.log('SUCCESS! Retrieved organic results:', res.data.organic.length);
            console.log('Sample result:', res.data.organic[0].title, '-', res.data.organic[0].link);
        } else {
            console.log('FAILED! No organic results found in response:', res.data);
        }
    } catch (err) {
        console.error('ERROR status:', err.response ? err.response.status : err.message);
        if (err.response && err.response.data) {
            console.error('Detailed Error:', JSON.stringify(err.response.data, null, 2));
        }
    }
}

async function testGoogleCSE() {
    const key = process.env.GOOGLE_CSE_API_KEY;
    const cx = process.env.GOOGLE_CSE_ENGINE_ID;
    
    if (!key || !cx) {
        console.log('\n--- GOOGLE CUSTOM SEARCH TEST: Skipped (GOOGLE_CSE_API_KEY or GOOGLE_CSE_ENGINE_ID is not defined) ---');
        return;
    }

    console.log('\n--- GOOGLE CUSTOM SEARCH TEST ---');
    console.log('Testing CSE with Key:', `${key.substring(0, 10)}...`);
    console.log('Testing CSE with CX:', cx);
    
    try {
        const res = await axios.get('https://www.googleapis.com/customsearch/v1', {
            params: {
                key,
                cx,
                q: 'két sắt mini',
                num: 1
            },
            timeout: 10000
        });
        console.log('SUCCESS! Results:', res.data.searchInformation);
    } catch (err) {
        console.error('ERROR status:', err.response ? err.response.status : err.message);
        if (err.response && err.response.data) {
            console.error('Detailed Error:', JSON.stringify(err.response.data, null, 2));
        }
    }
}

async function main() {
    await testSerper();
    await testGoogleCSE();
}

main();
