# Project Setup and Execution Instructions

## Prerequisites
- Python must be installed on your system
- Make sure you have the project files in a folder

## Step-by-Step Instructions

### Step 1: Verify Requirements File
Before running anything, make sure you have a `requirements.txt` file in your project folder. This file contains all the necessary packages for the project to work properly.

**Check if requirements.txt exists:**
- Look for `requirements.txt` file in your project folder
- If it's missing, contact the developer to provide this file

### Step 2: Run Setup File
1. Double-click on `setup.bat` file **OR** open Command Prompt and type:
   ```
   setup.bat
   ```
2. The setup file will automatically:
   - Check if virtual environment exists
   - Create a new virtual environment if needed
   - Activate the virtual environment
   - Install all required packages from requirements.txt

**Wait for setup to complete** - you'll see a "Setup completed successfully!" message.

### Step 3: Update Date in Script
1. Open your main Python script file
2. Look for date-related variables or settings
3. Update the date to your desired date range or current date
4. Save the file

### Step 4: Run the Main Script
1. Make sure your virtual environment is still active (you should see `(venv)` in your command prompt)
2. Run your Python script:
   ```
   python your_script_name.py
   ```
   *(Replace `your_script_name.py` with the actual name of your script)*

### Step 5: Check Output Files
After the script runs successfully, it will generate:
- **JSON file** - Contains structured data
- **CSV file** - Contains data in spreadsheet format

Both files will be created in your project folder.

## Troubleshooting

**If setup fails:**
- Make sure Python is installed and added to PATH
- Check if requirements.txt file exists
- Run Command Prompt as Administrator

**If script fails:**
- Make sure you updated the date correctly
- Check if virtual environment is active
- Verify all required input files are present

**If no output files are generated:**
- Check the script for any error messages
- Make sure the date range is valid
- Verify input data is available for the specified dates

## Need Help?
If you encounter any issues, please contact the development team with:
- Error messages (if any)
- Screenshots of the problem
- Description of what step failed