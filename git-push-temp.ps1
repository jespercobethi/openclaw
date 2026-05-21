Set-Location 'C:\Users\xuan1\.openclaw\workspace\main'
git add -A
$date = Get-Date -Format 'yyyy-MM-dd HH:mm'
git commit -m "自动推送 $date"
git push origin main
