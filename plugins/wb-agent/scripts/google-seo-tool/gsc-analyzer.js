const fs = require('fs').promises;
const { existsSync, readFileSync } = require('fs');
const path = require('path');
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
const KEY_FILE = process.env.GOOGLE_APPLICATION_CREDENTIALS || path.join(__dirname, 'service-account.json');
const REPORTS_DIR = path.join(__dirname, 'reports');

// Parse Command Line Arguments
// CLI: node gsc-analyzer.js --site https://toantuvi.com/ --days 30 --limit 5000 --ctr-threshold 0.03 --cannibal-threshold 0.10
const args = {};
process.argv.slice(2).forEach((val, index, array) => {
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

const SITE_URL = args.site || process.env.SITE_URL;
if (!SITE_URL) {
    throw new Error('[CRITICAL] SITE_URL is missing. Please provide it via --site argument or SITE_URL environment variable.');
}
const DAYS = parseInt(args.days || process.env.DAYS || '30', 10);
const ROW_LIMIT = parseInt(args.limit || process.env.ROW_LIMIT || '5000', 10);

// Advanced analysis configurations (with fallback/default values)
const CTR_THRESHOLD = parseFloat(args['ctr-threshold'] || process.env.CTR_THRESHOLD || '0.03');
const CANNIBAL_THRESHOLD = parseFloat(args['cannibal-threshold'] || process.env.CANNIBAL_THRESHOLD || '0.10');
const STRIKING_MIN = parseInt(args['striking-min'] || process.env.STRIKING_MIN || '8', 10);
const STRIKING_MAX = parseInt(args['striking-max'] || process.env.STRIKING_MAX || '20', 10);


async function run() {
    console.log('==================================================');
    console.log(`Starting Google Search Console Analyzer`);
    console.log(`Target Site: ${SITE_URL}`);
    console.log(`Date Range: Last ${DAYS} Days`);
    console.log(`Row Limit: ${ROW_LIMIT}`);
    console.log(`Analysis Configs:`);
    console.log(` - Striking Distance Range: ${STRIKING_MIN} - ${STRIKING_MAX}`);
    console.log(` - Underperforming CTR Limit: < ${(CTR_THRESHOLD * 100).toFixed(1)}%`);
    console.log(` - Cannibalization Threshold: >= ${(CANNIBAL_THRESHOLD * 100).toFixed(1)}%`);
    console.log('==================================================');

    // Ensure reports directory exists
    if (!existsSync(REPORTS_DIR)) {
        await fs.mkdir(REPORTS_DIR, { recursive: true });
    }

    // 1. Authenticate with Service Account
    if (!existsSync(KEY_FILE)) {
        throw new Error(`[CRITICAL] Google service account key file not found at: ${KEY_FILE}. Please download your service account JSON file and place it in the project root.`);
    }

    let jwtClient;
    try {
        const keyContent = await fs.readFile(KEY_FILE, 'utf8');
        const keyData = JSON.parse(keyContent);
        jwtClient = new google.auth.JWT(
            keyData.client_email,
            null,
            keyData.private_key,
            ['https://www.googleapis.com/auth/webmasters.readonly'],
            null
        );
        await jwtClient.authorize();
        console.log(`[SUCCESS] Authenticated as Service Account: ${keyData.client_email}`);
    } catch (e) {
        throw new Error(`[CRITICAL] Authentication failed: ${e.message}`);
    }

    const searchconsole = google.searchconsole({ version: 'v1', auth: jwtClient });

    // 2. Calculate Date Range (ending 2 days ago due to GSC data latency)
    const today = new Date();
    const endDate = new Date(today.getTime() - 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    const startDate = new Date(today.getTime() - (DAYS + 2) * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    
    console.log(`Query range: ${startDate} to ${endDate}`);

    // 3. Fetch Search Analytics Data (Query + Page level)
    let rows = [];
    try {
        console.log('Fetching search analytics data from GSC API...');
        const res = await searchconsole.searchanalytics.query({
            siteUrl: SITE_URL,
            requestBody: {
                startDate: startDate,
                endDate: endDate,
                dimensions: ['query', 'page'],
                rowLimit: ROW_LIMIT
            }
        });

        rows = res.data.rows || [];
        console.log(`[SUCCESS] Retrieved ${rows.length} rows of query-page data.`);
    } catch (e) {
        throw new Error(`[CRITICAL] Failed to fetch GSC data for ${SITE_URL}: ${e.message}. Ensure the Service Account has been added as Owner/Full User to this property.`);
    }

    if (rows.length === 0) {
        console.log('[-] No data returned from GSC. Exiting.');
        return;
    }

    // Parse domain name for file naming
    let domainName = 'site';
    try {
        if (SITE_URL.startsWith('sc-domain:')) {
            domainName = SITE_URL.replace('sc-domain:', '');
        } else {
            domainName = new URL(SITE_URL).hostname.replace('www.', '');
        }
    } catch (e) {}

    // 4. Transform Data
    const dataset = rows.map(row => ({
        query: row.keys[0],
        page: row.keys[1],
        clicks: row.clicks,
        impressions: row.impressions,
        ctr: row.ctr, // represented as float, e.g. 0.12 = 12%
        position: row.position
    }));

    // 5. Run SEO Audits / Analyses
    console.log('\nRunning SEO analysis models...');
    const strikingDistance = analyzeStrikingDistance(dataset);
    const lowCTR = analyzeLowCTR(dataset);
    const cannibalization = analyzeCannibalization(dataset);

    console.log(` -> Found ${strikingDistance.length} Striking Distance Keywords (Rank ${STRIKING_MIN}-${STRIKING_MAX} with high impressions).`);
    console.log(` -> Found ${lowCTR.length} Opportunity Pages (Rank 1-5 with CTR < ${(CTR_THRESHOLD * 100).toFixed(1)}%).`);
    console.log(` -> Found ${cannibalization.length} cases of Keyword Cannibalization.`);

    // 6. Generate Reports
    const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
    const reportMdFile = path.join(REPORTS_DIR, `report-${domainName}-${timestamp}.md`);
    const reportJsonFile = path.join(REPORTS_DIR, `data-${domainName}-${timestamp}.json`);

    // Output JSON data
    const outputData = {
        meta: {
            siteUrl: SITE_URL,
            startDate: startDate,
            endDate: endDate,
            days: DAYS,
            generatedAt: new Date().toISOString(),
            totalRowsAnalyzed: dataset.length,
            configs: {
                ctrThreshold: CTR_THRESHOLD,
                cannibalizationThreshold: CANNIBAL_THRESHOLD,
                strikingMin: STRIKING_MIN,
                strikingMax: STRIKING_MAX
            }
        },
        analyses: {
            strikingDistance: strikingDistance,
            lowCTR: lowCTR,
            cannibalization: cannibalization
        }
    };
    
    await fs.writeFile(reportJsonFile, JSON.stringify(outputData, null, 2), 'utf8');
    console.log(`\n[SUCCESS] Detailed JSON data saved to: ${path.basename(reportJsonFile)}`);

    // Build Markdown Report
    const mdContent = buildMarkdownReport(outputData);
    await fs.writeFile(reportMdFile, mdContent, 'utf8');
    console.log(`[SUCCESS] Beautiful Markdown SEO audit report saved to: ${path.basename(reportMdFile)}`);
    console.log('==================================================');
}

// Model 1: Striking Distance Keywords (Rank STRIKING_MIN to STRIKING_MAX, Clicks low, Impressions high)
function analyzeStrikingDistance(data) {
    return data
        .filter(item => item.position >= STRIKING_MIN && item.position <= STRIKING_MAX)
        .sort((a, b) => b.impressions - a.impressions)
        .slice(0, 50); // Top 50 striking distance opportunities
}

// Model 2: Underperforming CTR (Rank 1-5 but CTR < CTR_THRESHOLD)
function analyzeLowCTR(data) {
    return data
        .filter(item => item.position >= 1 && item.position <= 5 && item.ctr < CTR_THRESHOLD && item.impressions > 100)
        .sort((a, b) => b.impressions - a.impressions)
        .slice(0, 50);
}

// Model 3: Keyword Cannibalization
function analyzeCannibalization(data) {
    const queryMap = {};
    data.forEach(item => {
        if (!queryMap[item.query]) {
            queryMap[item.query] = [];
        }
        queryMap[item.query].push(item);
    });

    const results = [];
    Object.keys(queryMap).forEach(query => {
        const pages = queryMap[query];
        if (pages.length >= 2) {
            // Calculate total impressions for this query
            const totalImpressions = pages.reduce((sum, p) => sum + p.impressions, 0);
            
            // Filter pages that get at least CANNIBAL_THRESHOLD of the query's total impressions
            const competingPages = pages.filter(p => (p.impressions / totalImpressions) >= CANNIBAL_THRESHOLD);
            
            if (competingPages.length >= 2) {
                // Sort by impressions descending
                competingPages.sort((a, b) => b.impressions - a.impressions);
                results.push({
                    query: query,
                    totalImpressions: totalImpressions,
                    pages: competingPages.map(p => ({
                        page: p.page,
                        clicks: p.clicks,
                        impressions: p.impressions,
                        ctr: p.ctr,
                        position: p.position,
                        percentage: ((p.impressions / totalImpressions) * 100).toFixed(1) + '%'
                    }))
                });
            }
        }
    });

    // Sort by total impressions descending
    return results.sort((a, b) => b.totalImpressions - a.totalImpressions).slice(0, 30);
}

function buildMarkdownReport(data) {
    const { meta, analyses } = data;
    
    let md = `# BÁO CÁO PHÂN TÍCH SEO GOOGLE SEARCH CONSOLE\n\n`;
    md += `## 📋 Thông Tin Dự Án\n`;
    md += `- **Website:** [${meta.siteUrl}](${meta.siteUrl})\n`;
    md += `- **Khoảng thời gian phân tích:** ${meta.startDate} đến ${meta.endDate} (${meta.days} ngày)\n`;
    md += `- **Số dòng dữ liệu đã phân tích:** ${meta.totalRowsAnalyzed} (Query + Page combinations)\n`;
    md += `- **Ngày xuất báo cáo:** ${new Date(meta.generatedAt).toLocaleString('vi-VN')}\n\n`;

    // 1. Striking Distance
    md += `## 🚀 1. Từ Khóa Tiềm Năng Trang 2 (Striking Distance Keywords)\n`;
    md += `> Các từ khóa đang xếp hạng từ vị trí **${meta.configs.strikingMin} - ${meta.configs.strikingMax}** có lượt hiển thị (Impressions) cao nhưng Click chuột còn thấp. Đây là cơ hội tối ưu nhanh nhất để kéo Traffic lên trang 1.\n\n`;
    md += `| Vị trí trung bình | Từ Khóa | Trang Đích | Lượt hiển thị | Clicks | CTR | Đề xuất hành động |\n`;
    md += `| :---: | :--- | :--- | :---: | :---: | :---: | :--- |\n`;
    
    if (analyses.strikingDistance.length === 0) {
        md += `| - | Không tìm thấy | - | - | - | - | - |\n`;
    } else {
        analyses.strikingDistance.forEach(item => {
            const shortPage = item.page.replace(meta.siteUrl, '/');
            const ctrPercent = (item.ctr * 100).toFixed(1) + '%';
            md += `| **${item.position.toFixed(1)}** | \`${item.query}\` | [${shortPage}](${item.page}) | ${item.impressions} | ${item.clicks} | ${ctrPercent} | Thêm content, đi link nội bộ với anchor text chính xác |\n`;
        });
    }
    md += `\n`;

    // 2. Underperforming CTR
    md += `## 🎯 2. Trang Hiển Thị Tốt Nhưng CTR Thấp (CTR Optimization)\n`;
    md += `> Các từ khóa đã lọt **Top 1 - 5** nhưng CTR rất thấp (< ${(meta.configs.ctrThreshold * 100).toFixed(1)}%). Vấn đề nằm ở Title hoặc Meta Description chưa đủ hấp dẫn để người dùng click.\n\n`;
    md += `| Vị trí | Từ Khóa | Trang Đích | Lượt hiển thị | Clicks | CTR hiện tại | Đề xuất hành động |\n`;
    md += `| :---: | :--- | :--- | :---: | :---: | :---: | :--- |\n`;

    if (analyses.lowCTR.length === 0) {
        md += `| - | Không tìm thấy | - | - | - | - | - |\n`;
    } else {
        analyses.lowCTR.forEach(item => {
            const shortPage = item.page.replace(meta.siteUrl, '/');
            const ctrPercent = (item.ctr * 100).toFixed(1) + '%';
            md += `| **${item.position.toFixed(1)}** | \`${item.query}\` | [${shortPage}](${item.page}) | ${item.impressions} | ${item.clicks} | ${ctrPercent} | Viết lại Title/Meta cuốn hút hơn, chèn thêm CTR Modifiers |\n`;
        });
    }
    md += `\n`;

    // 3. Cannibalization
    md += `## ⚔️ 3. Hiện tượng Ăn Thịt Từ Khóa (Keyword Cannibalization)\n`;
    md += `> Xảy ra khi có từ 2 trang trở lên trên website cùng cạnh tranh thứ hạng cho cùng một từ khóa chính với tỷ lệ hiển thị >= ${(meta.configs.cannibalizationThreshold * 100).toFixed(0)}%, làm phân mảnh sức mạnh SEO.\n\n`;

    if (analyses.cannibalization.length === 0) {
        md += `*Chúc mừng! Không phát hiện hiện tượng ăn thịt từ khóa nghiêm trọng.*\n\n`;
    } else {
        analyses.cannibalization.forEach((item, index) => {
            md += `### ${index + 1}. Từ khóa: \`${item.query}\` (Tổng hiển thị: ${item.totalImpressions})\n`;
            md += `Các trang đang cạnh tranh nhau:\n`;
            md += `| URL trang đích | Clicks | Impressions | CTR | Vị trí | Tỷ lệ phân bổ |\n`;
            md += `| :--- | :---: | :---: | :---: | :---: | :---: |\n`;
            item.pages.forEach(p => {
                const shortPage = p.page.replace(meta.siteUrl, '/');
                md += `| [${shortPage}](${p.page}) | ${p.clicks} | ${p.impressions} | ${p.ctr} | ${p.position.toFixed(1)} | **${p.percentage}** |\n`;
            });
            md += `*👉 **Đề xuất:** Chọn trang tốt nhất làm trang SEO chính (Pillar Page), chuyển hướng 301 hoặc đặt canonical từ các trang phụ về trang chính, hoặc viết lại nội dung các trang phụ để tập trung vào từ khóa ngách khác.*\n\n`;
        });
    }

    return md;
}

run().catch(err => {
    console.error('Unhandled error in script execution:', err);
    process.exit(1);
});
