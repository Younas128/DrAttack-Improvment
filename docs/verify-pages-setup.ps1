#!/usr/bin/env powershell
# GitHub Pages & Custom Domain Verification Script
# Run this after enabling Pages and configuring DNS

param(
    [string]$Domain = "DrAttack.io",
    [string]$GitHubPagesURL = "https://younas128.github.io/DrAttack-Improvment/"
)

Write-Host "=== GitHub Pages & Custom Domain Verification ===" -ForegroundColor Cyan
Write-Host ""

# Check 1: GitHub Pages URL
Write-Host "1. Checking GitHub Pages URL..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $GitHubPagesURL -ErrorAction Stop
    Write-Host "   ✅ GitHub Pages is LIVE" -ForegroundColor Green
    Write-Host "   Status: $($response.StatusCode) $($response.StatusDescription)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ GitHub Pages returned error" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Response.StatusCode) $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
    Write-Host "   Fix: Go to Settings > Pages and verify:" -ForegroundColor Yellow
    Write-Host "        - Source branch: gh-pages" -ForegroundColor Yellow
    Write-Host "        - Folder: / (root)" -ForegroundColor Yellow
}
Write-Host ""

# Check 2: Custom Domain DNS
Write-Host "2. Checking DNS for $Domain..." -ForegroundColor Yellow
try {
    $dnsRecords = Resolve-DnsName -Name $Domain -Type A -ErrorAction Stop | Select-Object -ExpandProperty IPAddress
    Write-Host "   ✅ DNS A records found:" -ForegroundColor Green
    $dnsRecords | ForEach-Object { Write-Host "      - $_" -ForegroundColor Green }
    
    # Verify GitHub Pages IP range
    $githubIPs = @("185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153")
    $validIPs = $dnsRecords | Where-Object { $_ -in $githubIPs }
    if ($validIPs) {
        Write-Host "   ✅ DNS points to GitHub Pages" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  DNS does not point to GitHub Pages IPs" -ForegroundColor Yellow
        Write-Host "   Expected one of: $($githubIPs -join ', ')" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ DNS lookup failed or not configured" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Fix: Add A records at your domain registrar:" -ForegroundColor Yellow
    Write-Host "        185.199.108.153" -ForegroundColor Yellow
    Write-Host "        185.199.109.153" -ForegroundColor Yellow
    Write-Host "        185.199.110.153" -ForegroundColor Yellow
    Write-Host "        185.199.111.153" -ForegroundColor Yellow
}
Write-Host ""

# Check 3: Custom Domain HTTP
Write-Host "3. Checking custom domain $Domain..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "https://$Domain/" -ErrorAction Stop
    Write-Host "   ✅ Custom domain is LIVE" -ForegroundColor Green
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Custom domain not accessible" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "   Possible fixes:" -ForegroundColor Yellow
    Write-Host "        1. Wait for DNS to propagate (up to 48 hours)" -ForegroundColor Yellow
    Write-Host "        2. Verify GitHub Pages is enabled at Settings > Pages" -ForegroundColor Yellow
    Write-Host "        3. Verify custom domain is set in Pages settings" -ForegroundColor Yellow
}
Write-Host ""

# Check 4: HTTPS/SSL
Write-Host "4. Checking HTTPS certificate..." -ForegroundColor Yellow
try {
    $request = [System.Net.HttpWebRequest]::Create("https://$Domain/")
    $request.ServerCertificateValidationCallback = { $true }
    $response = $request.GetResponse()
    $cert = $request.ServicePoint.Certificate
    Write-Host "   ✅ HTTPS is enabled" -ForegroundColor Green
    Write-Host "   Certificate Subject: $($cert.Subject)" -ForegroundColor Green
    Write-Host "   Issuer: $($cert.Issuer)" -ForegroundColor Green
    $response.Close()
} catch {
    Write-Host "   ⚠️  HTTPS not yet provisioned" -ForegroundColor Yellow
    Write-Host "   This is normal if you just configured DNS" -ForegroundColor Yellow
    Write-Host "   GitHub Pages will auto-provision SSL in 1-5 minutes" -ForegroundColor Yellow
}
Write-Host ""

# Check 5: Asset Loading (index.html sample)
Write-Host "5. Checking asset loading..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $GitHubPagesURL -ErrorAction Stop
    $content = $response.Content
    
    if ($content -match '<img') {
        Write-Host "   ✅ Images referenced in HTML" -ForegroundColor Green
    }
    if ($content -match '<link.*css') {
        Write-Host "   ✅ CSS files referenced" -ForegroundColor Green
    }
    if ($content -match '<script') {
        Write-Host "   ✅ JavaScript files referenced" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠️  Could not verify assets" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Check the items above. All should show ✅ for a fully working site." -ForegroundColor White
Write-Host ""
Write-Host "Documentation: docs/GITHUB_PAGES_SETUP.md" -ForegroundColor Gray
Write-Host ""
