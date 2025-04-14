@echo off
SET VENV_DIR=%~dp0venv
SET REQUIREMENTS_FILE=%~dp0requirements.txt

:: Check if virtual environment exists
IF NOT EXIST "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

:: Activate the virtual environment and install dependencies
CALL "%VENV_DIR%\Scripts\activate.bat"
IF EXIST "%REQUIREMENTS_FILE%" (
    echo Installing dependencies from requirements.txt...
    pip install -r "%REQUIREMENTS_FILE%"
) ELSE (
    echo No requirements.txt found, skipping install.
)

:: Run browser.py
echo Running browser.py...
python "%~dp0browser.py"
