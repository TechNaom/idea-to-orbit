# Idea to Orbit installer for Windows (PowerShell 5.1 or 7), for any Claude Code surface
# (terminal, VS Code, desktop) where `/plugin install` is not available. Copies the skills and
# the /orbit command into your Claude config folder and registers the session-start hook.
#
#   .\install.ps1               install, or update to this copy (safe to run again)
#   .\install.ps1 --uninstall   remove exactly what it added; your own settings stay
#
# Config folder: $env:CLAUDE_CONFIG_DIR if set, else ~\.claude. Nothing is changed unless every
# check passes first.

# No param block: Windows PowerShell 5.1 does not bind "--uninstall" to a named parameter, it lands in $args.
$Mode = if (($args -contains "--uninstall") -or ($args -contains "-Uninstall")) { "--uninstall" } else { "install" }
$ErrorActionPreference = "Stop"

$src = $PSScriptRoot
$cfg = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME ".claude" }
$home2 = Join-Path $cfg "idea-to-orbit"
$skillsDir = Join-Path $cfg "skills"
$settingsPath = Join-Path $cfg "settings.json"
$marker = ".idea-to-orbit"                          # a file in every skill folder this installer put there
$MARK = "Idea to Orbit: reading the product state"  # the statusMessage that identifies our hook

function Stop-Install([string]$Message) { [Console]::Error.WriteLine("Stopped: $Message"); exit 1 }

# Read settings.json and check its shape; stop before any change if it is not what Claude Code expects.
function Read-Settings {
    if (-not (Test-Path $settingsPath)) { return $null }
    $text = [System.IO.File]::ReadAllText($settingsPath)   # strips a UTF-8 byte order mark
    if (-not $text.Trim()) { return (New-Object PSObject) }
    try { $s = ConvertFrom-Json -InputObject $text } catch { Stop-Install "$settingsPath is not valid JSON. Fix it first; nothing was changed." }
    $shape = "$settingsPath does not have the shape Claude Code expects (an object, with 'hooks' an object and 'hooks.SessionStart' a list). Fix it first; nothing was changed."
    if (-not ($s -is [System.Management.Automation.PSCustomObject])) { Stop-Install $shape }
    $h = $s.PSObject.Properties["hooks"]
    if ($h) {
        if (-not ($h.Value -is [System.Management.Automation.PSCustomObject])) { Stop-Install $shape }
        $ss = $h.Value.PSObject.Properties["SessionStart"]
        if ($ss -and -not ($ss.Value -is [System.Array])) { Stop-Install $shape }
    }
    return $s
}

# Add or remove our SessionStart hook; every other setting is kept as it is.
# add: $Arg is the hook command, and the keys it had to create are returned.
# remove: $Arg lists the keys the installer created; only those are removed again, and only if empty.
function Update-Settings([string]$Action, [string]$Arg) {
    $s = Read-Settings
    if ($null -eq $s) {
        if ($Action -eq "remove") { return "" }
        $s = New-Object PSObject
    }
    $before = ConvertTo-Json -InputObject $s -Depth 32 -Compress
    $created = @()
    if (-not $s.PSObject.Properties["hooks"]) { $s | Add-Member hooks (New-Object PSObject); $created += "hooks" }
    $hadStart = [bool]$s.hooks.PSObject.Properties["SessionStart"]
    if (-not $hadStart) { $created += "SessionStart" }
    $groups = @()
    if ($hadStart) {
        foreach ($g in @($s.hooks.SessionStart)) {
            if ($g.PSObject.Properties["hooks"] -and $g.hooks -is [System.Array]) {
                $all = @($g.hooks)
                $kept = @($all | Where-Object { -not ($_.PSObject.Properties["statusMessage"] -and $_.statusMessage -eq $MARK) })
                if ($kept.Count -eq 0 -and $all.Count -gt 0) { continue }   # the group held nothing but ours
                $g.hooks = $kept
            }
            $groups += $g
        }
        $s.hooks.PSObject.Properties.Remove("SessionStart")
    }
    if ($Action -eq "add") {
        $groups += [PSCustomObject]@{
            matcher = "startup|resume|clear|compact"
            hooks   = @([PSCustomObject]@{ type = "command"; command = $Arg; timeout = 10; statusMessage = $MARK })
        }
    }
    $mine = if ($Action -eq "remove") { @($Arg -split "\s+" | Where-Object { $_ }) } else { @() }
    if ($groups.Count -gt 0 -or -not ($Action -eq "remove" -and $mine -contains "SessionStart")) {
        $s.hooks | Add-Member SessionStart ([object[]]$groups)
    }
    if (@($s.hooks.PSObject.Properties).Count -eq 0 -and $Action -eq "remove" -and $mine -contains "hooks") {
        $s.PSObject.Properties.Remove("hooks")
    }
    $result = ($created -join " ")
    if ((ConvertTo-Json -InputObject $s -Depth 32 -Compress) -eq $before) { return $result }
    New-Item -ItemType Directory -Force $cfg | Out-Null
    $json = ConvertTo-Json -InputObject $s -Depth 32
    [System.IO.File]::WriteAllText($settingsPath, $json + "`n", (New-Object System.Text.UTF8Encoding($false)))
    return $result
}

$skills = @(Get-ChildItem (Join-Path $src "skills") -Directory | ForEach-Object { $_.Name })

# Every check before any change.
$null = Read-Settings
$cmdPath = Join-Path (Join-Path $cfg "commands") "orbit.md"
$ourCmd = Join-Path $home2 "orbit.md"
function Test-SameFile($a, $b) {
    (Test-Path $a) -and (Test-Path $b) -and ((Get-FileHash $a).Hash -eq (Get-FileHash $b).Hash)
}
if ($Mode -ne "--uninstall") {
    if ((Test-Path $cmdPath) -and -not (Test-SameFile $cmdPath $ourCmd) -and -not (Test-SameFile $cmdPath (Join-Path (Join-Path $src "commands") "orbit.md"))) {
        Stop-Install "$cmdPath is not from this installer (it may be yours). Rename or remove it first; nothing was changed."
    }
    foreach ($name in $skills) {
        $dir = Join-Path $skillsDir $name
        if ((Test-Path $dir) -and -not (Test-Path (Join-Path $dir $marker))) {
            Stop-Install "$dir is not from this installer (it may be yours). Rename or remove it first; nothing was changed."
        }
    }
}

# Skill folders of ours, from this version or an older one: they carry the marker file.
function Get-OurSkills {
    if (-not (Test-Path $skillsDir)) { return @() }
    @(Get-ChildItem $skillsDir -Directory | Where-Object { Test-Path (Join-Path $_.FullName $marker) })
}

if ($Mode -eq "--uninstall") {
    $keysFile = Join-Path $home2 "created-keys"
    $keys = if (Test-Path $keysFile) { [System.IO.File]::ReadAllText($keysFile) } else { "" }
    $null = Update-Settings "remove" $keys
    foreach ($d in Get-OurSkills) { Remove-Item -Recurse -Force $d.FullName }
    if (Test-SameFile $cmdPath $ourCmd) { Remove-Item -Force $cmdPath }
    if (Test-Path $home2) { Remove-Item -Recurse -Force $home2 }
    Write-Output "Idea to Orbit removed from $cfg."
    exit 0
}

foreach ($d in @($skillsDir, (Join-Path $cfg "commands"), $home2)) { New-Item -ItemType Directory -Force $d | Out-Null }
foreach ($d in Get-OurSkills) { Remove-Item -Recurse -Force $d.FullName }   # ours, from any version
foreach ($name in $skills) {
    $dest = Join-Path $skillsDir $name
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse (Join-Path (Join-Path $src "skills") $name) $dest
    [System.IO.File]::WriteAllText((Join-Path $dest $marker), "Installed by Idea to Orbit. Remove with install.ps1 --uninstall.`n")
}
Copy-Item -Force (Join-Path (Join-Path $src "commands") "orbit.md") $cmdPath
Copy-Item -Force (Join-Path (Join-Path $src "commands") "orbit.md") $ourCmd
$hooks = Join-Path $home2 "hooks"
if (Test-Path $hooks) { Remove-Item -Recurse -Force $hooks }
Copy-Item -Recurse (Join-Path $src "hooks") $hooks
$runCmd = (Join-Path $hooks "run.cmd") -replace "\\", "/"
$created = Update-Settings "add" "`"$runCmd`" session-start"
$keysFile = Join-Path $home2 "created-keys"
if (-not (Test-Path $keysFile)) { [System.IO.File]::WriteAllText($keysFile, "$created`n") }   # the first install knows what it created

Write-Output "Idea to Orbit installed in ${cfg}: $($skills.Count) skills, /orbit and the session-start hook."
Write-Output "Start a new Claude Code session and type /orbit."
