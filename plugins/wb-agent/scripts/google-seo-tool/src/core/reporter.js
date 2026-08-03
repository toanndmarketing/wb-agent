/**
 * Reporter — Markdown + JSON report generator
 * Shared across tất cả modules
 */
const fs = require('fs').promises;
const { existsSync } = require('fs');
const path = require('path');
const { ROOT_DIR } = require('./env');

const REPORTS_DIR = path.join(ROOT_DIR, 'reports');
let _customOutputDir = null;

/**
 * Set custom output directory (từ --output-dir flag)
 */
function setOutputDir(dir) {
    _customOutputDir = dir;
}

/**
 * Lấy output directory hiện tại
 */
function getOutputDir() {
    return _customOutputDir || REPORTS_DIR;
}

/**
 * Đảm bảo thư mục reports tồn tại
 */
async function ensureReportsDir() {
    const dir = getOutputDir();
    if (!existsSync(dir)) {
        await fs.mkdir(dir, { recursive: true });
    }
}

/**
 * Tạo tên file report theo format chuẩn
 */
function getReportFilename(moduleName, domain) {
    const dir = getOutputDir();
    const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
    return {
        md: path.join(dir, `${moduleName}-${domain}-${timestamp}.md`),
        json: path.join(dir, `${moduleName}-${domain}-${timestamp}.json`)
    };
}

/**
 * Lưu report JSON
 */
async function saveJsonReport(filepath, data) {
    await ensureReportsDir();
    await fs.writeFile(filepath, JSON.stringify(data, null, 2), 'utf8');
    console.log(`[✓] JSON saved: ${path.basename(filepath)}`);
}

/**
 * Lưu report Markdown
 */
async function saveMarkdownReport(filepath, content) {
    await ensureReportsDir();
    await fs.writeFile(filepath, content, 'utf8');
    console.log(`[✓] Report saved: ${path.basename(filepath)}`);
}

/**
 * Tạo Markdown table từ array of objects
 * @param {string[]} headers - Display headers
 * @param {string[]} keys - Object keys tương ứng
 * @param {object[]} rows - Data rows
 * @param {object} formatters - Custom formatters per key { key: (value) => string }
 */
function mdTable(headers, keys, rows, formatters = {}) {
    if (!rows || rows.length === 0) {
        return `| ${headers.join(' | ')} |\n| ${headers.map(() => ':---').join(' | ')} |\n| ${headers.map(() => '-').join(' | ')} |\n`;
    }

    let md = `| ${headers.join(' | ')} |\n`;
    md += `| ${headers.map(() => ':---').join(' | ')} |\n`;

    rows.forEach(row => {
        const cells = keys.map(key => {
            const val = row[key];
            if (formatters[key]) return formatters[key](val, row);
            if (val === undefined || val === null) return '-';
            return String(val);
        });
        md += `| ${cells.join(' | ')} |\n`;
    });

    return md;
}

/**
 * Format CTR (0.03 → 3.0%)
 */
function fmtCTR(val) {
    if (typeof val !== 'number') return '-';
    return (val * 100).toFixed(1) + '%';
}

/**
 * Format position
 */
function fmtPos(val) {
    if (typeof val !== 'number') return '-';
    return `**${val.toFixed(1)}**`;
}

/**
 * Format percentage change
 */
function fmtChange(val) {
    if (typeof val !== 'number') return '-';
    const sign = val >= 0 ? '+' : '';
    const emoji = val >= 0 ? '📈' : '📉';
    return `${emoji} ${sign}${val.toFixed(1)}%`;
}

/**
 * Shorten URL cho display
 */
function shortUrl(url, siteUrl) {
    if (!url) return '-';
    if (siteUrl) {
        const short = url.replace(siteUrl, '/').replace(/^\/\//, '/');
        return short.length < 60 ? short : short.substring(0, 57) + '...';
    }
    try {
        const u = new URL(url);
        const p = u.pathname;
        return p.length < 50 ? p : p.substring(0, 47) + '...';
    } catch {
        return url.substring(0, 50);
    }
}

/**
 * Print header cho module khi chạy
 */
function printHeader(moduleName, config = {}) {
    console.log('══════════════════════════════════════════════════');
    console.log(`🔍 ${moduleName}`);
    if (config.siteUrl) console.log(`   Target: ${config.siteUrl}`);
    if (config.sitemapUrl) console.log(`   Sitemap: ${config.sitemapUrl}`);
    console.log(`   Time: ${new Date().toISOString()}`);
    console.log('══════════════════════════════════════════════════');
}

/**
 * Tạo section Agent Instructions cho cuối report
 * Agent của project đích sẽ đọc phần này để biết cần làm gì
 */
function buildAgentInstructions(actions) {
    if (!actions || actions.length === 0) return '';

    let md = `\n---\n\n## 🤖 AGENT INSTRUCTIONS\n\n`;
    md += `> Phần này dành cho AI Agent của project. Agent hãy đọc và thực thi theo thứ tự ưu tiên.\n\n`;

    actions.forEach((action, i) => {
        md += `### ${i + 1}. [${action.priority}] ${action.title}\n`;
        md += `- **File(s)**: ${action.files || 'N/A'}\n`;
        md += `- **Action**: ${action.description}\n`;
        if (action.details) md += `- **Chi tiết**: ${action.details}\n`;
        md += `\n`;
    });

    return md;
}

module.exports = {
    REPORTS_DIR,
    setOutputDir,
    getOutputDir,
    ensureReportsDir,
    getReportFilename,
    saveJsonReport,
    saveMarkdownReport,
    mdTable,
    fmtCTR,
    fmtPos,
    fmtChange,
    shortUrl,
    printHeader,
    buildAgentInstructions
};
