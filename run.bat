@echo off
REM Run script: ativa venv e executa uma ação do projeto
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

REM Usage:
REM   run.bat format        -> abre o painel de formatação (clipboard/stdin)
REM   run.bat [args...]    -> executa o CLI `sentinel.cli` com os argumentos informados

IF "%1"=="format" (
    python -m sentinel.format_panel
) ELSE (
    python -m sentinel.cli %*
)

ENDLOCAL
