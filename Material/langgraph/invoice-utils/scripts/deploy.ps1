# Simulated staging deploy for the lab (Windows)
param([string]$Version = "0.1.0")

$distDir = "dist"
if (-not (Test-Path $distDir) -or -not (Get-ChildItem $distDir)) {
    Write-Error "dist/ is empty. Run 'uv build' first."
    exit 1
}

$artifacts = (Get-ChildItem $distDir | ForEach-Object { $_.Name }) -join " "
Write-Host "Deploying invoice-utils v$Version to staging..."
Write-Host "  Artifacts: $artifacts"
Write-Host "  Health check: OK"
Write-Host "  URL: https://staging.example.com/invoice-utils/$Version"
Write-Host "DEPLOY_SUCCESS"
