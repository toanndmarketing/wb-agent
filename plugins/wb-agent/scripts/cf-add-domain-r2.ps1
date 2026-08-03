param(
    [Parameter(Mandatory=$true)][string]$Domain,
    [Parameter(Mandatory=$true)][string]$AccountId,
    [Parameter(Mandatory=$true)][string]$R2Endpoint
)

$headers = @{
    "X-Auth-Email" = $env:CLOUDFLARE_EMAIL
    "X-Auth-Key"   = $env:CLOUDFLARE_API_KEY
    "Content-Type" = "application/json"
}

if (-not $env:CLOUDFLARE_EMAIL -or -not $env:CLOUDFLARE_API_KEY) {
    Write-Host "Error: CLOUDFLARE_EMAIL and CLOUDFLARE_API_KEY environment variables are required." -ForegroundColor Red
    exit 1
}

Write-Host "1. Adding zone $Domain to account $AccountId..."
$body = @{
    name = $Domain
    account = @{ id = $AccountId }
    type = "full"
} | ConvertTo-Json
$addZoneResponse = Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones" -Method Post -Headers $headers -Body $body -ErrorAction Stop

if (-not $addZoneResponse.success) {
    Write-Host "Failed to add zone." -ForegroundColor Red
    exit 1
}

$ZoneId = $addZoneResponse.result.id
$Nameservers = $addZoneResponse.result.name_servers -join ", "
Write-Host "Zone created successfully. ZoneID: $ZoneId" -ForegroundColor Green
Write-Host "Nameservers assigned: $Nameservers" -ForegroundColor Cyan

Write-Host "2. Adding CNAME record (cdn -> $R2Endpoint)..."
$cnameBody = @{
    type = "CNAME"
    name = "cdn"
    content = $R2Endpoint
    proxied = $true
} | ConvertTo-Json
$cnameResponse = Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/dns_records" -Method Post -Headers $headers -Body $cnameBody -ErrorAction SilentlyContinue

Write-Host "3. Applying SEO & Security configurations..."
# Tắt Bot Fight Mode, tắt AI Bot protection
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/bot_management" -Method Put -Headers $headers -Body '{"fight_mode":false,"ai_bots_protection":"disabled"}' -ErrorAction SilentlyContinue | Out-Null
# Bật Browser Integrity Check
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/settings/browser_check" -Method Patch -Headers $headers -Body '{"value":"on"}' -ErrorAction SilentlyContinue | Out-Null
# Đưa Security Level về Medium
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/settings/security_level" -Method Patch -Headers $headers -Body '{"value":"medium"}' -ErrorAction SilentlyContinue | Out-Null

Write-Host "Done! Please update the nameservers at your registrar to: $Nameservers" -ForegroundColor Green
