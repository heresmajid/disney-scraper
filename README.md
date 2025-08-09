# Disney Scraper - Setup and Execution Instructions

## Prerequisites
- Python must be installed on your system
- Make sure you have the project files in a folder
- **Proxy credentials** (required for API access)

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

### Step 3: Configure Proxy Settings
**IMPORTANT:** Before running the scripts, you must set up proxy credentials.

1. Open `codes/prices.py` file
2. Find this line (around line 120):
   ```python
   proxy = "http://YOUR_USERNAME:YOUR_PASSWORD@YOUR_PROXY_URL:PORT"
   ```
3. Replace with your proxy credentials
   

4. Open `codes/times.py` file  
5. Find this line (around line 60):
   ```python
   proxy = "http://YOUR_USERNAME:YOUR_PASSWORD@YOUR_PROXY_URL:PORT"
   ```
6. Replace with your proxy credentials   

7. Save both files

### Step 4: Update Date Settings (Optional)
1. **For Prices Script:** Open `codes/prices.py`
   - Find line with `'end_date': date(2026, 3, 31)`
   - Update to your desired end date: `'end_date': date(YEAR, MONTH, DAY)`

2. **For Times Script:** Open `codes/times.py`
   - Find line with `end_date = date(2025, 10, 31)`
   - Update to your desired end date: `end_date = date(YEAR, MONTH, DAY)`

3. Save the files

### Step 5: Run the Scripts
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

### Step 6: Check Output Files
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
- **Check proxy settings first** - Most common issue
- Verify proxy credentials are correct and active
- Make sure you updated the date correctly
- Check if virtual environment is active
- Verify all required input files are present

**If no output files are generated:**
- Check the script for any error messages
- **Verify proxy is working** - Test with browser or other tools
- Make sure the date range is valid
- Check if the API endpoints are accessible
- Verify input data is available for the specified dates

**Common Error Messages:**
- `Connection timeout` or `Proxy error` → Check proxy settings
- `401 Unauthorized` → Verify proxy credentials
- `No data collected` → Check date range and API availability

## Need Help?
If you encounter any issues, please contact the development team with:
- Error messages (if any)
- Screenshots of the problem
- Description of what step failed