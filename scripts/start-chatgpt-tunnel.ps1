[CmdletBinding()]
param(
    [int]$Port = 8791,
    [int]$HealthPort = 8091
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $root 'runtime'
New-Item -ItemType Directory -Force -Path $runtime | Out-Null

if ([string]::IsNullOrWhiteSpace($env:CONTROL_PLANE_API_KEY)) {
    throw 'CONTROL_PLANE_API_KEY is not set in this shell.'
}
if ([string]::IsNullOrWhiteSpace($env:CONTROL_PLANE_TUNNEL_ID)) {
    throw 'CONTROL_PLANE_TUNNEL_ID is not set in this shell.'
}

$bun = (Get-Command bun -ErrorAction Stop).Source
$tunnelClient = (Get-Command tunnel-client -ErrorAction Stop).Source

$mcpStdout = Join-Path $runtime 'mcp.stdout.log'
$mcpStderr = Join-Path $runtime 'mcp.stderr.log'
$mcp = Start-Process `
    -FilePath $bun `
    -ArgumentList @('run', 'server/index.ts', '--port', "$Port") `
    -WorkingDirectory $root `
    -RedirectStandardOutput $mcpStdout `
    -RedirectStandardError $mcpStderr `
    -WindowStyle Hidden `
    -PassThru

try {
    Start-Sleep -Milliseconds 750
    Invoke-RestMethod "http://127.0.0.1:$Port/readyz" | Out-Host

    & $tunnelClient run `
        --control-plane.tunnel-id $env:CONTROL_PLANE_TUNNEL_ID `
        --control-plane.api-key env:CONTROL_PLANE_API_KEY `
        --mcp.server-url "http://127.0.0.1:$Port/mcp" `
        --health.listen-addr "127.0.0.1:$HealthPort"
}
finally {
    if ($mcp -and -not $mcp.HasExited) {
        Stop-Process -Id $mcp.Id -Force -ErrorAction SilentlyContinue
    }
}
