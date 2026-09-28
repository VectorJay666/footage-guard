# footage-guard Windows entry (thin wrap; same args as run.sh)
param(
  [Parameter(Mandatory = $true, Position = 0)][string]$Video,
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$py = Join-Path $root "scripts\footage_guard.py"
& python $py $Video @Rest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
