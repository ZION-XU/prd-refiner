$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

Assert-PrdRefinerUv
$config = Read-PrdRefinerConfluenceConfig
$plainPat = Unprotect-PrdRefinerSecret -ProtectedSecret $config.protectedPat

try {
    $env:CONFLUENCE_URL = $script:PrdRefinerConfluenceUrl
    $env:CONFLUENCE_USERNAME = $config.username
    $env:CONFLUENCE_PERSONAL_TOKEN = $plainPat

    $mcpArguments = $script:PrdRefinerMcpArguments
    & uv @mcpArguments
    exit $LASTEXITCODE
} finally {
    Remove-Item Env:CONFLUENCE_PERSONAL_TOKEN -ErrorAction SilentlyContinue
    $plainPat = $null
}
