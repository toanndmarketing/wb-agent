---
name: speckit.nextjs-pseo
description: Quy trình & Blueprint tạo website Programmatic SEO (pSEO) và Onpage cơ bản bằng Next.js.
---

## 🎯 Mission
Cung cấp một Blueprint (Bộ tiêu chuẩn và cấu trúc) để xây dựng các website Programmatic SEO (pSEO) tối ưu, xử lý hàng vạn URLs tĩnh/động mượt mà bằng Next.js App Router, tuân thủ chặt chẽ các luật định trong `speckit.seo-technical`.

## 📥 Tình huống sử dụng
- Khi User yêu cầu: "Khởi tạo một website pSEO mới", "Làm trang vệ tinh", "Tạo thư mục Programmatic SEO cho dự án".
- Khi cần Agent (đặc biệt là `speckit.implement`) tự động generate code nền tảng (boilerplate) cho một dự án Next.js tập trung vào SEO.

## 📋 Core Architecture & Code Snippets

### 1. Cấu hình cốt lõi (next.config.ts)
BẮT BUỘC thiết lập `trailingSlash: true` để tạo ra "Pure Silo Pretty URLs" (VD: `/path/` thay vì `/path`), diệt triệt để lỗi redirect chain 308.
Định cấu hình `rewrites` và `redirects` linh hoạt để xử lý fallback SEO khi cấu trúc đổi.

```typescript
// next.config.ts
const nextConfig = {
    output: 'standalone',
    trailingSlash: true, // QUAN TRỌNG: Đồng nhất URL SEO
    // ...
};
export default nextConfig;
```

### 2. Sinh Metadata Động (Dynamic Metadata)
Trên các trang pSEO sinh hàng loạt (Ví dụ: `app/[slug]/page.tsx`), cấm dùng chung metadata.
Bắt buộc xây dựng thư viện `lib/seo/metadata.ts` gồm các hàm chuyên dụng:
- `generateSEOMetadata(data)`
- `generateOpenGraph(data)`
- `sanitizeMetaTitle(title: string)`: Chống ký tự lạ, giới hạn độ dài.
- `sanitizeMetaDescription(desc: string)`: Tránh nhồi nhét từ khóa, cắt đúng độ dài chuẩn (120-158 ký tự).

Mẫu khai báo trong `page.tsx`:
```tsx
import type { Metadata } from 'next';
import { generateSEOMetadata, sanitizeMetaTitle, sanitizeMetaDescription } from '@/lib/seo/metadata';

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const data = await fetchData(slug);
    if (!data) return { title: 'Not Found' };

    const seo = generateSEOMetadata({ data });
    
    return {
        title: { absolute: sanitizeMetaTitle(seo.title) },
        description: sanitizeMetaDescription(seo.description),
        alternates: { canonical: seo.canonical }, // ĐẢM BẢO CÓ TRAILING SLASH
    };
}
```

### 3. Dynamic Sitemap Index (Giải quyết ngưỡng 10k URLs)
Không nhồi nhét tất cả URL vào 1 file `sitemap.xml` vì sẽ gây timeout trên các hệ thống Serverless/Cloudflare Worker.
BẮT BUỘC sử dụng cấu trúc Route Handler cho Sitemap (VD: `app/sitemap.xml/route.ts`).
Lấy `total` record từ API (hoặc DB), chia cho `ITEMS_PER_SITEMAP = 10000`, tạo `<sitemapindex>` XML trả về danh sách các Sub-sitemap (VD: `/sitemap/posts-1.xml`, `/sitemap/posts-2.xml`).

```typescript
// app/sitemap.xml/route.ts
import { NextResponse } from 'next/server';
import { SITE_URL } from '@/lib/config';

const ITEMS_PER_SITEMAP = 10000; // Ngưỡng an toàn

export async function GET() {
    let total = await fetchTotalRecords();
    const pages = Math.ceil(total / ITEMS_PER_SITEMAP) || 1;
    
    const sitemaps = ['core']; // Trang tĩnh
    for (let i = 1; i <= pages; i++) sitemaps.push(`posts-${i}`);

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemaps.map((id) => `  <sitemap>
    <loc>${SITE_URL}/sitemap/${id}.xml</loc>
  </sitemap>`).join('\n')}
</sitemapindex>`;

    return new NextResponse(xml, { headers: { 'Content-Type': 'application/xml' } });
}
```

### 4. Structured Data (JSON-LD)
Tuyệt đối không dùng Microdata inline trực tiếp vào HTML. Bắt buộc tạo các React Component tách biệt cho Schema, và tiêm bằng `dangerouslySetInnerHTML`.

```tsx
export function EntitySchema({ entity }) {
    const schema = {
        '@context': 'https://schema.org',
        '@type': 'LocalBusiness', // Hoặc Article, Product...
        name: entity.name,
        // ...
    };
    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
    );
}
```

### 5. GEO Direct Answer Box (Tối ưu AI Search & Hợp Nhất Hero Subtitle)
Nhằm đón đầu xu hướng Generative Engine Optimization (AI Overviews, ChatGPT Search, Perplexity). Trên trang chủ, trang Pillar, hoặc trang cụm (Cluster):
- **QUY TẮC HỢP NHẤT (CONSOLIDATED GEO HERO)**: BẮT BUỘC hợp nhất đoạn mô tả chính (Subtitle) dưới H1 vào làm CHÍNH khung `<GeoDirectAnswer html="..." />`.
- **CẤM TRÙNG LẶP**: TUYỆT ĐỐI CẤM tách rời 1 đoạn `<p>` mô tả thô riêng biệt rồi lại chèn thêm 1 box GEO trùng lặp bên dưới gây rác UI, lặp từ ngữ và lãng phí không gian hiển thị.
- **Tác dụng kép**: Khung GEO Direct Answer vừa làm chức năng mô tả trang dẫn dắt mượt mà cho người dùng (UI Glassmorphism), vừa là khối Fact-Dense Answer cô đọng để AI Search Crawlers bóc tách làm Featured Snippet.

```tsx
export function GeoDirectAnswer({ html }: { html: string }) {
    return (
        <div className="geo-direct-answer border-l-4 border-cyan pl-4 py-3 bg-cyan/5 italic my-4 rounded-r-xl text-foreground-secondary leading-relaxed">
            <div dangerouslySetInnerHTML={{ __html: html }} />
        </div>
    );
}
```

### 6. Cấu trúc Revalidation & ISR
Hệ thống pSEO yêu cầu build cực nhanh và khả năng cập nhật dữ liệu liên tục. Bắt buộc sử dụng Incremental Static Regeneration (ISR).
- Khai báo `export const revalidate = 3600;` trên các trang Detail/Listing.
- Dùng cấu hình fetch caching `fetch(url, { next: { revalidate: 3600 } })` khi gọi API nội bộ hoặc external.
- **Xử lý lỗi Soft 404 (Quan trọng)**: Trong các trang SSR/ISR, nếu API không trả về dữ liệu cho slug, BẮT BUỘC gọi hàm `notFound()` của `next/navigation` để server trả về mã `HTTP 404` thực sự. Tuyệt đối không render giao diện lỗi kèm HTTP 200.

### 7. Tech Stack & Version Lock (Chống xung đột & Lỗ hổng)
Đối với các dự án pSEO xử lý dữ liệu nặng (Data Heavy), việc chốt version chuẩn xác giúp tránh lỗi Memory Leak, xung đột ORM, và lỗ hổng CVE trên server. Bắt buộc tuân thủ:
- **Node.js**: `v22 LTS` (Tối ưu fetch/caching tốt nhất cho Next.js, không dùng bản thử nghiệm).
- **Next.js**: `v15.x` (Trưởng thành về App Router, ổn định về ISR).
- **Database**: `postgres:16-alpine` (Bản 16 LTS siêu nhẹ an toàn, không lộ port public).
- **Caching**: `redis:7.2-alpine` (Dùng để cache kết quả SQL / Tính toán tần suất, chống nghẽn DB).
- **ORM**: `Drizzle ORM` bản stable (Tuyệt đối ưu tiên Drizzle thay vì Prisma cho các hệ toán xác suất nặng để tối ưu query Raw SQL).

## 🚫 Guard Rails (Quy định nghiêm ngặt)
- **Anchor Text Tinh Khiết (Anti Block-level Link)**: KHÔNG BAO GIỜ sinh ra Component có thẻ `<a>` bọc toàn bộ khối giao diện như `<Card>`. Áp dụng Pseudo-element trick: Thẻ `<a>` chỉ bọc thẻ tiêu đề (H2/H3) và kèm class Tailwind `after:absolute after:inset-0 focus:outline-none` (Đòi hỏi container cha phải có `relative`).
- **Dynamic Image Alt**: 100% hình ảnh chèn vào page động phải có thuộc tính `alt` sinh tự động có ngữ nghĩa (VD: `alt={\`Best \${category} in \${location}\`}`).
- **Tuyệt đối URL**: Luôn kiểm tra biến môi trường (`NEXT_PUBLIC_SITE_URL`) khi build Canonical, sitemap và OpenGraph. URL SEO BẮT BUỘC phải là Absolute URL (`https://...`).
- ☯️ **Quy tắc Phong Thủy UI/UX (BẮT BUỘC)**: Mọi UI/CSS (Tailwind) sinh ra phải dùng hệ màu Thủy sinh Mộc (Background Đen/Xanh đen, Accent Xanh dương/Xanh lá). CẤM dùng màu nền Trắng/Xám bạc (Kim), Đỏ/Cam (Hỏa) ở các mảng khối lớn. Các góc viền (border-radius) phải bo tròn mềm mại (`rounded-xl/2xl/full`), không dùng góc vuông sắc nhọn.
 
 