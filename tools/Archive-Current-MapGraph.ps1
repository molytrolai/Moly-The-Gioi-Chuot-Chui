param(
    [int[]] $MapId = @(),
    [int] $ThrottleLimit = 4,
    [switch] $PopulateMirror
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$projectRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = 'https://www.moleworld.net/mole2016/'
$communityRoot = Join-Path $projectRoot 'archive\community\moleworld.net\mole2016\current'
$mirrorRoot = Join-Path $projectRoot 'archive\clients\offline-mirror\mole.61.com'
$reportPath = Join-Path $projectRoot 'data\server\current-map-graph-archive.json'
New-Item -ItemType Directory -Force -Path $communityRoot | Out-Null

$graphUrl = $sourceRoot + 'mo-mapgraph.json'
$graphResponse = Invoke-WebRequest -UseBasicParsing -Uri $graphUrl -TimeoutSec 45
$graphText = [string] $graphResponse.Content
$graphPath = Join-Path $communityRoot 'mo-mapgraph.json'
[System.IO.File]::WriteAllText($graphPath, $graphText, [System.Text.UTF8Encoding]::new($false))
$graph = $graphText | ConvertFrom-Json

$selectedMaps = if ($MapId.Count -gt 0) {
    $wanted = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($id in $MapId) { [void] $wanted.Add([string] $id) }
    @($graph.maps.PSObject.Properties | Where-Object { $wanted.Contains($_.Name) })
}
else {
    @($graph.maps.PSObject.Properties)
}

$assets = @(
    $selectedMaps |
        ForEach-Object { @($_.Value) } |
        Where-Object { $_ -is [string] -and $_ -notmatch '^\s*$' } |
        Sort-Object -Unique
)

$populate = [bool] $PopulateMirror
$results = $assets | ForEach-Object -Parallel {
    $ErrorActionPreference = 'Stop'
    $ProgressPreference = 'SilentlyContinue'
    $asset = [string] $_
    $sourceRoot = $using:sourceRoot
    $communityRoot = $using:communityRoot
    $mirrorRoot = $using:mirrorRoot
    $populate = $using:populate

    try {
        $assetUri = [System.Uri]::new([System.Uri] $sourceRoot, $asset)
        if ($assetUri.Scheme -ne 'https' -or $assetUri.Host -ne 'www.moleworld.net') {
            throw "Unexpected asset origin: $assetUri"
        }
        $prefix = '/mole2016/'
        if (-not $assetUri.AbsolutePath.StartsWith($prefix, [System.StringComparison]::Ordinal)) {
            throw "Unexpected asset path: $($assetUri.AbsolutePath)"
        }
        $relative = [System.Uri]::UnescapeDataString($assetUri.AbsolutePath.Substring($prefix.Length))
        if ([string]::IsNullOrWhiteSpace($relative) -or $relative.Split('/') -contains '..') {
            throw "Unsafe asset path: $relative"
        }

        $destination = [System.IO.Path]::GetFullPath((Join-Path $communityRoot $relative))
        $resolvedCommunity = [System.IO.Path]::GetFullPath($communityRoot).TrimEnd('\') + '\'
        if (-not $destination.StartsWith($resolvedCommunity, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Asset escaped archive root: $destination"
        }
        $directory = Split-Path -Parent $destination
        New-Item -ItemType Directory -Force -Path $directory | Out-Null

        $downloaded = $false
        if (-not (Test-Path -LiteralPath $destination -PathType Leaf) -or (Get-Item -LiteralPath $destination).Length -eq 0) {
            $temporary = Join-Path $directory ('.moly-' + [guid]::NewGuid().ToString('N') + '.tmp')
            try {
                $response = Invoke-WebRequest -UseBasicParsing -Uri $assetUri.AbsoluteUri `
                    -TimeoutSec 90 -SkipHttpErrorCheck -OutFile $temporary -PassThru `
                    -Headers @{ 'Accept-Encoding' = 'identity' }
                if ([int] $response.StatusCode -ne 200) {
                    throw "HTTP $([int] $response.StatusCode)"
                }
                [System.IO.File]::Move($temporary, $destination, $true)
                $downloaded = $true
            }
            finally {
                if (Test-Path -LiteralPath $temporary) {
                    Remove-Item -LiteralPath $temporary -Force
                }
            }
        }

        $hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        $length = (Get-Item -LiteralPath $destination).Length
        $mirrorState = 'disabled'
        $mirrorDestination = $null
        if ($populate) {
            $mirrorDestination = [System.IO.Path]::GetFullPath((Join-Path $mirrorRoot $relative))
            $resolvedMirror = [System.IO.Path]::GetFullPath($mirrorRoot).TrimEnd('\') + '\'
            if (-not $mirrorDestination.StartsWith($resolvedMirror, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Asset escaped mirror root: $mirrorDestination"
            }
            if (Test-Path -LiteralPath $mirrorDestination -PathType Leaf) {
                $mirrorState = 'kept-existing'
            }
            else {
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $mirrorDestination) | Out-Null
                Copy-Item -LiteralPath $destination -Destination $mirrorDestination
                $mirrorState = 'added'
            }
        }

        [pscustomobject]@{
            asset = $asset
            status = 'ready'
            downloaded = $downloaded
            bytes = $length
            sha256 = $hash
            source = $assetUri.AbsoluteUri
            saved = $destination
            mirror = $mirrorState
            mirror_path = $mirrorDestination
        }
    }
    catch {
        [pscustomobject]@{
            asset = $asset
            status = 'failed'
            downloaded = $false
            bytes = 0
            sha256 = $null
            source = $null
            saved = $null
            mirror = 'not-added'
            mirror_path = $null
            error = $_.Exception.Message
        }
    }
} -ThrottleLimit $ThrottleLimit

$summary = [pscustomobject]@{
    generated_at = [DateTimeOffset]::UtcNow.ToString('O')
    graph_source = $graphUrl
    graph_sha256 = (Get-FileHash -LiteralPath $graphPath -Algorithm SHA256).Hash.ToLowerInvariant()
    selected_map_count = $selectedMaps.Count
    asset_count = $assets.Count
    ready_count = @($results | Where-Object status -eq 'ready').Count
    failed_count = @($results | Where-Object status -eq 'failed').Count
    total_bytes = ($results | Where-Object status -eq 'ready' | Measure-Object -Property bytes -Sum).Sum
    assets = @($results)
}
$summary | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reportPath -Encoding utf8
$summary | Select-Object selected_map_count, asset_count, ready_count, failed_count, total_bytes | Format-List
if ($summary.failed_count -gt 0) {
    $results | Where-Object status -eq 'failed' | Format-Table asset, error -AutoSize
    exit 1
}
