/**
 * Module: Rank Comparison (24h comparison)
 * So sánh hiệu suất từ khóa & rank của 24h gần nhất (có dữ liệu) so với 24h trước đó.
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

    printHeader('Rank & Traffic Comparison (24h)', config);
    const domain = extractDomain(siteUrl);
    const { searchconsole } = await getSearchConsoleClient();

    // Tự động tìm ngày gần nhất có dữ liệu (thử lùi tối đa 10 ngày)
    const today = new Date();
    let currentDate = '';
    let previousDate = '';
    let currentRows = [];
    let previousRows = [];

    const fetchPeriod = async (date) => {
        console.log(`  Fetching data for date: ${date}...`);
        const res = await searchconsole.searchanalytics.query({
            siteUrl,
            requestBody: {
                startDate: date,
                endDate: date,
                dimensions: ['query', 'page'],
                rowLimit
            }
        });
        return res.data.rows || [];
    };

    let daysAgo = 2;
    while (daysAgo < 12) {
        const testDate = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        console.log(`  Testing date for data availability: ${testDate}...`);
        try {
            const rows = await fetchPeriod(testDate);
            if (rows && rows.length > 0) {
                currentDate = testDate;
                currentRows = rows;
                
                // Tìm ngày liền trước có dữ liệu
                const prevDate = new Date(today.getTime() - (daysAgo + 1) * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
                previousDate = prevDate;
                previousRows = await fetchPeriod(previousDate);
                break;
            }
        } catch (e) {
            console.warn(`  [WARNING] Failed fetching date ${testDate}: ${e.message}`);
        }
        daysAgo++;
    }

    if (!currentDate || currentRows.length === 0) {
        throw new Error('[CRITICAL] No data could be retrieved from Google Search Console for the last 10 days.');
    }

    console.log(`  Kỳ hiện tại (Current - gần nhất có dữ liệu): ${currentDate} (${currentRows.length} rows)`);
    console.log(`  Kỳ đối chiếu (Previous - ngày trước đó): ${previousDate} (${previousRows.length} rows)`);

    // Map dữ liệu để so sánh theo key: "query|||page"
    const prevMap = {};
    previousRows.forEach(row => {
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

    // Duyệt qua kỳ hiện tại
    currentRows.forEach(row => {
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
            position: 100 // Gán mặc định ngoài top 100 nếu chưa có rank
        };

        const clickDiff = curr.clicks - prev.clicks;
        const impressionDiff = curr.impressions - prev.impressions;
        // Position diff: giảm số nghĩa là tăng rank (ví dụ: rank 5 -> rank 2 => tăng 3 hạng. rankDiff = 5 - 2 = +3)
        // Nếu trước đó không xuất hiện (mặc định 100) thì coi như mới vào top
        const rankDiff = prev.position - curr.position;

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
            isNew: !prevMap[key]
        });

        // Xóa khỏi map để lát tìm các trang bị rớt khỏi top hoàn toàn
        delete prevMap[key];
    });

    // Các trang có trong kỳ đối chiếu nhưng biến mất trong kỳ hiện tại
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
            currPos: 100, // Coi như bay màu khỏi top 100
            rankDiff: prev.position - 100,
            isLost: true
        });
    });

    // 1. TỐP TĂNG HẠNG NHIỀU NHẤT (Rank Gainers)
    // Điều kiện: impressions hiện tại > 10 (tránh rank ảo của từ khóa không ai tìm)
    const rankGainers = comparisonList
        .filter(item => !item.isLost && item.rankDiff > 0.5 && item.currImpressions > 10)
        .sort((a, b) => b.rankDiff - a.rankDiff)
        .slice(0, 20);

    // 2. TỐP GIẢM HẠNG NHIỀU NHẤT (Rank Losers)
    const rankLosers = comparisonList
        .filter(item => item.rankDiff < -0.5 && (item.prevImpressions > 10 || item.currImpressions > 10))
        .sort((a, b) => a.rankDiff - b.rankDiff) // Âm nhiều nhất xếp trước
        .slice(0, 20);

    // 3. TỐP TĂNG CLICKS NHIỀU NHẤT (Click Gainers)
    const clickGainers = comparisonList
        .filter(item => item.clickDiff > 0)
        .sort((a, b) => b.clickDiff - a.clickDiff)
        .slice(0, 20);

    // 4. TỐP GIẢM CLICKS NHIỀU NHẤT (Click Losers)
    const clickLosers = comparisonList
        .filter(item => item.clickDiff < 0)
        .sort((a, b) => a.clickDiff - b.clickDiff)
        .slice(0, 20);

    // 5. TỐP TỪ KHÓA MỚI LỌT TOP (New Entrants)
    const newEntrants = comparisonList
        .filter(item => item.isNew && item.currPos <= 30 && item.currImpressions > 10)
        .sort((a, b) => a.currPos - b.currPos)
        .slice(0, 20);

    // Thống kê tổng hợp
    const totalPrevClicks = previousRows.reduce((sum, r) => sum + r.clicks, 0);
    const totalCurrClicks = currentRows.reduce((sum, r) => sum + r.clicks, 0);
    const totalClickChange = totalCurrClicks - totalPrevClicks;
    const totalClickChangePct = totalPrevClicks > 0 ? (totalClickChange / totalPrevClicks) * 100 : 0;

    const totalPrevImps = previousRows.reduce((sum, r) => sum + r.impressions, 0);
    const totalCurrImps = currentRows.reduce((sum, r) => sum + r.impressions, 0);
    const totalImpChange = totalCurrImps - totalPrevImps;
    const totalImpChangePct = totalPrevImps > 0 ? (totalImpChange / totalPrevImps) * 100 : 0;

    const reportData = {
        meta: {
            siteUrl,
            currentDate,
            previousDate,
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
            newEntrants
        }
    };

    const files = getReportFilename('rank-comparison', domain);
    await saveJsonReport(files.json, reportData);

    // Xây dựng báo cáo Markdown
    let md = `# 📈 Báo Cáo So Sánh Rank & Traffic 24h — ${domain}\n\n`;
    md += `## 📊 Tóm Tắt Hiệu Suất Tổng Quan\n`;
    md += `So sánh ngày **${currentDate}** (Kỳ hiện tại) vs **${previousDate}** (Kỳ đối chiếu).\n\n`;

    const pctEmoji = (val) => val >= 0 ? '🟢' : '🔴';
    const numSign = (val) => val >= 0 ? `+${val}` : `${val}`;
    const pctSign = (val) => val >= 0 ? `+${val.toFixed(1)}%` : `${val.toFixed(1)}%`;

    md += `| Chỉ số | Kỳ đối chiếu (${previousDate}) | Kỳ hiện tại (${currentDate}) | Thay đổi | % Thay đổi |\n`;
    md += `| :--- | :---: | :---: | :---: | :---: |\n`;
    md += `| **Tổng Clicks** | ${totalPrevClicks.toLocaleString()} | ${totalCurrClicks.toLocaleString()} | ${numSign(totalClickChange)} | ${pctEmoji(totalClickChangePct)} **${pctSign(totalClickChangePct)}** |\n`;
    md += `| **Tổng Impressions** | ${totalPrevImps.toLocaleString()} | ${totalCurrImps.toLocaleString()} | ${numSign(totalImpChange)} | ${pctEmoji(totalImpChangePct)} **${pctSign(totalImpChangePct)}** |\n\n`;

    // Định dạng cột Rank Diff
    const fmtRankDiff = (val, row) => {
        if (row.isNew) return '🆕 Mới';
        if (row.isLost) return '❌ Mất top';
        if (val === 0) return '➖';
        return val > 0 ? `▲ +${val.toFixed(1)}` : `▼ ${val.toFixed(1)}`;
    };

    const fmtNumDiff = (val) => {
        if (val === 0) return '0';
        return val > 0 ? `▲ +${val}` : `▼ ${val}`;
    };

    // Table formatter
    const formatters = {
        page: (v) => `[${shortUrl(v, siteUrl)}](${v})`,
        prevPos: (v) => v === 100 ? '-' : v.toFixed(1),
        currPos: (v) => v === 100 ? '-' : v.toFixed(1),
        rankDiff: fmtRankDiff,
        clickDiff: fmtNumDiff,
        impressionDiff: fmtNumDiff
    };

    // 1. Top Rank Gainers
    md += `## 🚀 1. Từ Khóa Tăng Hạng Nhiều Nhất (Top Rank Gainers)\n`;
    md += `> Các từ khóa có sự bứt phá thứ hạng mạnh mẽ nhất trong 24h qua.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Rank Trước', 'Rank Hiện Tại', 'Thay Đổi Rank', 'Clicks', 'Impressions'],
        ['query', 'page', 'prevPos', 'currPos', 'rankDiff', 'currClicks', 'currImpressions'],
        rankGainers,
        formatters
    );
    md += `\n`;

    // 2. Top Rank Losers
    md += `## 📉 2. Từ Khóa Giảm Hạng Nhiều Nhất (Top Rank Losers)\n`;
    md += `> Các từ khóa bị tụt hạng sâu nhất. Cần kiểm tra lại nội dung và liên kết của các trang này.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Rank Trước', 'Rank Hiện Tại', 'Thay Đổi Rank', 'Clicks', 'Impressions'],
        ['query', 'page', 'prevPos', 'currPos', 'rankDiff', 'currClicks', 'currImpressions'],
        rankLosers,
        formatters
    );
    md += `\n`;

    // 3. Top Click Gainers
    md += `## ➕ 3. Từ Khóa Tăng Click Nhiều Nhất (Top Click Gainers)\n`;
    md += `> Những từ khóa mang lại sự tăng trưởng traffic đột phá trong 24h qua.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Clicks Trước', 'Clicks Hiện Tại', 'Thay Đổi Clicks', 'Rank Trước', 'Rank Hiện Tại'],
        ['query', 'page', 'prevClicks', 'currClicks', 'clickDiff', 'prevPos', 'currPos'],
        clickGainers,
        formatters
    );
    md += `\n`;

    // 4. Top Click Losers
    md += `## ➖ 4. Từ Khóa Giảm Click Nhiều Nhất (Top Click Losers)\n`;
    md += `> Những từ khóa bị sụt giảm click nhiều nhất. Cần tối ưu lại CTR hoặc cải thiện thứ hạng.\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Clicks Trước', 'Clicks Hiện Tại', 'Thay Đổi Clicks', 'Rank Trước', 'Rank Hiện Tại'],
        ['query', 'page', 'prevClicks', 'currClicks', 'clickDiff', 'prevPos', 'currPos'],
        clickLosers,
        formatters
    );
    md += `\n`;

    // 5. New Entrants
    md += `## 🆕 5. Từ Khóa Mới Lọt Top (New Entrants)\n`;
    md += `> Các từ khóa mới xuất hiện trong Top 30 lần đầu tiên (ở kỳ hiện tại so với không có ở kỳ đối chiếu).\n\n`;
    md += mdTable(
        ['Từ Khóa', 'Trang Đích', 'Rank Hiện Tại', 'Clicks', 'Impressions'],
        ['query', 'page', 'currPos', 'currClicks', 'currImpressions'],
        newEntrants,
        formatters
    );
    md += `\n`;

    // Tạo đề xuất hành động cho Agent
    const agentActions = [];
    if (rankLosers.length > 0) {
        agentActions.push({
            priority: 'P0-CRITICAL',
            title: `Fix decaying rankings on top query: "${rankLosers[0].query}"`,
            description: `Từ khóa "${rankLosers[0].query}" bị tụt ${Math.abs(rankLosers[0].rankDiff).toFixed(1)} hạng (từ ${rankLosers[0].prevPos.toFixed(1)} về ${rankLosers[0].currPos.toFixed(1)}).`,
            files: `Trang đích: ${shortUrl(rankLosers[0].page, siteUrl)}`
        });
    }
    if (clickLosers.length > 0 && clickLosers[0].clickDiff <= -5) {
        agentActions.push({
            priority: 'P1-HIGH',
            title: `Improve CTR/Rank for: "${clickLosers[0].query}"`,
            description: `Clicks giảm từ ${clickLosers[0].prevClicks} xuống ${clickLosers[0].currClicks} (${clickLosers[0].clickDiff} clicks).`,
            files: `Trang đích: ${shortUrl(clickLosers[0].page, siteUrl)}`
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
