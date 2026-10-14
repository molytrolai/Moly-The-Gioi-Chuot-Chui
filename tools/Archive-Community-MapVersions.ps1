param(
    [string[]] $Variant = @(
        'era-1326446938',
        'era-1368182401',
        'era-1371204111',
        'era-1417156567',
        'era-1446620130',
        'tw-2016',
        'cn-2025-revival',
        '61p-2011-xmas',
        '61p-2012-cny'
    ),
    [string[]] $Asset = @(
        'resource/map/Map_10017.xml',
        'resource/map/Map_10017.swf',
        'resource/map/17.swf',
        'resource/map/Map_10019.xml',
        'resource/map/19.xml',
        'resource/map/Map_10019.swf',
        'resource/map/19.swf'
    )
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$projectRoot = Split-Path -Parent $PSScriptRoot
$archiveRoot = Join-Path $projectRoot 'archive\community\moleworld.net\mole2016'
$reportPath = Join-Path $projectRoot 'data\server\community-map-version-audit.json'
$baseUrl = 'https://www.moleworld.net/mole2016/v'
$result = [System.Collections.Generic.List[object]]::new()

foreach ($variantName in $Variant) {
    foreach ($assetPath in $Asset) {
        $url = '{0}/{1}/{2}' -f $baseUrl, $variantName, $assetPath
        $destination = Join-Path (Join-Path $archiveRoot $variantName) $assetPath
        $destinationDirectory = Split-Path -Parent $destination
        New-Item -ItemType Directory -Force -Path $destinationDirectory | Out-Null

        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 45 `
                -SkipHttpErrorCheck -Headers @{ 'Accept-Encoding' = 'identity' }
            $status = [int] $response.StatusCode
            if ($response.Content -is [byte[]]) {
                $bytes = [byte[]] $response.Content
            }
            elseif ($response.RawContentStream -and $response.RawContentStream.CanSeek) {
                $response.RawContentStream.Position = 0
                $memory = [System.IO.MemoryStream]::new()
                $response.RawContentStream.CopyTo($memory)
                $bytes = $memory.ToArray()
                $memory.Dispose()
            }
            else {
                $bytes = [System.Text.Encoding]::UTF8.GetBytes([string] $response.Content)
            }
            if ($status -eq 200) {
                [System.IO.File]::WriteAllBytes($destination, $bytes)
                $sha256 = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
            }
            else {
                $sha256 = $null
            }

            $result.Add([pscustomobject]@{
                variant = $variantName
                asset = $assetPath
                status = $status
                bytes = if ($status -eq 200) { $bytes.Length } else { 0 }
                sha256 = $sha256
                source = $url
                saved = if ($status -eq 200) { $destination } else { $null }
            })
        }
        catch {
            $result.Add([pscustomobject]@{
                variant = $variantName
                asset = $assetPath
                status = 0
                bytes = 0
                sha256 = $null
                source = $url
                saved = $null
                error = $_.Exception.GetType().Name
            })
        }
    }
}

$result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $reportPath -Encoding utf8
$result | Where-Object status -eq 200 | Format-Table variant, asset, bytes, sha256 -AutoSize
