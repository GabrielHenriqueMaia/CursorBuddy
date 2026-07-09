@echo off
REM Build the hotkey configuration executable with PyInstaller.
SETLOCAL

IF NOT EXIST venv\Scripts\activate (
    echo Virtual environment not found. Creating and installing dependencies...
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .
) ELSE (
    call venv\Scripts\activate
)

echo Building executable...
pyinstaller --onefile --name CursorBuddyHotkeyConfig --distpath dist --clean src\sentinel\hotkey_config.py

echo Build finished. Executable em dist\CursorBuddyHotkeyConfig.exe
ENDLOCAL
