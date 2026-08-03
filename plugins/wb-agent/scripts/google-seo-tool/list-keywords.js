const { getSearchConsoleClient } = require('./src/core/auth');
const { getDateRange } = require('./src/core/config');

async function main() {
    try {
        const { searchconsole } = await getSearchConsoleClient();
        const { startDate, endDate } = getDateRange(30);
        console.log(`Querying GSC for sc-domain:tastehi.com between ${startDate} and ${endDate}...`);
        
        const gscRes = await searchconsole.searchanalytics.query({
            siteUrl: 'sc-domain:tastehi.com',
            requestBody: {
                startDate,
                endDate,
                dimensions: ['query', 'page'],
                rowLimit: 100
            }
        });

        const rows = gscRes.data.rows || [];
        console.log(`Found ${rows.length} rows`);
        if (rows.length > 0) {
            console.log('Top 20 rows:');
            const formatted = rows.slice(0, 20).map(r => ({
                query: r.keys[0],
                page: r.keys[1],
                clicks: r.clicks,
                impressions: r.impressions,
                position: r.position
            }));
            console.log(JSON.stringify(formatted, null, 2));
        }
    } catch (err) {
        console.error('Error:', err.message);
    }
}
main();
