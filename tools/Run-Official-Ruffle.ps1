param(
    [string] $ClientSwf = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$ruffleExe = Join-Path $projectRoot 'tools\ruffle-0.7.1\ruffle.exe'
$dataRoot = Join-Path $projectRoot 'data\ruffle-official'

if (-not (Test-Path -LiteralPath $ruffleExe -PathType Leaf)) {
    throw "Chưa có Ruffle tại $ruffleExe"
}

if (-not $ClientSwf) {
    $ClientSwf = Join-Path $projectRoot 'archive\clients\2026-10-09\china\Client.swf'
}

if (-not (Test-Path -LiteralPath $ClientSwf -PathType Leaf)) {
    throw "Chưa có SWF tại $ClientSwf"
}

$configDir = Join-Path $dataRoot 'config'
$cacheDir = Join-Path $dataRoot 'cache'
$saveDir = Join-Path $dataRoot 'save'
foreach ($directory in @($configDir, $cacheDir, $saveDir)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

$officialUrl = 'http://mole.61.com/Client.swf'
$ruffleArgs = @(
    $ClientSwf,
    '--spoof-url', $officialUrl,
    '--base', 'http://mole.61.com/',
    '--tcp-connections', 'allow',
    '--config', $configDir,
    '--cache-directory', $cacheDir,
    '--save-directory', $saveDir,
    '--graphics', 'dx12',
    '--width', '1024',
    '--height', '768'
)

$proxyFile = Join-Path $dataRoot 'capture-proxy.txt'
if (Test-Path -LiteralPath $proxyFile -PathType Leaf) {
    $proxyUrl = (Get-Content -Raw -LiteralPath $proxyFile).Trim()
    if ($proxyUrl) {
        $ruffleArgs += @('--proxy', $proxyUrl)
    }
}

Write-Host 'Client tải tài nguyên công khai qua kho lưu cục bộ; Server.xml được đổi sang máy chủ thử 127.0.0.1.'
Write-Host 'Chỉ dùng tài khoản giả, không nhập mật khẩu thật.'
Write-Host "Dữ liệu Ruffle: $dataRoot"
& $ruffleExe @ruffleArgs
