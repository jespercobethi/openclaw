$json = Get-Content 'C:\Users\xuan1\.openclaw\openclaw.json' -Raw | ConvertFrom-Json
$json.models.providers.PSObject.Properties.Remove('zai')
$json.agents.defaults.models.PSObject.Properties.Remove('zai/glm-4.7')
$json.auth.profiles.PSObject.Properties.Remove('zai:default')
$json.plugins.entries.PSObject.Properties.Remove('zai')
$json | ConvertTo-Json -Depth 20 | Set-Content 'C:\Users\xuan1\.openclaw\openclaw.json' -Encoding UTF8
Write-Host "Done - ZAI removed"
