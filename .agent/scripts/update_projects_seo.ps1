$projects = @(
    @{ path = "D:\Project\tastehi.com"; type = "fullstack" },
    @{ path = "D:\Project\phuquocaz.com"; type = "fullstack" },
    @{ path = "D:\Tuvi\toantuvi.com"; type = "fullstack" },
    @{ path = "D:\Project\thansohoctuoanh.com"; type = "fullstack" },
    @{ path = "D:\Project\ketsatgiadinh.vn"; type = "web_public" },
    @{ path = "D:\Project\apisport.online"; type = "fullstack" }
)

foreach ($proj in $projects) {
    $path = $proj.path
    $type = $proj.type
    if (Test-Path $path) {
        Write-Host "──────────────────────────────────────────────────"
        Write-Host "🚀 Updating SEO Standards & Knowledge for: $path (Type: $type)"
        Write-Host "──────────────────────────────────────────────────"
        
        Push-Location $path
        try {
            # 1. Khởi tạo/Nâng cấp cấu trúc .agent với các templates và skills mới
            wb-agent init --type $type --force
            
            # 2. Tải và chắt lọc tài liệu Google Search Central
            wb-agent learn-seo
            
            Write-Host "✅ Hoàn tất cập nhật SEO cho: $path`n"
        } catch {
            Write-Host "❌ Lỗi khi cập nhật $path : $_`n" -ForegroundColor Red
        }
        Pop-Location
    } else {
        Write-Host "⚠️ Không tìm thấy đường dẫn dự án: $path`n" -ForegroundColor Yellow
    }
}
