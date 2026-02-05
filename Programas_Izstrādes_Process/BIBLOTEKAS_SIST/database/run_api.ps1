# Start the API server from this script's folder so imports and files resolve correctly
Set-Location -Path $PSScriptRoot
python api.py
