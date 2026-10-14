# Preview only: opens the official Chinese web game, not a local game server.
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if ($root -ne 'E:\Codex\Projects\Moly-Viet') { throw "Unexpected project location: $root" }

$env:MOLY_DATA_ROOT = Join-Path $root 'data\client'
New-Item -ItemType Directory -Path $env:MOLY_DATA_ROOT -Force | Out-Null
$binary = Join-Path $root 'runtime\client\target\release\moleruffle.exe'
if (-not (Test-Path -LiteralPath $binary)) {
    throw "Client is not built yet: $binary"
}
& $binary
exit $LASTEXITCODE
