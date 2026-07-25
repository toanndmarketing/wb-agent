$ErrorActionPreference = "Stop"

# Xác định đường dẫn
$SourceDir = Join-Path $PSScriptRoot "plugins\wb-agent"
$TargetDir = Join-Path $env:USERPROFILE ".gemini\config\plugins\wb-agent"

Write-Host "⚡ Cài đặt WB-Agent Global Plugin..." -ForegroundColor Cyan

# 1. Kiểm tra Source
if (-not (Test-Path $SourceDir)) {
    Write-Host "❌ Lỗi: Không tìm thấy source plugin tại $SourceDir" -ForegroundColor Red
    Write-Host "Vui lòng chạy script này từ thư mục gốc của repository." -ForegroundColor Yellow
    pause
    exit 1
}

# 2. Đảm bảo Target tồn tại
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# 3. Copy (ghi đè)
try {
    Copy-Item -Path "$SourceDir\*" -Destination $TargetDir -Recurse -Force
    
    # Đếm số lượng skills đã copy
    $SkillsDir = Join-Path $TargetDir "skills"
    if (Test-Path $SkillsDir) {
        $Count = (Get-ChildItem -Path $SkillsDir -Directory).Count
        Write-Host "✅ Đã copy thành công $Count skills vào IDE hệ thống!" -ForegroundColor Green
        Write-Host "📁 Vị trí cài đặt: $TargetDir" -ForegroundColor Green
    }
}
catch {
    Write-Host "❌ Lỗi khi copy file: $_" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "`nQuá trình hoàn tất. Vui lòng khởi động lại IDE (nếu cần) để nhận plugin mới." -ForegroundColor Cyan
Start-Sleep -Seconds 3
