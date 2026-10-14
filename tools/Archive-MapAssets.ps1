param(
    [int[]] $MapId = @(2, 5, 15, 17, 19, 20, 21, 28, 38, 63, 64, 75, 76, 120, 142, 143),
    [string] $ProxyUrl = 'http://127.0.0.1:18080'
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$projectRoot = Split-Path -Parent $PSScriptRoot
$result = [System.Collections.Generic.List[object]]::new()

function Save-PublicAsset {
    param([int] $Id, [string] $Kind, [string] $Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -Proxy $ProxyUrl -UseBasicParsing `
            -SkipHttpErrorCheck -TimeoutSec 45 -Headers @{ 'Accept-Encoding' = 'identity' }
        $result.Add([pscustomobject]@{
            map = $Id
            kind = $Kind
            status = [int] $response.StatusCode
            bytes = $response.RawContentLength
            url = $Url
        })
        return [int] $response.StatusCode
    }
    catch {
        $result.Add([pscustomobject]@{
            map = $Id
            kind = $Kind
            status = 0
            bytes = 0
            url = $Url
            error = $_.Exception.GetType().Name
        })
        return 0
    }
}

foreach ($id in $MapId) {
    $assetId = 10000 + $id
    $xmlUrl = 'http://mole.61.com/resource/map/Map_{0}.xml?moly-archive=current' -f $assetId
    $xmlStatus = Save-PublicAsset -Id $id -Kind 'xml-map' -Url $xmlUrl
    if ($xmlStatus -ne 200) {
        $shortXmlUrl = 'http://mole.61.com/resource/map/{0}.xml?moly-archive=current' -f $id
        [void](Save-PublicAsset -Id $id -Kind 'xml-short' -Url $shortXmlUrl)
    }

    $swfUrl = 'http://mole.61.com/resource/map/Map_{0}.swf?moly-archive=current' -f $assetId
    $swfStatus = Save-PublicAsset -Id $id -Kind 'swf-map' -Url $swfUrl
    if ($swfStatus -ne 200) {
        $shortSwfUrl = 'http://mole.61.com/resource/map/{0}.swf?moly-archive=current' -f $id
        [void](Save-PublicAsset -Id $id -Kind 'swf-short' -Url $shortSwfUrl)
    }
}

$reportPath = Join-Path $projectRoot 'data\server\map-asset-audit.json'
$result | ConvertTo-Json | Set-Content -LiteralPath $reportPath -Encoding utf8
$result | Format-Table -AutoSize
