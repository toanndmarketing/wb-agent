/**
 * Module: Rank Comparison 3 Days (3-day comparison)
 * So sánh hiệu suất từ khóa & rank của 3 ngày gần nhất có dữ liệu (Period A) so với 3 ngày trước đó (Period B).
 * Giúp phát hiện sự thay đổi thứ hạng ổn định hơn và tìm các từ khóa mới nổi có volume cao trong chu kỳ ngắn.
 */
const { getSearchConsoleClient } = require('../core/auth');
const { extractDomain } = require('../core/config');
const { 
    printHeader, 
    getReportFilename, 
    saveJsonReport, 
    saveMarkdownReport, 
    mdTable, 
    fmtCTR, 
    fmtPos, 
    shortUrl 
} = require('../core/reporter');

async function run(config) {
    const { siteUrl, rowLimit } = config;
    if (!siteUrl) throw new Error('[CRITICAL] --site hoặc SITE_URL là bắt buộc.');

    printHeader('Rank & Traffic Comparison (3-Day Periods)', config);
    const domain = extractDomain(siteUrl);
    const { searchconsole } = await getSearchConsoleClient();

    // 1. Tự động xác định ngày gần nhất có dữ liệu (quét lùi tối đa 12 ngày)
    const today = new Date();
    let latestDateStr = '';
    let latestRows = [];

    const fetchSingleDay = async (dateStr) => {
        console.log(`  Checking data for date: ${dateStr}...`);
        const res = await searchconsole.searchanalytics.query({
            siteUrl,
            requestBody: {
                startDate: dateStr,
                endDate: dateStr,
                dimensions: ['query'],
                rowLimit: 5
            }
        });
        return res.data.rows || [];
    };

    let daysAgo = 2;
    while (daysAgo < 12) {
        const testDateStr = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        try {
            const rows = await fetchSingleDay(testDateStr);
            if (rows && rows.length > 0) {
                latestDateStr = testDateStr;
                latestRows = rows;
                break;
            }
        } catch (e) {
            console.warn(`  [WARNING] Failed checking date ${testDateStr}: ${e.message}`);
        }
        daysAgo++;
    }

    if (!latestDateStr) {
        throw new Error('[CRITICAL] Không tìm thấy ngày nào có dữ liệu trong vòng 10 ngày qua.');
    }

    console.log(`  [SUCCESS] Latest date with data found: ${latestDateStr}`);

    // 2. Tính toán 2 chu kỳ 3 ngày
    // Period A (Current 3 days): [latestDate - 2 days, latestDate]
    // Period B (Previous 3 days): [latestDate - 5 days, latestDate - 3 days]
    const latestDate = new Date(latestDateStr);
    
    const dateAEnd = latestDateStr;
    const dateAStart = new Date(latestDate.getTime() - 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

    const dateBEnd = new Date(latestDate.getTime() - 3 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    const dateBStart = new Date(latestDate.getTime() - 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

    console.log(`  -> Chu kỳ A (3 ngày hiện tại): ${dateAStart} đến ${dateAEnd}`);
    console.log(`  -> Chu kỳ B (3 ngày trước đó): ${dateBStart} đến ${dateBEnd}`);

    // Hàm gọi dữ liệu cho một chu kỳ
    const fetchPeriodData = async (startDate, endDate) => {
        console.log(`  Fetching GSC data from ${startDate} to ${endDate}...`);
        const res = await searchconsole.searchanalytics.query({
            siteUrl,
            requestBody: {
                startDate,
                endDate,
                dimensions: ['query', 'page'],
                rowLimit
            }
        });
        return res.data.rows || [];
    };

    const rowsA = await fetchPeriodData(dateAStart, dateAEnd);
    const rowsB = await fetchPeriodData(dateBStart, dateBEnd);

    console.log(`  [SUCCESS] Lấy thành công ${rowsA.length} dòng cho Chu kỳ A, ${rowsB.length} dòng cho Chu kỳ B.`);

    // 3. Map dữ liệu Chu kỳ B (Previous) để so sánh theo key "query|||page"
    const prevMap = {};
    rowsB.forEach(row => {
        const query = row.keys[0];
        const page = row.keys[1];
        const key = `${query}|||${page}`;
        prevMap[key] = {
            clicks: row.clicks,
            impressions: row.impressions,
            ctr: row.ctr,
            position: row.position
        };
    });

    const comparisonList = [];

    // Duyệt qua Chu kỳ A (Current) để so sánh
    rowsA.forEach(row => {
        const query = row.keys[0];
        const page = row.keys[1];
        const key = `${query}|||${page}`;

        const curr = {
            clicks: row.clicks,
            impressions: row.impressions,
            ctr: row.ctr,
            position: row.position
        };

        const prev = prevMap[key] || {
            clicks: 0,
            impressions: 0,
            ctr: 0,
            position: 100 // Nếu chưa lọt top thì coi như nằm ngoài top 100
        };

        const clickDiff = curr.clicks - prev.clicks;
        const impressionDiff = curr.impressions - prev.impressions;
        const rankDiff = prev.position - curr.position; // Dương là tăng hạng (ví dụ: 15 về 10 -> tăng 5 hạng)

        comparisonList.push({
            query,
            page,
            prevClicks: prev.clicks,
            currClicks: curr.clicks,
            clickDiff,
            prevImpressions: prev.impressions,
            currImpressions: curr.impressions,
            impressionDiff,
            prevPos: prev.position,
            currPos: curr.position,
            rankDiff,
            isNew: !prevMap[key],
            prevImpressionsRaw: prevMap[key] ? prev.impressions : 0
        });

        // Xóa để tìm các key bị bay màu
        delete prevMap[key];
    });

    // Các key có trong B nhưng biến mất trong A
    Object.keys(prevMap).forEach(key => {
        const [query, page] = key.split('|||');
        const prev = prevMap[key];
        comparisonList.push({
            query,
            page,
            prevClicks: prev.clicks,
            currClicks: 0,
            clickDiff: -prev.clicks,
            prevImpressions: prev.impressions,
            currImpressions: 0,
            impressionDiff: -prev.impressions,
            prevPos: prev.position,
            currPos: 100,
            rankDiff: prev.position - 100,
            isLost: true,
            prevImpressionsRaw: prev.impressions
        });
    });

    // 4. Phân tích các nhóm chỉ số

    // 4.1 Tăng hạng nhiều nhất (Rank Gainers)
    // Chỉ tính các query có Impressions > 10 ở chu kỳ A để tránh rank ảo
    const rankGainers = comparisonList
        .filter(item => !item.isLost && item.rankDiff > 0.5 && item.currImpressions > 10)
        .sort((a, b) => b.rankDiff - a.rankDiff)
        .slice(0, 20);

    // 4.2 Giảm hạng nhiều nhất (Rank Losers)
    const rankLosers = comparisonList
        .filter(item => item.rankDiff < -0.5 && (item.prevImpressions > 10 || item.currImpressions > 10))
        .sort((a, b) => a.rankDiff - b.rankDiff)
        .slice(0, 20);

    // 4.3 Tăng traffic/click nhiều nhất (Click Gainers)
    const clickGainers = comparisonList
        .filter(item => item.clickDiff > 0)
        .sort((a, b) => b.clickDiff - a.clickDiff)
        .slice(0, 20);

    // 4.4 Giảm traffic/click nhiều nhất (Click Losers)
    const clickLosers = comparisonList
        .filter(item => item.clickDiff < 0)
        .sort((a, b) => a.clickDiff - b.clickDiff)
        .slice(0, 20);

    // 4.5 Từ khóa MỚI NỔI có Volume cao
    // Định nghĩa: Chu kỳ trước có rất ít hoặc không có hiển thị (prevImpressions <= 3),
    // Chu kỳ hiện tại hiển thị tăng vọt (currImpressions >= 15)
    const newHighVolume = comparisonList
        .filter(item => item.prevImpressionsRaw <= 3 && item.currImpressions >= 15)
        .sort((a, b) => b.currImpressions - a.currImpressions)
        .slice(0, 20);

    // 5. Thống kê tổng hợp toàn site
    const totalPrevClicks = rowsB.reduce((sum, r) => sum + r.clicks, 0);
    const totalCurrClicks = rowsA.reduce((sum, r) => sum + r.clicks, 0);
    const totalClickChange = totalCurrClicks - totalPrevClicks;
    const totalClickChangePct = totalPrevClicks > 0 ? (totalClickChange / totalPrevClicks) * 100 : 0;

    const totalPrevImps = rowsB.reduce((sum, r) => sum + r.impressions, 0);
    const totalCurrImps = rowsA.reduce((sum, r) => sum + r.impressions, 0);
    const totalImpChange = totalCurrImps - totalPrevImps;
    const totalImpChangePct = totalPrevImps > 0 ? (totalImpChange / totalPrevImps) * 100 : 0;

    const reportData = {
        meta: {
            siteUrl,
            periodA: { start: dateAStart, end: dateAEnd },
            periodB: { start: dateBStart, end: dateBEnd },
            generatedAt: new Date().toISOString(),
            stats: {
                prevClicks: totalPrevClicks,
                currClicks: totalCurrClicks,
                clickChange: totalClickChange,
                clickChangePct: totalClickChangePct,
                prevImpressions: totalPrevImps,
                currImpressions: totalCurrImps,
                impChange: totalImpChange,
                impChangePct: totalImpChangePct
            }
        },
        data: {
            rankGainers,
            rankLosers,
            clickGainers,
            clickLosers,
            newHighVolume
        }
    };

    const files = getReportFilename('rank-comparison-3days', domain);
    await saveJsonReport(files.json, reportData);

    // 6. Xây dựng Báo cáo Markdown (Vietnamese)
    let md = `# 📈 Báo Cáo So Sánh Rank & Traffic 3 Ngày — ${domain}\n\n`;
    md += `## 📊 Tóm Tắt Hiệu Suất Tổng Quan\n`;
    md += `- **Chu kỳ hiện tại (3 ngày A):** ${dateAStart} đến ${dateAEnd}\n`;
    md += `- **Chu kỳ đối chiếu (3 ngày B trước đó):** ${dateBStart} đến ${dateBEnd}\n\n`;

    const pctEmoji = (val) => val >= 0 ? '🟢' : '🔴';
    const numSign = (val) => val >= 0 ? `+${val}` : `${val}`;
    const pctSign = (val) => val >= 0 ? `+${val.toFixed(1)}%` : `${val.toFixed(1)}%`;

    md += `| Chỉ số | Chu kỳ B (${dateBStart} - ${dateBEnd}) | Chu kỳ A (${dateAStart} - ${dateAEnd}) | Thay đổi | % Thay đổi |\n`;
    md += `| :--- | :---: | :---: | :---: | :---: |\n`;
    md += `| **Tổng Clicks** | ${totalPrevClicks.toLocaleString()} | ${totalCurrClicks.toLocaleString()} | ${numSign(totalClickChange)} | ${pctEmoji(totalClickChangePct)} **${pctSign(totalClickChangePct)}** |\n`;
    md += `| **Tổng Impressions (Volume)** | ${totalPrevImps.toLocaleString()} | ${totalCurrImps.toLocaleString()} | ${numSign(totalImpChange)} | ${pctEmoji(totalImpChangePct)} **${pctSign(totalImpChangePct)}** |\n\n`;

    // Định dạng các cột hiển thị
    const fmtRankDiff = (val, row) => {
        if (row.isNew) return '🆕 Mới';
        if (row.isLost) return '❌ Mất top';
        if (Math.abs(val) < 0.1) return '➖';
        return val > 0 ? `▲ +${val.toFixed(1)}` : `▼ ${val.toFixed(1)}`;
    };

    const fmtNumDiff = (val) => {
        if (val === 0) return '0';
        return val > 0 ? `▲ +${val}` : `▼ ${val}`;
    };

    const formatters = {
        page: (v) => `[${shortUrl(v, siteUrl)}](${v})`,
        prevPos: (v) => v === 100 ? '-' : v.toFixed(1),
        currPos: (v) => v === 100 ? '-' : v.toFixed(1),
        rankDiff: fmtRankDiff,
        clickDiff: fmtNumDiff,
        impressionDiff: fmtNumDiff
    };

    // 6.1 Từ khóa MỚI NỔI có Volume cao
    md += `## 🆕 1. Từ Khóa Mới Xuất Hiện Có Volume (Hiển Thị) Cao\n`;
    md += `> Các từ khóa trước đó hầu như không có hiển thị (impressions <= 3) nhưng hiện tại đã bứt phá đạt lượt hiển thị lớn. Đây là cơ hội tối ưu nội dung để lấy traffic.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Hiển Thị 3 Ngày A', 'Clicks 3 Ngày A', 'Rank 3 Ngày A', 'Hiển Thị Trước'],
        ['query', 'page', 'currImpressions', 'currClicks', 'currPos', 'prevImpressions'],
        newHighVolume,
        formatters
    );
    md += `\n`;

    // 6.2 Top Rank Gainers
    md += `## 🚀 2. Từ Khóa Tăng Hạng Nhiều Nhất (Rank Gainers)\n`;
    md += `> Top các từ khóa tăng hạng mạnh nhất (trung bình vị trí được cải thiện nhiều nhất trong 3 ngày).\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Rank Trước (B)', 'Rank Hiện Tại (A)', 'Thay Đổi Rank', 'Clicks A', 'Hiển Thị A'],
        ['query', 'page', 'prevPos', 'currPos', 'rankDiff', 'currClicks', 'currImpressions'],
        rankGainers,
        formatters
    );
    md += `\n`;

    // 6.3 Top Rank Losers
    md += `## 📉 3. Từ Khóa Giảm Hạng Nhiều Nhất (Rank Losers)\n`;
    md += `> Top các từ khóa bị sụt giảm thứ hạng nhiều nhất. Hãy chú ý kiểm tra content/backlink cho các trang này.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Rank Trước (B)', 'Rank Hiện Tại (A)', 'Thay Đổi Rank', 'Clicks A', 'Hiển Thị A'],
        ['query', 'page', 'prevPos', 'currPos', 'rankDiff', 'currClicks', 'currImpressions'],
        rankLosers,
        formatters
    );
    md += `\n`;

    // 6.4 Top Click Gainers
    md += `## ➕ 4. Từ Khóa Tăng Traffic Nhiều Nhất (Click Gainers)\n`;
    md += `> Các từ khóa mang lại lượng click gia tăng lớn nhất cho website.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Clicks B', 'Clicks A', 'Thay Đổi Clicks', 'Rank B', 'Rank A'],
        ['query', 'page', 'prevClicks', 'currClicks', 'clickDiff', 'prevPos', 'currPos'],
        clickGainers,
        formatters
    );
    md += `\n`;

    // 6.5 Top Click Losers
    md += `## ➖ 5. Từ Khóa Giảm Traffic Nhiều Nhất (Click Losers)\n`;
    md += `> Các từ khóa bị tụt giảm click nhiều nhất. Cần tối ưu lại tiêu đề/meta hoặc nội dung.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Clicks B', 'Clicks A', 'Thay Đổi Clicks', 'Rank B', 'Rank A'],
        ['query', 'page', 'prevClicks', 'currClicks', 'clickDiff', 'prevPos', 'currPos'],
        clickLosers,
        formatters
    );
    md += `\n`;

    // Tạo đề xuất hành động cho Agent
    const agentActions = [];
    if (newHighVolume.length > 0) {
        agentActions.push({
            priority: 'P0-CRITICAL',
            title: `Tập trung tối ưu từ khóa mới nổi: "${newHighVolume[0].query}"`,
            description: `Từ khóa mới nổi "${newHighVolume[0].query}" có lượt hiển thị tăng vọt lên ${newHighVolume[0].currImpressions} nhưng chỉ nhận được ${newHighVolume[0].currClicks} clicks (Rank ${newHighVolume[0].currPos.toFixed(1)}).`,
            files: `Trang đích: ${shortUrl(newHighVolume[0].page, siteUrl)}`
        });
    }
    if (rankLosers.length > 0) {
        agentActions.push({
            priority: 'P1-HIGH',
            title: `Khôi phục thứ hạng từ khóa tụt sâu: "${rankLosers[0].query}"`,
            description: `Từ khóa "${rankLosers[0].query}" tụt ${Math.abs(rankLosers[0].rankDiff).toFixed(1)} hạng về mức ${rankLosers[0].currPos.toFixed(1)}.`,
            files: `Trang đích: ${shortUrl(rankLosers[0].page, siteUrl)}`
        });
    }

    if (agentActions.length > 0) {
        const { buildAgentInstructions } = require('../core/reporter');
        md += buildAgentInstructions(agentActions);
    }

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
