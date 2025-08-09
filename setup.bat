@echo off
echo Checking for virtual environment...

REM Check if venv folder exists
if exist "venv" (
    echo Virtual environment found. Activating...
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo Virtual environment not found. Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment. Make sure Python is installed.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
)

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install some packages.
        pause
        exit /b 1
    )
    echo All packages installed successfully!
) else (
    echo Warning: requirements.txt file not found.
)

echo.
echo Setup completed successfully!
echo Virtual environment is now active.
echo You can now run your Python scripts.
pause