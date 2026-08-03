const { getSearchConsoleClient } = require('./src/core/auth');

async function main() {
    try {
        const { searchconsole, email } = await getSearchConsoleClient();
        console.log('Authenticated email:', email);
        const res = await searchconsole.sites.list();
        console.log('Verified sites on Search Console:');
        console.log(JSON.stringify(res.data.siteEntry, null, 2));
    } catch (err) {
        console.error('Error listing sites:', err.message);
    }
}

main();
