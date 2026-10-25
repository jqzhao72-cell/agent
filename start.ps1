$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot

& "$projectRoot\.venv\Scripts\python.exe" -m uvicorn api.server:app --host 127.0.0.1 --port 8002
