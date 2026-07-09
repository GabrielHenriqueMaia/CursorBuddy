@echo off
REM Build script: cria/atualiza venv, instala dependências e instala pacote em modo editável
SETLOCAL

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt

echo Installing package in editable mode...
pip install -e .

echo Build complete.
ENDLOCAL
pause
