-- =============================================================================
-- Google SEO Tool - Brand Branches Name & Meta Optimizer
-- Giải quyết triệt để lỗi Keyword Cannibalization giữa các chi nhánh cùng Brand
-- =============================================================================

-- Bước 1: Tạo bảng tạm lưu thông tin tên mới đã tối ưu hóa
CREATE TEMP TABLE temp_optimized_names AS
SELECT 
    r.id,
    b.name AS brand_name,
    r.city,
    -- Trích xuất tên đường sạch từ địa chỉ
    REGEXP_REPLACE(
        REGEXP_REPLACE(
            SPLIT_PART(r.address, ',', 1), 
            '^[0-9\-]+\s+', 
            ''
        ), 
        '\s+(Suite|Ste|Spc|Unit|Store|Bldg|Pad|Apt|#).*$', 
        '', 
        'i'
    ) AS street_name
FROM "Restaurant" r
JOIN "Brand" b ON r."brandId" = b.id;

-- Bước 2: Cập nhật tên và Meta SEO cho Restaurant dựa trên bảng tạm
UPDATE "Restaurant" r
SET 
    name = t.brand_name || ' - ' || r.city || ' (' || t.street_name || ')',
    "metaTitle" = t.brand_name || ' - ' || r.city || ' (' || t.street_name || ') | Menu, Hours & Reviews - TasteHi',
    "metaDescription" = 'Visit ' || t.brand_name || ' in ' || r.city || ' (' || t.street_name || '), Hawaii. View the official menu, guest ratings, reviews, address map, phone, and operating hours.',
    "isSeoOptimizedByAgent" = true
FROM temp_optimized_names t
WHERE r.id = t.id;

-- Bước 3: Dọn dẹp bảng tạm
DROP TABLE temp_optimized_names;

-- Bước 4: Kiểm tra kết quả cập nhật
SELECT name, "metaTitle", "metaDescription" 
FROM "Restaurant" 
WHERE "brandId" IS NOT NULL 
LIMIT 10;
