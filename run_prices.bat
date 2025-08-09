@echo off
echo Starting Prices Script...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first to create the virtual environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Virtual environment activated.
echo Running prices script...
echo.

REM Run the prices Python script
python codes/prices.py

if errorlevel 1 (
    echo.
    echo Error: Prices script failed to run properly.
    echo Please check the error messages above.
) else (
    echo.
    echo Prices script completed successfully!
    echo Check the 'output' folder for generated JSON and CSV files.
)

echo.
pause