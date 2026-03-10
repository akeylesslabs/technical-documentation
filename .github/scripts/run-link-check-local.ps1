param(
    [string]$Target = "./**/*.md"
)

$ErrorActionPreference = "Stop"

# Prefer an existing token; fallback to GitHub CLI if available.
if (-not $env:GITHUB_TOKEN -or [string]::IsNullOrWhiteSpace($env:GITHUB_TOKEN)) {
    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if ($gh) {
        try {
            $token = gh auth token 2>$null
            if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($token)) {
                $env:GITHUB_TOKEN = $token.Trim()
                Write-Host "Using GITHUB_TOKEN from gh auth token."
            }
        }
        catch {
            # Ignore and continue without token.
        }
    }
}

if (-not $env:GITHUB_TOKEN -or [string]::IsNullOrWhiteSpace($env:GITHUB_TOKEN)) {
    Write-Warning "GITHUB_TOKEN is not set. GitHub URLs may return 429 rate-limit errors."
}

$lycheeArgs = @(
    "--verbose"
    "--no-progress"
    "--max-retries", "4"
    "--retry-wait-time", "5"
    "--exclude-file", ".github/lychee/.lycheeignore"
    "--exclude-path", ".github"
    "--exclude-link-local"
    "--exclude-loopback"
    "--include-mail"
    $Target
)

& lychee @lycheeArgs
exit $LASTEXITCODE
