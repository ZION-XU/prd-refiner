[CmdletBinding()]
param(
    [string]$Username,
    [string]$PatFile,
    [switch]$SkipDependencyWarmup
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

if ([string]::IsNullOrWhiteSpace($Username)) {
    $Username = Read-Host 'Enter your company Confluence username'
}
if ([string]::IsNullOrWhiteSpace($Username)) {
    throw 'Confluence username cannot be empty.'
}

if ([string]::IsNullOrWhiteSpace($PatFile)) {
    $securePat = Read-Host 'Enter your company Confluence PAT (input is hidden)' -AsSecureString
} else {
    if (-not (Test-Path -LiteralPath $PatFile -PathType Leaf)) {
        throw "PAT file not found: $PatFile"
    }
    $plainPat = (Get-Content -Raw -LiteralPath $PatFile).Trim()
    if ([string]::IsNullOrWhiteSpace($plainPat)) {
        throw 'PAT file is empty.'
    }
    $securePat = ConvertTo-SecureString -String $plainPat -AsPlainText -Force
    $plainPat = $null
}

if ($securePat.Length -eq 0) {
    throw 'Confluence PAT cannot be empty.'
}

New-Item -ItemType Directory -Force -Path $script:PrdRefinerConfigDirectory | Out-Null
$payload = [ordered]@{
    schemaVersion = 1
    url = $script:PrdRefinerConfluenceUrl
    username = $Username.Trim()
    protectedPat = Protect-PrdRefinerSecret -Secret $securePat
    updatedAt = (Get-Date).ToUniversalTime().ToString('o')
}
$payload | ConvertTo-Json | Set-Content -LiteralPath $script:PrdRefinerConfigPath -Encoding UTF8

Write-Host "Confluence configuration saved for the current Windows user: $script:PrdRefinerConfigPath"
Write-Host "Confluence URL: $script:PrdRefinerConfluenceUrl"
Write-Host "Username: $($Username.Trim())"

if (-not $SkipDependencyWarmup) {
    Assert-PrdRefinerUv
    Write-Host 'Preparing the pinned Confluence MCP runtime...'
    $dependencyArguments = $script:PrdRefinerUvDependencyArguments
    & uv @dependencyArguments python -c "import mcp_atlassian; print('mcp-atlassian', mcp_atlassian.__version__)"
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to prepare the Confluence MCP runtime (exit code $LASTEXITCODE)."
    }
}

Write-Host 'Setup completed. Start a new Agent task so the MCP server can be loaded.'
