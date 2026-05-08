$filePath = 'C:\Users\xuan1\.openclaw\media\inbound\基于多电机驱动的大型风电变桨伺服系统研究---ba0e1272-0dd2-4ca5-a6c1-7db8f38706ea.docx'
$outPath = 'C:\Users\xuan1\.openclaw\workspace\main\temp_doc_text.txt'

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($filePath, $false, $true)
    $text = $doc.Content.Text
    $doc.Close($false)
    $word.Quit()
    [System.IO.File]::WriteAllText($outPath, $text, [System.Text.Encoding]::UTF8)
    Write-Output "SUCCESS"
} catch {
    Write-Output "ERROR: $_"
    try { $word.Quit() } catch {}
}
