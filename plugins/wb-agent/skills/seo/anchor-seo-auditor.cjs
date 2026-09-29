const fs = require('fs');
const path = require('path');

const ANSI_RED = '\x1b[31m';
const ANSI_YELLOW = '\x1b[33m';
const ANSI_GREEN = '\x1b[32m';
const ANSI_RESET = '\x1b[0m';

let targetDir = 'src';
if (process.argv[2] && fs.existsSync(process.argv[2])) {
  targetDir = process.argv[2];
} else if (!fs.existsSync('src')) {
  targetDir = '.';
}

function walk(dir, cb) {
  if (!fs.existsSync(dir)) return;
  fs.readdirSync(dir).forEach(f => {
    if (f === 'node_modules' || f === '.git' || f === '.next' || f === 'dist' || f === 'build') return;
    let p = path.join(dir, f);
    fs.statSync(p).isDirectory() ? walk(p, cb) : cb(p);
  });
}

let totalFiles = 0;
let totalAnchors = 0;
let totalErrors = 0;
let fileErrors = {};

function logError(file, lineNum, rule, snippet) {
  if (!fileErrors[file]) fileErrors[file] = [];
  fileErrors[file].push({ lineNum, rule, snippet });
  totalErrors++;
}

console.log(`${ANSI_YELLOW}🔍 Bắt đầu quét Anchor Tag SEO (dựa theo constitution)...${ANSI_RESET}\n`);

walk(targetDir, (file) => {
  if (/\.(astro|tsx?|jsx?|mdx?|html)$/i.test(file)) {
    totalFiles++;
    let content = fs.readFileSync(file, 'utf8');
    
    // Tìm tất cả các thẻ <a> (mở đến đóng)
    const anchorRegex = /(<a\b[^>]*>)([\s\S]*?)<\/a>/gi;
    let match;
    
    while ((match = anchorRegex.exec(content)) !== null) {
      totalAnchors++;
      const fullTag = match[0];
      const openTag = match[1];
      const innerHtml = match[2];
      
      const lineNum = content.substring(0, match.index).split('\n').length;
      let hasError = false;

      // 1. Rule: Missing Title
      if (!/title\s*=/i.test(openTag)) {
        logError(file, lineNum, 'Missing Title', openTag);
        hasError = true;
      }

      // 2. Rule: Block-level Wrapping
      if (/<(div|section|article|p|ul|li|nav|header|footer)\b/i.test(innerHtml)) {
        logError(file, lineNum, 'Block-level Element Wrapped', fullTag.replace(/\r?\n/g, ' ').substring(0, 80) + '...');
        hasError = true;
      }

      // 3. Rule: Decorative Characters in Anchor Text
      const textWithoutAriaHidden = innerHtml.replace(/<span[^>]*aria-hidden=["']true["'][^>]*>[\s\S]*?<\/span>/gi, '');
      if (/(→|&rarr;|>>|&raquo;)/i.test(textWithoutAriaHidden) || /(→|&rarr;|>>|&raquo;)/i.test(openTag)) {
        logError(file, lineNum, 'Contains Decorative Characters without aria-hidden', fullTag.replace(/\r?\n/g, ' ').substring(0, 80) + '...');
        hasError = true;
      }

      // 4. Rule: Missing or Invalid Href
      if (!/href\s*=/i.test(openTag) || /href=["'](?:#|javascript:.*?)?["']/i.test(openTag)) {
        logError(file, lineNum, 'Invalid or Missing Href', openTag);
        hasError = true;
      }

      // 5. Rule: External Link Missing rel="noopener noreferrer"
      if (/href=["']https?:\/\//i.test(openTag)) {
        const relMatch = openTag.match(/rel=["']([^"']+)["']/i);
        const relValue = relMatch ? relMatch[1] : '';
        const hasNoopener = /\bnoopener\b/i.test(relValue);
        const hasNoreferrer = /\bnoreferrer\b/i.test(relValue);
        if (!hasNoopener || !hasNoreferrer) {
          logError(file, lineNum, 'External Link Missing rel="noopener noreferrer"', openTag);
          hasError = true;
        }
      }

      // 6. Rule: Empty Anchor Text
      const plainText = innerHtml.replace(/<[^>]*>/g, '').trim();
      if (plainText === '' && !/<img\b/i.test(innerHtml) && !/<svg\b/i.test(innerHtml)) {
        logError(file, lineNum, 'Empty Anchor Text (no visible text or image)', fullTag.replace(/\r?\n/g, ' ').substring(0, 80) + '...');
        hasError = true;
      }

      // 7. Rule: Image-only Link Missing Alt Text
      if (/<img\b/i.test(innerHtml)) {
        const imgRegex = /<img\b[^>]*>/gi;
        let imgMatch;
        let imgMissingAlt = false;
        while ((imgMatch = imgRegex.exec(innerHtml)) !== null) {
          const imgTag = imgMatch[0];
          if (!/alt\s*=/i.test(imgTag) || /alt=["']\s*["']/i.test(imgTag)) {
            imgMissingAlt = true;
            break;
          }
        }
        if (imgMissingAlt) {
          logError(file, lineNum, 'Image-only Link Missing Alt Text', fullTag.replace(/\r?\n/g, ' ').substring(0, 80) + '...');
          hasError = true;
        }
      }
    }
  }
});

// In kết quả
if (totalErrors === 0) {
  console.log(`${ANSI_GREEN}✅ Tuyệt vời! Toàn bộ thẻ <a> trong dự án đều tuân thủ 100% chuẩn SEO.${ANSI_RESET}`);
} else {
  console.log(`${ANSI_RED}❌ Phát hiện ${totalErrors} lỗi vi phạm chuẩn SEO thẻ <a>:${ANSI_RESET}\n`);
  
  for (const [file, errors] of Object.entries(fileErrors)) {
    console.log(`${ANSI_YELLOW}📁 File: ${file}${ANSI_RESET}`);
    errors.forEach(e => {
      console.log(`   L${e.lineNum} | [${ANSI_RED}${e.rule}${ANSI_RESET}] - ${e.snippet}`);
    });
    console.log('');
  }
}

console.log(`📊 Tổng: ${totalFiles} files quét | ${totalAnchors} thẻ <a> kiểm tra | ${totalErrors} lỗi phát hiện`);

if (totalErrors > 0) {
  process.exit(1);
}
