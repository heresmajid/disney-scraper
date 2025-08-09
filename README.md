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

### Step 4: Run the Scripts
You have two options to run the scripts:

**Option A: Run Prices Script**
- Double-click on `run_prices.bat` **OR** open Command Prompt and type:
  ```
  run_prices.bat
  ```
- This will automatically activate the virtual environment and run the prices scraper

**Option B: Run Times Script**  
- Double-click on `run_times.bat` **OR** open Command Prompt and type:
  ```
  run_times.bat
  ```
- This will automatically activate the virtual environment and run the times scraper

**Note:** You don't need to manually activate the virtual environment - the .bat files handle this automatically!

### Step 5: Check Output Files
After the script runs successfully, it will generate files in the **output** folder:

**For Prices Script:**
- `output/prices.json` - Contains structured price data
- `output/prices.csv` - Contains price data in spreadsheet format

**For Times Script:**
- `output/times.json` - Contains structured times data  
- `output/times.csv` - Contains times data in spreadsheet format

The output folder will be created automatically if it doesn't exist.

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