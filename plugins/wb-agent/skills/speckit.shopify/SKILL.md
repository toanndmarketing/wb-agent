---
name: speckit.shopify
description: Shopify theme/app development standards và Liquid templates
---

## 🎯 Mission
Thiết lập, phát triển và tối ưu giao diện Shopify Storefront sử dụng Liquid, Section Schema (Online Store 2.0) và vận hành Shopify CLI qua Docker để đồng bộ và deploy an toàn.

## 📥 Input
- `.agent/specs/[feature]/spec.md` (Design requirements)
- `.agent/specs/[feature]/plan.md` (Implementation details)
- `.env` (Chứa các cấu hình: `SHOPIFY_FLAG_STORE`, `SHOPIFY_CLI_THEME_TOKEN`, `SHOPIFY_THEME_ID`)

## 📋 Shopify Knowledge Base & Standards

### 1. Liquid Engine Syntax & Best Practices
- **Render vs Include**: Luôn dùng `{% render 'snippet-name' %}` thay vì `{% include %}` để cô lập scope biến và cải thiện hiệu năng load trang.
- **Filters**: Sử dụng các filter tối ưu cho media và styling:
  - Image: `{{ product.featured_image | image_url: width: 450 | image_tag: loading: 'lazy', alt: product.title }}`. Luôn chỉ định width/height và lazy load để tối ưu SEO LCP/CLS.
  - CSS/JS: `{{ 'theme.css' | asset_url | stylesheet_tag }}` và `{{ 'theme.js' | asset_url | javascript_tag }}`.
- **Loop Optimization**: Tránh lồng loops (`for` inside `for`). Sử dụng map hoặc lưu trữ mảng trung gian để giảm độ phức tạp tính toán O(N^2).
- **Whitespace Control**: Dùng `{%-` và `-%}` để xóa khoảng trắng thừa trong HTML output.

### 2. Online Store 2.0 Section Schema
- Mỗi Custom Section phải đi kèm thẻ `{% schema %}` chuẩn JSON định dạng để hỗ trợ Shopify Theme Editor kéo thả:
```json
{
  "name": "Custom Product Grid",
  "tag": "section",
  "class": "section-custom-grid",
  "limit": 1,
  "settings": [
    {
      "type": "text",
      "id": "heading",
      "label": "Heading Title",
      "default": "Sản phẩm nổi bật"
    },
    {
      "type": "range",
      "id": "products_to_show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 4,
      "label": "Số lượng sản phẩm"
    }
  ],
  "blocks": [
    {
      "type": "column",
      "name": "Feature Column",
      "settings": [
        {
          "type": "image_picker",
          "id": "image",
          "label": "Image Banner"
        },
        {
          "type": "url",
          "id": "link",
          "label": "Action Link"
        }
      ]
    }
  ],
  "presets": [
    {
      "name": "Custom Product Grid",
      "blocks": [
        { "type": "column" },
        { "type": "column" }
      ]
    }
  ]
}
```

### 3. Shopify Admin API / GraphQL Rules
- Khi tương tác dữ liệu (ví dụ: lấy Metafields, tạo sản phẩm nháp), sử dụng GraphQL Admin API qua endpoints:
  - Base URL: `https://{shop}.myshopify.com/admin/api/2026-07/graphql.json`
  - Header: `X-Shopify-Access-Token: {api_password}`
- **GraphQL Query Metafields Example**:
```graphql
query getProductMetafields($id: ID!) {
  product(id: $id) {
    title
    metafields(first: 10) {
      edges {
        node {
          namespace
          key
          value
        }
      }
    }
  }
}
```

### 4. Dockerized Shopify CLI Protocol
- **Định nghĩa Service Docker Compose**:
  Để chạy Shopify CLI không phụ thuộc host, dự án phải định nghĩa service `shopify` trong file `docker-compose.yml` (hoặc `.agent/memory/docker-compose.shopify.yml`):
  ```yaml
  services:
    shopify:
      image: ghcr.io/shopify/cli:latest
      volumes:
        - .:/app
      working_dir: /app
      environment:
        - SHOPIFY_CLI_THEME_TOKEN=${SHOPIFY_CLI_THEME_TOKEN}
        - SHOPIFY_FLAG_STORE=${SHOPIFY_FLAG_STORE}
  ```
- **Lệnh CLI qua Docker (PowerShell syntax)**:
  - **Login**: `docker compose run --rm shopify login --store=$env:SHOPIFY_FLAG_STORE`
  - **Start Dev Preview**: `docker compose run --rm --service-ports shopify theme dev --store=$env:SHOPIFY_FLAG_STORE --theme=$env:SHOPIFY_THEME_ID`
  - **Push Deploy Draft**: `docker compose run --rm shopify theme push --store=$env:SHOPIFY_FLAG_STORE --theme=$env:SHOPIFY_THEME_ID --development`
  - **Pull Code**: `docker compose run --rm shopify theme pull --store=$env:SHOPIFY_FLAG_STORE --theme=$env:SHOPIFY_THEME_ID`

## 📤 Output
- Sinh cấu trúc theme Shopify chuẩn (`assets/`, `layout/`, `sections/`, `snippets/`, `templates/`, `config/`, `locales/`).
- Các files JSON Section Schema và Liquid components hợp lệ.
- Lệnh deploy/push thành công thông qua Dockerized Shopify CLI.

## 🚫 Guard Rails
- KHÔNG sử dụng legacy CSS/JS libs cồng kềnh; ưu tiên Vanilla CSS và Native JavaScript.
- KHÔNG hardcode theme credentials hoặc tokens trực tiếp vào code; luôn luôn dùng biến môi trường.
- KHÔNG thay đổi settings schema của các sections mặc định khi chưa phân tích Blast Radius.