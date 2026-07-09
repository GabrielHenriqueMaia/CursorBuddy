@echo off
REM Open the hotkey configuration interface in the project environment.
SETLOCAL

IF EXIST venv\Scripts\activate (
    call venv\Scripts\activate
) ELSE (
    echo Virtual environment not found. Creating and installing dependencies...
    python -m venv venv
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .
)

python -m sentinel.hotkey_config
ENDLOCAL
