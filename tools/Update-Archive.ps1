# Run manually from PowerShell 7. It fetches new source refs and saves immutable
# copies of the public startup bundles. It does not deploy or start a game server.
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if ($projectRoot -ne 'E:\Codex\Projects\Moly-Viet') {
    throw "Unexpected project location: $projectRoot"
}

$runId = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH-mm-ss.fffffffZ')
$runRoot = Join-Path $projectRoot "updates\$runId"
$sources = @(
    @{ Name = 'taomee-server-leak-full'; Path = Join-Path $projectRoot 'archive\source\taomee-server-leak-full' },
    @{ Name = 'MoleRuffle'; Path = Join-Path $projectRoot 'archive\source\MoleRuffle' }
)
$clients = @(
    @{ Region = 'china'; Url = 'http://mole.61.com/Client.swf' },
    @{ Region = 'taiwan'; Url = 'https://mole.61.com.tw/Client.swf' }
)
$startupPaths = @(
    'Client.swf',
    'version/zzz_config.txt',
    'config/Server.xml',
    'resource/xml/logo/loadingWord.xml',
    'resource/xml/ext.xml',
    'resource/login/Login.swf',
    'resource/login/LoginHome.swf',
    'resource/ui/main_resource.swf',
    'module/external/logo/randomMC.swf',
    'dll/TaomeeCoreDLL.swf',
    'dll/ClientConfigDLL.swf',
    'dll/ClientCommonDLL.swf',
    'dll/ClientSocketDLL.swf',
    'dll/ClientAppDLL.swf'
)

New-Item -ItemType Directory -Path $runRoot -ErrorAction Stop | Out-Null
$sourceResults = @()
foreach ($source in $sources) {
    if (-not (Test-Path -LiteralPath (Join-Path $source.Path '.git'))) {
        throw "Git repository missing: $($source.Path)"
    }
    & git -C $source.Path fetch --all --tags
    if ($LASTEXITCODE -ne 0) { throw "git fetch failed: $($source.Name)" }
    $sourceResults += [pscustomobject]@{
        name = $source.Name
        checkout = (& git -C $source.Path rev-parse HEAD).Trim()
        origin = (& git -C $source.Path rev-parse origin/HEAD).Trim()
    }
}

$clientResults = @()
foreach ($client in $clients) {
    $baseUrl = $client.Url.Substring(0, $client.Url.Length - 'Client.swf'.Length)
    foreach ($relativePath in $startupPaths) {
        $target = Join-Path $runRoot "clients\$($client.Region)\$relativePath"
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        $url = $baseUrl + $relativePath
        Invoke-WebRequest -Uri $url -OutFile $target -TimeoutSec 45
        $bytes = [System.IO.File]::ReadAllBytes($target)
        if ($bytes.Length -eq 0 -or $bytes.Length -gt 50MB) {
            throw "Unexpected asset size: $url"
        }
        if ($relativePath.EndsWith('.swf') -and
            ($bytes.Length -lt 1024 -or [System.Text.Encoding]::ASCII.GetString($bytes, 0, 3) -notin @('FWS','CWS','ZWS'))) {
            throw "Downloaded content is not a valid SWF: $url"
        }
        $clientResults += [pscustomobject]@{
            region = $client.Region
            sourceUrl = $url
            relativePath = "clients/$($client.Region)/$relativePath"
            bytes = $bytes.Length
            sha256 = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
}

$manifest = [pscustomobject]@{
    capturedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    projectRoot = $projectRoot
    sources = $sourceResults
    clients = $clientResults
    note = 'Public startup assets only; no authenticated resources, no full playable game, no deployment.'
}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $runRoot 'manifest.json') -Encoding utf8
Write-Output "Archived update snapshot: $runRoot"
