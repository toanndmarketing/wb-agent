<RULE[pseo_audit_command]>
# Lệnh Workflow Tự Động: `/audit-pseo`

Khi người dùng nhập `/audit-pseo` hoặc yêu cầu "Kiểm tra kiến trúc pSEO", Agent BẮT BUỘC thực hiện luồng sau:

1. ĐỌC SKILL: `view_file` skill `pseo-location-geo` để nắm chuẩn Link Juice.
2. SUBAGENT QUÉT (Flash Model): Quét `trailingSlash`, `Breadcrumbs`, `JSON-LD`, và component `Sitemap`.
3. BÁO CÁO: Xuất file `pseo-audit-report.md` chỉ rõ chỗ nào hở Link Juice, chỗ nào Orphan Page và Đề xuất code sửa.
</RULE[pseo_audit_command]>
