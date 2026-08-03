/**
 * Module: Technical SEO Auditor
 * Crawl website → Kiểm tra 12+ rules kỹ thuật SEO cho từng trang
 */
const { parseSitemap, fetchPage, batchProcess } = require('../core/crawler');
const { extractDomain } = require('../core/config');
const { printHeader, getReportFilename, saveJsonReport, saveMarkdownReport, mdTable, shortUrl, buildAgentInstructions } = require('../core/reporter');
const { getSearchConsoleClient } = require('../core/auth');

// ═══════════════════════════════════════════
// SEO RULES ENGINE
// ═══════════════════════════════════════════
const SEO_RULES = [
    {
        id: 'title-exists',
        name: 'Title tag tồn tại',
        weight: 10,
        check: ($) => {
            const title = $('title').first().text().trim();
            return { pass: !!title, value: title || '(missing)', detail: !title ? 'Thiếu thẻ <title>' : null };
        }
    },
    {
        id: 'title-length',
        name: 'Title length (30-60 chars)',
        weight: 8,
        check: ($) => {
            const title = $('title').first().text().trim();
            const len = title.length;
            return {
                pass: len >= 30 && len <= 60,
                value: `${len} chars`,
                detail: len < 30 ? `Quá ngắn (${len} < 30)` : len > 60 ? `Quá dài (${len} > 60)` : null
            };
        }
    },
    {
        id: 'meta-description-exists',
        name: 'Meta description tồn tại',
        weight: 9,
        check: ($) => {
            const desc = $('meta[name="description"]').attr('content') || '';
            return { pass: !!desc.trim(), value: desc.substring(0, 80) || '(missing)', detail: !desc.trim() ? 'Thiếu meta description' : null };
        }
    },
    {
        id: 'meta-description-length',
        name: 'Meta description length (120-160 chars)',
        weight: 7,
        check: ($) => {
            const desc = ($('meta[name="description"]').attr('content') || '').trim();
            const len = desc.length;
            return {
                pass: len >= 120 && len <= 160,
                value: `${len} chars`,
                detail: len < 120 ? `Quá ngắn (${len} < 120)` : len > 160 ? `Quá dài (${len} > 160)` : null
            };
        }
    },
    {
        id: 'h1-count',
        name: 'Chỉ có 1 thẻ H1',
        weight: 9,
        check: ($) => {
            const count = $('h1').length;
            return { pass: count === 1, value: `${count} H1 tags`, detail: count === 0 ? 'Thiếu H1' : count > 1 ? `Có ${count} H1, chỉ nên có 1` : null };
        }
    },
    {
        id: 'images-alt',
        name: 'Images có alt text',
        weight: 6,
        check: ($) => {
            const images = $('img');
            let missing = 0;
            images.each((_, el) => {
                const alt = $(el).attr('alt');
                if (!alt || !alt.trim()) missing++;
            });
            const total = images.length;
            return {
                pass: missing === 0,
                value: `${total - missing}/${total} có alt`,
                detail: missing > 0 ? `${missing}/${total} ảnh thiếu alt text` : null
            };
        }
    },
    {
        id: 'canonical',
        name: 'Canonical tag',
        weight: 8,
        check: ($) => {
            const canonical = $('link[rel="canonical"]').attr('href') || '';
            return { pass: !!canonical, value: canonical || '(missing)', detail: !canonical ? 'Thiếu canonical tag' : null };
        }
    },
    {
        id: 'og-tags',
        name: 'Open Graph tags',
        weight: 5,
        check: ($) => {
            const ogTitle = $('meta[property="og:title"]').attr('content') || '';
            const ogDesc = $('meta[property="og:description"]').attr('content') || '';
            const ogImage = $('meta[property="og:image"]').attr('content') || '';
            const score = [ogTitle, ogDesc, ogImage].filter(v => !!v).length;
            return {
                pass: score >= 2,
                value: `${score}/3 OG tags`,
                detail: score < 2 ? `Thiếu OG tags: ${!ogTitle ? 'og:title ' : ''}${!ogDesc ? 'og:description ' : ''}${!ogImage ? 'og:image' : ''}` : null
            };
        }
    },
    {
        id: 'structured-data',
        name: 'Structured Data (JSON-LD)',
        weight: 7,
        check: ($) => {
            const jsonld = $('script[type="application/ld+json"]');
            return {
                pass: jsonld.length > 0,
                value: `${jsonld.length} schema(s)`,
                detail: jsonld.length === 0 ? 'Không có JSON-LD structured data' : null
            };
        }
    },
    {
        id: 'viewport',
        name: 'Viewport meta tag',
        weight: 8,
        check: ($) => {
            const viewport = $('meta[name="viewport"]').attr('content') || '';
            return { pass: !!viewport, value: viewport ? 'OK' : '(missing)', detail: !viewport ? 'Thiếu viewport meta — không mobile-friendly' : null };
        }
    },
    {
        id: 'lang-attribute',
        name: 'HTML lang attribute',
        weight: 4,
        check: ($) => {
            const lang = $('html').attr('lang') || '';
            return { pass: !!lang, value: lang || '(missing)', detail: !lang ? 'Thiếu lang attribute trên <html>' : null };
        }
    },
    {
        id: 'heading-hierarchy',
        name: 'Heading hierarchy (H2-H6)',
        weight: 5,
        check: ($) => {
            const h2 = $('h2').length;
            const h3 = $('h3').length;
            return {
                pass: h2 > 0,
                value: `H2: ${h2}, H3: ${h3}`,
                detail: h2 === 0 ? 'Không có thẻ H2 — cấu trúc heading yếu' : null
            };
        }
    }
];

/**
 * Audit 1 page
 */
async function auditPage(url, options = {}) {
    try {
        const { $, statusCode } = await fetchPage(url, options);

        if (statusCode !== 200) {
            return { url, statusCode, score: 0, passed: 0, total: SEO_RULES.length, issues: [`HTTP ${statusCode}`], results: [] };
        }

        let totalWeight = 0;
        let earnedWeight = 0;
        const results = [];
        const issues = [];

        SEO_RULES.forEach(rule => {
            const result = rule.check($);
            totalWeight += rule.weight;
            if (result.pass) earnedWeight += rule.weight;
            else if (result.detail) issues.push(result.detail);

            results.push({
                id: rule.id,
                name: rule.name,
                pass: result.pass,
                value: result.value,
                detail: result.detail
            });
        });

        const score = totalWeight > 0 ? Math.round((earnedWeight / totalWeight) * 100) : 0;
        const passed = results.filter(r => r.pass).length;

        return { url, statusCode, score, passed, total: SEO_RULES.length, issues, results };
    } catch (e) {
        return { url, statusCode: 0, score: 0, passed: 0, total: SEO_RULES.length, issues: [`Error: ${e.message}`], results: [] };
    }
}

async function inspectUrlWithGoogle(url, siteUrl) {
    try {
        const { searchconsole } = await getSearchConsoleClient();
        console.log(`  📡 Gọi Google URL Inspection API cho URL này...`);
        const res = await searchconsole.urlInspection.index.inspect({
            requestBody: {
                inspectionUrl: url,
                siteUrl: siteUrl,
                languageCode: 'vi'
            }
        });
        return res.data.inspectionResult;
    } catch (e) {
        console.warn(`\n  ⚠️  Google URL Inspection API thất bại: ${e.message}`);
        return null;
    }
}

function printSinglePageReport(local, gsc, siteUrl) {
    console.log('\n==================================================');
    console.log(`🤖 BÁO CÁO KIỂM TRA TRANG ĐƠN LẺ & GOOGLE INDEXING`);
    console.log(`URL: ${local.url}`);
    console.log(`HTTP Status: ${local.statusCode} | SEO Score: ${local.score}/100`);
    console.log('==================================================');

    console.log('\n🛡️  KẾT QUẢ KIỂM TRA ON-PAGE CỤC BỘ:');
    local.results.forEach(r => {
        const icon = r.pass ? '✅' : '❌';
        console.log(`  ${icon} ${r.name}: ${r.value} ${r.detail ? `(${r.detail})` : ''}`);
    });

    if (gsc) {
        const status = gsc.indexStatusResult || {};
        console.log('\n📡 TRẠNG THÁI TRÊN GOOGLE SEARCH CONSOLE:');
        console.log(`  🔍 Verdict: ${status.verdict === 'PASS' ? '🟢 ĐÃ ĐƯỢC INDEX (URL is on Google)' : status.verdict === 'FAIL' ? '🔴 CHƯA ĐƯỢC INDEX (URL is not on Google)' : '🟡 NEUTRAL'}`);
        console.log(`  📝 Trạng thái Index: ${status.coverageState || 'Không xác định'}`);
        console.log(`  ⚙️  Cho phép Index: ${status.indexingState || 'Không xác định'}`);
        console.log(`  📥 Trạng thái Fetch: ${status.pageFetchState || 'Không xác định'}`);
        console.log(`  📅 Thời gian quét cuối: ${status.lastCrawlTime || 'Chưa bao giờ'}`);
        console.log(`  🤖 Crawled As: ${status.crawledAs || 'Không xác định'}`);
        console.log(`  🔗 Google Canonical: ${status.googleCanonical || 'Không có'}`);
        console.log(`  🔗 User Canonical: ${status.userCanonical || 'Không có'}`);
        if (status.referringUrls && status.referringUrls.length > 0) {
            console.log(`  📂 Phát hiện từ nguồn (Referrers):`);
            status.referringUrls.slice(0, 5).forEach(ref => console.log(`     - ${ref}`));
            if (status.referringUrls.length > 5) {
                console.log(`     ... và ${status.referringUrls.length - 5} URL khác`);
            }
        }
        if (status.sitemap && status.sitemap.length > 0) {
            console.log(`  🗺️  Trong Sitemap:`);
            status.sitemap.forEach(sm => console.log(`     - ${sm}`));
        }

        const mobile = gsc.mobileUsabilityResult;
        if (mobile) {
            console.log(`\n📱 THÂN THIỆN VỚI DI ĐỘNG: ${mobile.verdict === 'PASS' ? '✅ Có' : '❌ Không'}`);
            if (mobile.issues && mobile.issues.length > 0) {
                mobile.issues.forEach(issue => {
                    console.log(`   - ❌ ${issue.issueType} (${issue.severity})`);
                });
            }
        }

        const rich = gsc.richResultsResult;
        if (rich) {
            console.log(`\n📐 SCHEMA / DỮ LIỆU CẤU TRÚC (Rich Results): ${rich.verdict === 'PASS' ? '✅ Hợp lệ' : rich.verdict === 'FAIL' ? '❌ Có lỗi' : '🟡 Neutral'}`);
            if (rich.detectedItems && rich.detectedItems.length > 0) {
                rich.detectedItems.forEach(item => {
                    console.log(`   - 📦 ${item.richResultType}:`);
                    if (item.items && item.items.length > 0) {
                        item.items.forEach(subItem => {
                            if (subItem.issues && subItem.issues.length > 0) {
                                subItem.issues.forEach(issue => {
                                    console.log(`     ❌ Lỗi: ${issue.issueMessage} (${issue.severity})`);
                                });
                            } else {
                                console.log(`     ✅ Hợp lệ: ${subItem.name || 'OK'}`);
                            }
                        });
                    }
                });
            }
        }
    } else {
        console.log('\n⚠️  TRẠNG THÁI GOOGLE INDEX: (Không lấy được dữ liệu, vui lòng check file service-account.json)');
    }
    console.log('\n==================================================\n');
}

function generateSinglePageMarkdown(local, gsc, siteUrl, domain) {
    let md = `# 🔧 Technical SEO Audit & Google Inspection — ${domain}\n\n`;
    md += `- **URL kiểm tra**: [${local.url}](${local.url})\n`;
    md += `- **SEO Score**: **${local.score}/100** ${local.score >= 80 ? '🟢' : local.score >= 50 ? '🟡' : '🔴'}\n`;
    md += `- **HTTP Status**: ${local.statusCode}\n`;
    md += `- **Thời gian chạy**: ${new Date().toISOString()}\n\n`;

    md += `## 🛡️ Kết quả kiểm tra On-Page cục bộ\n\n`;
    md += `| Quy tắc | Trạng thái | Giá trị ghi nhận | Chi tiết |\n`;
    md += `| :--- | :---: | :--- | :--- |\n`;
    local.results.forEach(r => {
        md += `| ${r.name} | ${r.pass ? '🟢 ĐẠT' : '🔴 THẤT BẠI'} | ${r.value || ''} | ${r.detail || ''} |\n`;
    });

    if (gsc) {
        const status = gsc.indexStatusResult || {};
        md += `\n## 📡 Google Search Console URL Inspection\n\n`;
        md += `- **Google Verdict**: **${status.verdict || 'UNKNOWN'}** (${status.verdict === 'PASS' ? 'Đã lập chỉ mục' : 'Chưa lập chỉ mục'})\n`;
        md += `- **Trạng thái Index**: ${status.coverageState || 'Không rõ'}\n`;
        md += `- **indexing State (Cho phép index)**: ${status.indexingState || 'Không rõ'}\n`;
        md += `- **Trạng thái Fetch**: ${status.pageFetchState || 'Không rõ'}\n`;
        md += `- **Thời gian quét cuối cùng**: ${status.lastCrawlTime || 'Chưa bao giờ'}\n`;
        md += `- **Trình thu thập dữ liệu (Googlebot)**: ${status.crawledAs || 'Không rõ'}\n`;
        md += `- **URL Canonical do Google chọn**: ${status.googleCanonical || 'Không có'}\n`;
        md += `- **URL Canonical do User khai báo**: ${status.userCanonical || 'Không có'}\n`;

        if (status.referringUrls && status.referringUrls.length > 0) {
            md += `\n### 🔗 Phát hiện từ nguồn (Referrers)\n`;
            status.referringUrls.forEach(ref => {
                md += `- [${ref}](${ref})\n`;
            });
        }

        if (status.sitemap && status.sitemap.length > 0) {
            md += `\n### 🗺️ Trong Sitemaps\n`;
            status.sitemap.forEach(sm => {
                md += `- [${sm}](${sm})\n`;
            });
        }

        const mobile = gsc.mobileUsabilityResult;
        if (mobile) {
            md += `\n### 📱 Thân thiện với di động\n\n`;
            md += `- **Kết quả**: **${mobile.verdict}**\n`;
            if (mobile.issues && mobile.issues.length > 0) {
                md += `\n**Vấn đề phát hiện:**\n`;
                mobile.issues.forEach(issue => {
                    md += `- ❌ ${issue.issueType} (${issue.severity})\n`;
                });
            }
        }

        const rich = gsc.richResultsResult;
        if (rich) {
            md += `\n### 📐 Dữ liệu cấu trúc / Schema (Rich Results)\n\n`;
            md += `- **Kết quả**: **${rich.verdict}**\n`;
            if (rich.detectedItems && rich.detectedItems.length > 0) {
                rich.detectedItems.forEach(item => {
                    md += `\n#### 📦 ${item.richResultType}\n`;
                    if (item.items && item.items.length > 0) {
                        item.items.forEach(subItem => {
                            if (subItem.issues && subItem.issues.length > 0) {
                                md += `- **${subItem.name || 'Schema Item'}**:\n`;
                                subItem.issues.forEach(issue => {
                                    md += `  - ❌ ${issue.issueMessage} (${issue.severity})\n`;
                                });
                            } else {
                                md += `- ✅ Đạt: **${subItem.name || 'OK'}**\n`;
                            }
                        });
                    }
                });
            }
        }
    } else {
        md += `\n## 📡 Google Search Console URL Inspection\n\n`;
        md += `⚠️ *Không lấy được dữ liệu Google URL Inspection. Vui lòng xác thực tài khoản Google API và kiểm tra quyền GSC Property.* \n`;
    }

    // Checklist khắc phục
    md += `\n## 🛠️ Checklist Khắc Phục SEO Remediations\n\n`;
    local.results.filter(r => !r.pass).forEach(r => {
        md += `- [ ] **Sửa On-Page: ${r.name}**\n`;
        md += `  - Lỗi: ${r.detail || 'Không đạt kiểm tra cục bộ'}\n`;
    });

    if (gsc) {
        const status = gsc.indexStatusResult || {};
        if (status.verdict !== 'PASS') {
            md += `- [ ] **Sửa lỗi lập chỉ mục Google**\n`;
            md += `  - Lý do: ${status.coverageState || 'Chưa index'}\n`;
            md += `  - Gợi ý: Hãy kiểm tra file robots.txt, thẻ noindex, redirect hoặc canonical tag.\n`;
        }
        
        const rich = gsc.richResultsResult;
        if (rich && rich.verdict === 'FAIL') {
            md += `- [ ] **Khắc phục lỗi Dữ liệu cấu trúc (Schema)**\n`;
            md += `  - Google phát hiện lỗi schema cấu trúc trên trang. Kiểm tra phần Schema để sửa chi tiết.\n`;
        }
    }

    return md;
}

async function run(config) {
    const { sitemapUrl, siteUrl, crawlConcurrency, crawlDelay, maxPages, userAgent, targetUrl } = config;
    
    // XỬ LÝ TRƯỜNG HỢP KIỂM TRA URL ĐƠN LẺ
    if (targetUrl) {
        printHeader('Single Page Audit & Google Inspection', { ...config, targetUrl });
        const domain = extractDomain(targetUrl);
        
        console.log(`  Starting audit for URL: ${targetUrl}`);
        console.log(`  1. Running Local On-Page SEO checks...`);
        const localResult = await auditPage(targetUrl, { userAgent });
        
        let gscResult = null;
        if (localResult.statusCode === 200) {
            console.log(`  2. Checking Google Search Console index status...`);
            // Xác định siteUrl (GSC property) tự động nếu người dùng không truyền siteUrl
            let determinedSiteUrl = siteUrl;
            if (!determinedSiteUrl) {
                try {
                    const uObj = new URL(targetUrl);
                    determinedSiteUrl = `${uObj.origin}/`;
                } catch {
                    determinedSiteUrl = targetUrl;
                }
            }
            gscResult = await inspectUrlWithGoogle(targetUrl, determinedSiteUrl);
        } else {
            console.log(`  ⚠️ Skiping GSC Inspection vì trang trả về trạng thái HTTP ${localResult.statusCode}`);
        }
        
        // In báo cáo CLI trực quan
        printSinglePageReport(localResult, gscResult, siteUrl);
        
        // Lưu báo cáo file
        const files = getReportFilename('technical-audit-page', domain);
        const reportData = {
            meta: {
                siteUrl: siteUrl || (new URL(targetUrl).origin + '/'),
                targetUrl,
                isSinglePage: true,
                generatedAt: new Date().toISOString()
            },
            localAudit: localResult,
            googleInspection: gscResult ? {
                inspectionResultLink: gscResult.inspectionResultLink,
                indexStatusResult: gscResult.indexStatusResult,
                mobileUsabilityResult: gscResult.mobileUsabilityResult,
                richResultsResult: gscResult.richResultsResult
            } : null
        };
        
        await saveJsonReport(files.json, reportData);
        
        const mdContent = generateSinglePageMarkdown(localResult, gscResult, siteUrl, domain);
        await saveMarkdownReport(files.md, mdContent);
        
        console.log(`  📂 Reports generated:`);
        console.log(`     - JSON: ${files.json}`);
        console.log(`     - MD:   ${files.md}`);
        return reportData;
    }

    const targetSitemap = sitemapUrl || (siteUrl ? siteUrl.replace(/\/$/, '') + '/sitemap.xml' : null);
    if (!targetSitemap) throw new Error('[CRITICAL] --sitemap hoặc SITEMAP_URL hoặc --url là bắt buộc.');

    printHeader('Technical SEO Auditor', { ...config, sitemapUrl: targetSitemap });
    const domain = extractDomain(siteUrl || targetSitemap);

    console.log('  Parsing sitemap...');
    const sitemapUrls = await parseSitemap(targetSitemap);
    const urls = sitemapUrls.slice(0, maxPages).map(u => u.url);
    console.log(`  → ${sitemapUrls.length} URLs found, auditing ${urls.length}`);

    console.log('  Auditing pages...\n');
    const results = await batchProcess(urls, (url) => auditPage(url, { userAgent }), {
        concurrency: crawlConcurrency,
        delay: crawlDelay,
        onProgress: (done, total) => {
            process.stdout.write(`\r  Progress: ${done}/${total} (${Math.round(done/total*100)}%)`);
        }
    });
    console.log('\n');

    // Aggregate
    const validResults = results.filter(r => r.statusCode === 200);
    const avgScore = validResults.length > 0
        ? Math.round(validResults.reduce((s, r) => s + r.score, 0) / validResults.length)
        : 0;
    const errorPages = results.filter(r => r.statusCode !== 200);

    // Sort by score ascending (worst first)
    validResults.sort((a, b) => a.score - b.score);

    // Aggregate issues across all pages
    const issueCount = {};
    validResults.forEach(r => {
        r.issues.forEach(issue => {
            issueCount[issue] = (issueCount[issue] || 0) + 1;
        });
    });
    const topIssues = Object.entries(issueCount)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 20)
        .map(([issue, count]) => ({ issue, count, percent: ((count / validResults.length) * 100).toFixed(1) + '%' }));

    console.log(`  Overall Score: ${avgScore}/100`);
    console.log(`  Pages audited: ${validResults.length}`);
    console.log(`  Pages with errors: ${errorPages.length}`);

    const files = getReportFilename('technical-audit', domain);
    const reportData = {
        meta: { siteUrl: siteUrl || targetSitemap, sitemapUrl: targetSitemap, pagesAudited: validResults.length, avgScore, generatedAt: new Date().toISOString() },
        topIssues,
        worstPages: validResults.slice(0, 30),
        errorPages: errorPages.slice(0, 20),
        allResults: validResults
    };

    await saveJsonReport(files.json, reportData);

    // Markdown
    let md = `# 🔧 Technical SEO Audit — ${domain}\n\n`;
    md += `- **Overall Score**: **${avgScore}/100** ${avgScore >= 80 ? '🟢' : avgScore >= 50 ? '🟡' : '🔴'}\n`;
    md += `- **Pages Audited**: ${validResults.length}\n`;
    md += `- **Pages with HTTP errors**: ${errorPages.length}\n`;
    md += `- **Generated**: ${new Date().toISOString()}\n\n`;

    md += `## 🚨 Top Issues (sắp xếp theo tần suất)\n\n`;
    md += mdTable(
        ['Issue', 'Số trang bị ảnh hưởng', '% tổng'],
        ['issue', 'count', 'percent'],
        topIssues
    );

    md += `\n## 📉 Worst ${Math.min(validResults.length, 20)} Pages (Score thấp nhất)\n\n`;
    md += mdTable(
        ['Score', 'Page', 'Pass/Total', 'Issues chính'],
        ['score', 'url', '_passInfo', '_topIssue'],
        validResults.slice(0, 20).map(r => ({
            ...r,
            score: `${r.score}/100 ${r.score >= 80 ? '🟢' : r.score >= 50 ? '🟡' : '🔴'}`,
            _passInfo: `${r.passed}/${r.total}`,
            _topIssue: r.issues.slice(0, 2).join('; ') || 'None'
        })),
        { url: (v) => `[${shortUrl(v, siteUrl)}](${v})` }
    );

    if (errorPages.length > 0) {
        md += `\n## ⚠️ HTTP Error Pages\n\n`;
        md += mdTable(
            ['URL', 'Status Code'],
            ['url', 'statusCode'],
            errorPages,
            { url: (v) => `[${shortUrl(v, siteUrl)}](${v})` }
        );
    }

    // Agent Instructions — actionable remediation for project agents
    const agentActions = [];

    // Map top issues → agent-friendly actions
    const issueToAction = {
        'Thiếu thẻ <title>': { priority: 'P0-CRITICAL', title: 'Thêm title tag', description: 'Thêm thẻ <title> vào <head> cho các trang thiếu.', files: 'Layout/Page components (metadata export)' },
        'Thiếu meta description': { priority: 'P0-CRITICAL', title: 'Thêm meta description', description: 'Thêm meta description (120-160 chars) phù hợp với nội dung trang.', files: 'Layout/Page components (metadata export)' },
        'Thiếu H1': { priority: 'P1-HIGH', title: 'Thêm H1 tag', description: 'Đảm bảo mỗi trang có đúng 1 thẻ H1 mô tả nội dung chính.', files: 'Page components' },
        'Thiếu canonical tag': { priority: 'P1-HIGH', title: 'Thêm canonical tag', description: 'Thêm <link rel="canonical"> trỏ về URL chính, tránh duplicate content.', files: 'Layout/Head component' },
        'Không có JSON-LD structured data': { priority: 'P1-HIGH', title: 'Thêm JSON-LD Schema', description: 'Thêm structured data (Article, BreadcrumbList, Organization...) vào <head>.', files: 'Layout/Page components' },
        'Thiếu viewport meta — không mobile-friendly': { priority: 'P0-CRITICAL', title: 'Thêm viewport meta', description: 'Thêm <meta name="viewport" content="width=device-width, initial-scale=1">.', files: 'Root layout' },
    };

    topIssues.forEach(issue => {
        // Match exact or partial
        const matchedKey = Object.keys(issueToAction).find(k => issue.issue.includes(k));
        if (matchedKey) {
            agentActions.push({
                ...issueToAction[matchedKey],
                details: `${issue.count} trang bị ảnh hưởng (${issue.percent})`
            });
        } else {
            // Generic action for unmatched issues
            agentActions.push({
                priority: issue.count > validResults.length * 0.5 ? 'P1-HIGH' : 'P2-MEDIUM',
                title: `Fix: ${issue.issue}`,
                description: `Khắc phục lỗi "${issue.issue}" trên ${issue.count} trang.`,
                files: 'Tùy theo component gây lỗi',
                details: `${issue.count} trang (${issue.percent})`
            });
        }
    });

    // Add page-specific actions for worst pages
    validResults.slice(0, 5).forEach(page => {
        if (page.score < 80 && page.issues.length > 0) {
            agentActions.push({
                priority: page.score < 50 ? 'P0-CRITICAL' : 'P2-MEDIUM',
                title: `Optimize page: ${shortUrl(page.url, siteUrl)}`,
                description: `Score ${page.score}/100. Fix: ${page.issues.join('; ')}`,
                files: `Page route handling: ${shortUrl(page.url, siteUrl)}`
            });
        }
    });

    md += buildAgentInstructions(agentActions);

    await saveMarkdownReport(files.md, md);
    return reportData;
}

module.exports = { run };
