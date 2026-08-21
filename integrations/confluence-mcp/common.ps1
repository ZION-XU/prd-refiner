$script:PrdRefinerConfluenceUrl = 'https://confluence.zwcad.com'
Add-Type -AssemblyName System.Security -ErrorAction Stop
$script:PrdRefinerConfigDirectory = if ([string]::IsNullOrWhiteSpace($env:PRD_REFINER_CONFIG_DIR)) {
    Join-Path ([Environment]::GetFolderPath('ApplicationData')) 'PRDRefiner'
} else {
    $env:PRD_REFINER_CONFIG_DIR
}
$script:PrdRefinerConfigPath = Join-Path $script:PrdRefinerConfigDirectory 'confluence.json'

# This combination is verified against ZWCAD Confluence 7.19.4. Newer
# atlassian-python-api releases currently build an incompatible /rest/api/1.0 path.
$script:PrdRefinerUvDependencyArguments = @(
    'run',
    '--quiet',
    '--with', 'mcp-atlassian==0.8.4',
    '--with', 'atlassian-python-api==3.41.21',
    '--with', 'markdown-to-confluence==0.3.0',
    '--with', 'mcp==1.9.4'
)
$script:PrdRefinerMcpArguments = @(
    $script:PrdRefinerUvDependencyArguments
    'python'
    (Join-Path $PSScriptRoot 'server.py')
)

function Assert-PrdRefinerUv {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        throw 'uv is required. Install uv, reopen the terminal, and rerun the PRD Refiner Confluence setup.'
    }
}

function Protect-PrdRefinerSecret {
    param([System.Security.SecureString]$Secret)

    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secret)
    $bytes = $null
    try {
        $plainText = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
        $bytes = [Text.Encoding]::UTF8.GetBytes($plainText)
        $protectedBytes = [System.Security.Cryptography.ProtectedData]::Protect(
            $bytes,
            $null,
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        return [Convert]::ToBase64String($protectedBytes)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
        if ($null -ne $bytes) {
            [Array]::Clear($bytes, 0, $bytes.Length)
        }
        $plainText = $null
    }
}

function Unprotect-PrdRefinerSecret {
    param([string]$ProtectedSecret)

    $protectedBytes = [Convert]::FromBase64String($ProtectedSecret)
    $bytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
        $protectedBytes,
        $null,
        [System.Security.Cryptography.DataProtectionScope]::CurrentUser
    )
    try {
        return [Text.Encoding]::UTF8.GetString($bytes)
    } finally {
        [Array]::Clear($bytes, 0, $bytes.Length)
    }
}

function Read-PrdRefinerConfluenceConfig {
    if (-not (Test-Path -LiteralPath $script:PrdRefinerConfigPath -PathType Leaf)) {
        throw "Confluence is not configured. Run integrations\confluence-mcp\configure.ps1 first."
    }

    $config = Get-Content -Raw -LiteralPath $script:PrdRefinerConfigPath | ConvertFrom-Json
    if ($config.url -ne $script:PrdRefinerConfluenceUrl) {
        throw "Unexpected Confluence URL in $script:PrdRefinerConfigPath. Rerun configure.ps1."
    }
    if ([string]::IsNullOrWhiteSpace($config.username)) {
        throw "Confluence username is missing from $script:PrdRefinerConfigPath."
    }
    if ([string]::IsNullOrWhiteSpace($config.protectedPat)) {
        throw "Protected Confluence PAT is missing from $script:PrdRefinerConfigPath."
    }
    return $config
}
