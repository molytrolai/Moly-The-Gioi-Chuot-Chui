# Builds the research client on E. It still connects to the official Chinese
# server; this is not a build of the local game server.
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if ($root -ne 'E:\Codex\Projects\Moly-Viet') { throw "Unexpected project location: $root" }

$env:CARGO_HOME = Join-Path $root 'tools\cargo-home'
$env:RUSTUP_HOME = Join-Path $root 'tools\rustup-home'
$env:CARGO_TARGET_DIR = Join-Path $root 'runtime\client\target'
$env:MOLY_DATA_ROOT = Join-Path $root 'data\client'
foreach ($path in @($env:CARGO_HOME, $env:RUSTUP_HOME, $env:CARGO_TARGET_DIR, $env:MOLY_DATA_ROOT)) {
    New-Item -ItemType Directory -Path $path -Force | Out-Null
}

$cargo = Get-Command cargo -ErrorAction SilentlyContinue
if (-not $cargo) {
    throw 'Rust/Cargo is not installed. Install a trusted Rust toolchain onto E before building.'
}
& $cargo.Source build --locked --release -p moleruffle-desktop --manifest-path (Join-Path $root 'runtime\client\Cargo.toml')
if ($LASTEXITCODE -ne 0) { throw "Cargo build failed with exit code $LASTEXITCODE" }
Write-Output (Join-Path $env:CARGO_TARGET_DIR 'release\moleruffle.exe')
