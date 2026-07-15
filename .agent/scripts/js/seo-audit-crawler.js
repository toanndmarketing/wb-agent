const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// Config
const DEFAULT_BASE_URL = 'http://localhost:8980';
const MAX_PAGES = 50;
const REPORT_PATH = path.resolve(__dirname, '../../memory/seo-audit-report.md');

class SeoCrawler {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.crawledUrls = new Set();
    this.queue = [];
    this.results = [];
  }

  async run() {
    console.log(`🚀 Bắt đầu quét SEO cho: ${this.baseUrl}`);
    console.log(`⚙️ Giới hạn quét tối đa: ${MAX_PAGES} trang\n`);

    this.queue.push(this.baseUrl);

    while (this.queue.length > 0 && this.crawledUrls.size < MAX_PAGES) {
      const url = this.queue.shift();
      const normalizedUrl = url.replace(/\/$/, '');
      if (this.crawledUrls.has(normalizedUrl)) continue;

      this.crawledUrls.add(normalizedUrl);
      console.log(`[${this.crawledUrls.size}/${MAX_PAGES}] Đang quét: ${url}`);

      try {
        const result = await this.auditPage(url);
        if (result) {
          this.results.push(result);
        }
      } catch (error) {
        console.error(`❌ Lỗi khi quét ${url}:`, error.message);
      }
    }

    this.generateReport();
  }

  async auditPage(url) {
    const startTime = Date.now();
    let response;

    try {
      response = await fetch(url, {
        headers: { 'User-Agent': 'SEO-Audit-Crawler/1.0' },
        signal: AbortSignal.timeout(10000),
      });
    } catch (e) {
      return {
        url,
        status: 0,
        title: { text: '', status: 'error', message: `Không thể kết nối: ${e.message}` },
        description: { text: '', status: 'error', message: 'Không khả dụng' },
        canonical: { text: '', status: 'error', message: 'Không khả dụng' },
        headings: { h1Count: 0, headingsList: [], status: 'error', message: 'Không khả dụng' },
        images: { total: 0, missingAlt: 0, missingAltList: [], status: 'error' },
        links: { internalCount: 0, externalCount: 0 },
        loadTimeMs: Date.now() - startTime,
      };
    }

    const loadTimeMs = Date.now() - startTime;
    const status = response.status;

    if (status !== 200) {
      return {
        url,
        status,
        title: { text: '', status: 'error', message: `Mã phản hồi lỗi: ${status}` },
        description: { text: '', status: 'error', message: 'Không khả dụng' },
        canonical: { text: '', status: 'error', message: 'Không khả dụng' },
        headings: { h1Count: 0, headingsList: [], status: 'error', message: 'Không khả dụng' },
        images: { total: 0, missingAlt: 0, missingAltList: [], status: 'error' },
        links: { internalCount: 0, externalCount: 0 },
        loadTimeMs,
      };
    }

    const html = await response.text();
    const $ = cheerio.load(html);

    // Title
    const titleText = $('title').text().trim();
    let titleStatus = 'passed';
    let titleMsg = 'Đạt yêu cầu';
    if (!titleText) {
      titleStatus = 'error';
      titleMsg = 'Thiếu thẻ <title>!';
    } else if (titleText.length < 30) {
      titleStatus = 'warning';
      titleMsg = `Tiêu đề ngắn (${titleText.length} ký tự). Nên từ 30-60 ký tự.`;
    } else if (titleText.length > 60) {
      titleStatus = 'warning';
      titleMsg = `Tiêu đề dài (${titleText.length} ký tự). Nên từ 30-60 ký tự.`;
    }

    // Description
    const descText = $('meta[name="description"]').attr('content')?.trim() || '';
    let descStatus = 'passed';
    let descMsg = 'Đạt yêu cầu';
    if (!descText) {
      descStatus = 'error';
      descMsg = 'Thiếu thẻ <meta name="description">!';
    } else if (descText.length < 120) {
      descStatus = 'warning';
      descMsg = `Mô tả ngắn (${descText.length} ký tự). Nên từ 120-160 ký tự.`;
    } else if (descText.length > 160) {
      descStatus = 'warning';
      descMsg = `Mô tả dài (${descText.length} ký tự). Nên từ 120-160 ký tự.`;
    }

    // Canonical
    const canonical = $('link[rel="canonical"]').attr('href')?.trim() || '';
    let canonicalStatus = 'passed';
    let canonicalMsg = 'Đạt yêu cầu';
    if (!canonical) {
      canonicalStatus = 'error';
      canonicalMsg = 'Thiếu thẻ canonical!';
    } else {
      try {
        const absoluteCanonical = new URL(canonical, url).href;
        const u1 = new URL(absoluteCanonical);
        const u2 = new URL(url);
        const pathsMatch = u1.pathname === u2.pathname && u1.search === u2.search;
        
        if (!pathsMatch) {
          canonicalStatus = 'warning';
          canonicalMsg = `Canonical trỏ về URL khác: ${canonical}`;
        }
      } catch (e) {
        canonicalStatus = 'error';
        canonicalMsg = `Thẻ canonical chứa URL không hợp lệ: ${canonical}`;
      }
    }

    // Headings
    const headingsList = [];
    const h1s = $('h1');
    const h1Count = h1s.length;
    let headingStatus = 'passed';
    let headingMsg = 'Đạt yêu cầu';

    if (h1Count === 0) {
      headingStatus = 'error';
      headingMsg = 'Thiếu thẻ H1!';
    } else if (h1Count > 1) {
      headingStatus = 'warning';
      headingMsg = `Có nhiều thẻ H1 (${h1Count} thẻ). Chỉ nên có 1 thẻ H1 duy nhất.`;
    }

    $('h1, h2, h3, h4, h5, h6').each((_, el) => {
      headingsList.push({
        tag: el.name.toUpperCase(),
        text: $(el).text().trim().replace(/\s+/g, ' '),
      });
    });

    // Images alt Check
    let totalImages = 0;
    let missingAlt = 0;
    const missingAltList = [];
    $('img').each((_, el) => {
      totalImages++;
      const alt = $(el).attr('alt');
      const src = $(el).attr('src') || '';
      if (alt === undefined || alt.trim() === '') {
        missingAlt++;
        missingAltList.push(src);
      }
    });
    const imageStatus = missingAlt > 0 ? 'warning' : 'passed';

    // Link extraction
    let internalCount = 0;
    let externalCount = 0;

    $('a').each((_, el) => {
      const href = $(el).attr('href')?.trim();
      if (!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) return;

      try {
        const resolvedUrl = new URL(href, url);
        const isInternal = resolvedUrl.hostname === new URL(this.baseUrl).hostname;

        if (isInternal) {
          internalCount++;
          const crawlUrl = resolvedUrl.origin + resolvedUrl.pathname;
          const normalizedCrawl = crawlUrl.replace(/\/$/, '');
          if (!this.crawledUrls.has(normalizedCrawl) && !this.queue.includes(crawlUrl) && this.crawledUrls.size + this.queue.length < MAX_PAGES * 2) {
            this.queue.push(crawlUrl);
          }
        } else {
          externalCount++;
        }
      } catch (e) {
        // Ignore invalid URLs
      }
    });

    return {
      url,
      status,
      title: { text: titleText, status: titleStatus, message: titleMsg },
      description: { text: descText, status: descStatus, message: descMsg },
      canonical: { text: canonical, status: canonicalStatus, message: canonicalMsg },
      headings: { h1Count, headingsList, status: headingStatus, message: headingMsg },
      images: { total: totalImages, missingAlt, missingAltList, status: imageStatus },
      links: { internalCount, externalCount },
      loadTimeMs,
    };
  }

  generateReport() {
    console.log(`\n📊 Đang biên soạn báo cáo SEO Audit...`);
    console.log(`
📊 Đang biên soạn báo cáo SEO Audit...`);

    const totalPages = this.results.length;
    let criticalErrors = 0;
    let warnings = 0;
    let totalLoadTime = 0;
    let totalImages = 0;
    let totalMissingAlt = 0;

    let totalScore = 0;
    this.results.forEach(r => {
      totalLoadTime += r.loadTimeMs;
      if (r.status !== 200) criticalErrors++;
      if (r.title.status === 'error') criticalErrors++;
      if (r.title.status === 'warning') warnings++;
      if (r.description.status === 'error') criticalErrors++;
      if (r.description.status === 'warning') warnings++;
      if (r.canonical.status === 'error') criticalErrors++;
      if (r.canonical.status === 'warning') warnings++;
      if (r.headings.status === 'error') criticalErrors++;
      if (r.headings.status === 'warning') warnings++;
      
      totalImages += r.images.total;
      totalMissingAlt += r.images.missingAlt;
      if (r.images.status === 'warning') warnings++;

      let pScore = 100;
      if (r.status !== 200) pScore -= 50;
      if (r.title.status === 'error') pScore -= 25;
      if (r.title.status === 'warning') pScore -= 5;
      if (r.description.status === 'error') pScore -= 25;
      if (r.description.status === 'warning') pScore -= 5;
      if (r.canonical.status === 'error') pScore -= 15;
      if (r.canonical.status === 'warning') pScore -= 5;
      if (r.headings.status === 'error') pScore -= 15;
      if (r.headings.status === 'warning') pScore -= 5;
      if (r.images.status === 'warning') pScore -= 5;
      totalScore += Math.max(0, pScore);
    });

    const avgLoadTime = totalPages > 0 ? (totalLoadTime / totalPages).toFixed(0) : '0';
    const altPercentage = totalImages > 0 ? (((totalImages - totalMissingAlt) / totalImages) * 100).toFixed(1) : '100';

    const score = totalPages > 0 ? Math.round(totalScore / totalPages) : 100;

    let scoreEmoji = '🔴';
    if (score >= 80) scoreEmoji = '🟢';
    else if (score >= 50) scoreEmoji = '🟡';

    const dir = path.dirname(REPORT_PATH);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    let md = `# 🔍 Báo cáo SEO Audit & Tối ưu hóa

`;
    md += `*   **Địa chỉ quét:** \`${this.baseUrl}\`
`;
    md += `*   **Thời gian thực hiện:** ${new Date().toLocaleString('vi-VN')}
`;
    md += `*   **Tổng số trang đã quét:** ${totalPages}
`;
    md += `*   **Tốc độ tải trang trung bình:** \`${avgLoadTime}ms\`
`;
    md += `*   **Điểm đánh giá SEO:** ${scoreEmoji} **${score}/100**

`;

    md += `## 📊 Chỉ số tổng quan

`;
    md += `| Chỉ số | Kết quả | Trạng thái |
`;
    md += `| :--- | :--- | :--- |
`;
    md += `| Lỗi nghiêm trọng (Critical) | **${criticalErrors}** | ${criticalErrors > 0 ? '🔴 Cần khắc phục ngay' : '🟢 Tuyệt vời'} |
`;
    md += `| Cảnh báo (Warnings) | **${warnings}** | ${warnings > 0 ? '🟡 Cần tối ưu thêm' : '🟢 Đạt chuẩn'} |
`;
    md += `| Tỷ lệ ảnh có thẻ Alt | **${altPercentage}%** (${totalImages - totalMissingAlt}/${totalImages} ảnh) | ${totalMissingAlt > 0 ? '🟡 Thiếu ' + totalMissingAlt + ' thẻ alt' : '🟢 Đạt chuẩn'} |

`;

    md += `## 📋 Chi tiết các trang đã quét

`;

    this.results.forEach((r, idx) => {
      const pageScore = r.status === 200 && r.title.status !== 'error' && r.description.status !== 'error' && r.headings.status !== 'error' ? '🟢 Đạt' : '🔴 Lỗi';
      md += `### ${idx + 1}. Trang: \`${r.url}\` (${pageScore})

`;
      md += `*   **Mã phản hồi HTTP:** \`${r.status}\` | **Tốc độ tải:** \`${r.loadTimeMs}ms\`
`;
      md += `*   **Meta Title:** ${r.title.status === 'passed' ? '🟢' : r.title.status === 'warning' ? '🟡' : '🔴'} \`${r.title.text || '(Trống)'}\` - *${r.title.message}*
`;
      md += `*   **Meta Description:** ${r.description.status === 'passed' ? '🟢' : r.description.status === 'warning' ? '🟡' : '🔴'} \`${r.description.text || '(Trống)'}\` - *${r.description.message}*
`;
      md += `*   **Thẻ Canonical:** ${r.canonical.status === 'passed' ? '🟢' : r.canonical.status === 'warning' ? '🟡' : '🔴'} \`${r.canonical.text || '(Trống)'}\` - *${r.canonical.message}*
`;
      md += `*   **Cấu trúc Headings (H1):** ${r.headings.status === 'passed' ? '🟢' : r.headings.status === 'warning' ? '🟡' : '🔴'} *${r.headings.message}* (Số lượng H1: ${r.headings.h1Count})
`;
      md += `*   **Hình ảnh:** ${r.images.status === 'passed' ? '🟢' : '🟡'} Có ${r.images.total} hình ảnh, thiếu ${r.images.missingAlt} thẻ mô tả Alt.
`;
      md += `*   **Liên kết nội bộ/ngoài:** \`${r.links.internalCount}\` links nội bộ / \`${r.links.externalCount}\` links ngoài.
`;

      if (r.images.missingAlt > 0) {
        md += `    *   *Danh sách ảnh thiếu thẻ alt (Tối đa hiển thị 3):*\n`;
        r.images.missingAltList.slice(0, 3).forEach(img => {
          md += `        *   \`${img}\`\n`;
        });
      }

      if (r.headings.headingsList.length > 0) {
        md += `    *   *Danh mục cấu trúc Heading:*\n`;
        r.headings.headingsList.slice(0, 6).forEach(h => {
          md += `        *   \`${h.tag}\`: ${h.text}\n`;
        });
        if (r.headings.headingsList.length > 6) {
          md += `        *   *...và ${r.headings.headingsList.length - 6} tiêu đề khác.*\n`;
        }
      }
      md += `\n---\n\n`;
    });

    md += `\n*Báo cáo được tạo tự động bởi SEO Audit Engine.*\n`;

    fs.writeFileSync(REPORT_PATH, md, 'utf8');
    console.log(`\n🎉 Đã ghi báo cáo SEO tại: \${REPORT_PATH}`);
  }
}

const targetUrl = process.argv[2] || DEFAULT_BASE_URL;
const crawler = new SeoCrawler(targetUrl);
crawler.run().catch(err => {
  console.error('Fatal crawler error:', err);
  process.exit(1);
});
