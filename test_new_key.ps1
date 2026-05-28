$headers = @{
    "Authorization" = "Bearer tp-ctqr0sgkqxicfadd3wj6oipgzb0789g6u7xawcsho08ytllc"
    "Content-Type" = "application/json"
}

# Test mimo-v2-pro
$body1 = @{
    model = "mimo-v2-pro"
    messages = @(@{ role = "user"; content = "Hi" })
    max_tokens = 10
} | ConvertTo-Json -Compress

try {
    $r = Invoke-WebRequest -Uri "https://api.xiaomimimo.com/v1/chat/completions" -Method POST -Headers $headers -Body $body1 -TimeoutSec 15
    Write-Host "mimo-v2-pro OK: $($r.StatusCode)"
    Write-Host "Response: $($r.Content.Substring(0, [Math]::Min(300, $r.Content.Length)))"
} catch {
    Write-Host "mimo-v2-pro ERR: $($_.Exception.Message)"
}

# Test mimo-v2.5-pro
$body2 = @{
    model = "mimo-v2.5-pro"
    messages = @(@{ role = "user"; content = "Hi" })
    max_tokens = 10
} | ConvertTo-Json -Compress

try {
    $r2 = Invoke-WebRequest -Uri "https://token-plan-cn.xiaomimimo.com/v1/chat/completions" -Method POST -Headers $headers -Body $body2 -TimeoutSec 15
    Write-Host "mimo-v2.5-pro OK: $($r2.StatusCode)"
    Write-Host "Response: $($r2.Content.Substring(0, [Math]::Min(300, $r2.Content.Length)))"
} catch {
    Write-Host "mimo-v2.5-pro ERR: $($_.Exception.Message)"
}

# Test mimo-v2.5
$body3 = @{
    model = "mimo-v2.5"
    messages = @(@{ role = "user"; content = "Hi" })
    max_tokens = 10
} | ConvertTo-Json -Compress

try {
    $r3 = Invoke-WebRequest -Uri "https://token-plan-cn.xiaomimimo.com/v1/chat/completions" -Method POST -Headers $headers -Body $body3 -TimeoutSec 15
    Write-Host "mimo-v2.5 OK: $($r3.StatusCode)"
    Write-Host "Response: $($r3.Content.Substring(0, [Math]::Min(300, $r3.Content.Length)))"
} catch {
    Write-Host "mimo-v2.5 ERR: $($_.Exception.Message)"
}
