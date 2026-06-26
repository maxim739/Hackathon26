"""
Build script for Rocket Man — produces a standalone executable via PyInstaller.

Usage:
    python312 build.py          # Windows .exe
    python3   build.py          # macOS app / Linux binary

Output:
    dist/RocketMan.exe          (Windows)
    dist/RocketMan              (macOS / Linux)

Requirements:
    pip install pyinstaller
"""

import subprocess
import sys
import platform

system = platform.system()

args = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--noconsole',
    '--name', 'RocketMan',
    '--add-data', f'assets{chr(59) if system == "Windows" else ":"}assets',
    '--add-data', f'maps{chr(59) if system == "Windows" else ":"}maps',
    'main.py',
]

print(f'Building for {system}...')
print(' '.join(args))
subprocess.run(args, check=True)
print(f'\nDone. Executable is in dist/')
