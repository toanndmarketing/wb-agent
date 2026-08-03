# Script cài đặt 1-Click Global Plugin cho wb-agent
$PluginPath = "$env:USERPROFILE\.gemini\config\plugins\wb-agent"
$RepoPath = $PSScriptRoot

if (-not (Test-Path "$env:USERPROFILE\.gemini\config\plugins")) {
    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini\config\plugins" | Out-Null
}

if (Test-Path $PluginPath) {
    Remove-Item -Recurse -Force $PluginPath -ErrorAction SilentlyContinue
}

New-Item -ItemType Junction -Path $PluginPath -Target $RepoPath | Out-Null

Write-Host "✅ Cài đặt wb-agent Global Plugin thành công!" -ForegroundColor Green
Write-Host "📍 Plugin Link: $PluginPath -> $RepoPath" -ForegroundColor Cyan
