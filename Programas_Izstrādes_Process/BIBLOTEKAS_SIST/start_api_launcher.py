"""Launcher that runs the database/api.py script regardless of current working directory.

This helps avoid issues when PowerShell or the environment has trouble with the path encoding.
"""
import runpy
from pathlib import Path

ROOT = Path(__file__).parent
API_PATH = ROOT / 'Programas_Izstrādes_Process' / 'BIBLOTEKAS_SIST' / 'database' / 'api.py'
if not API_PATH.exists():
    raise SystemExit(f"api.py not found at {API_PATH!s}")

print(f"Starting API at {API_PATH}")
runpy.run_path(str(API_PATH), run_name='__main__')
