Set-Location 'C:\Users\xuan1\.openclaw\workspace\main'
git add -A
$date = Get-Date -Format 'yyyy-MM-dd HH:mm'
$msg = "auto push " + $date
git commit -m $msg
$retries = 0
$maxRetries = 3
while ($retries -lt $maxRetries) {
    $result = git push origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Output "Push OK"
        Write-Output $result
        exit 0
    }
    $retries++
    Write-Output "Push failed, retry $retries/$maxRetries"
    Start-Sleep -Seconds ($retries * 5)
}
Write-Output "Push failed after $maxRetries retries"
Write-Output $result
exit 1
