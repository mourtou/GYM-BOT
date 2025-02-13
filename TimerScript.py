import schedule
import time
import subprocess
from datetime import datetime, timedelta

##########################################################################
# Monday to Friday
# time options: 1    2    3     4     5     6     7     8                 
#               7:45 9:30 11:15 13:00 14:45 16:45 18:30 20:15             
time_option = 6  # Select your preferred time slot

# Saturday
# time options: 9     10     11						
#               8:45  10:30  12:15					
time_option2 = 9  # Select your preferred time slot for Saturday
##########################################################################

# **SET THE CORRECT PATH TO `GymAutomation.py`**
script_path = "C:/Users/codan/Desktop/gymbot/GymAutomation.py"
python_path = "C:/Python312/python.exe"  # Make sure this is correct

# Function to run the main script
def run_main_script():
    today = datetime.now()
    future_date = today + timedelta(days=4)  # Selects 5 days ahead
    next5day = future_date.day  # Correctly stores the date number (1-31)
    next_month = future_date.month  # Store month in case it's needed

    print(f"Running GymAutomation.py with options {time_option}, {time_option2}, {next5day}, {next_month}...")

    # **Ensure correct path format**
    subprocess.run([python_path, script_path, str(time_option), str(time_option2), str(next5day), str(next_month)], shell=True)

# Schedule the script to run every day at these times
schedule.every().day.at("10:36").do(run_main_script)
schedule.every().day.at("08:06").do(run_main_script)
schedule.every().day.at("08:08").do(run_main_script)
schedule.every().day.at("08:12").do(run_main_script)

print("Scheduler started. Waiting for the scheduled time...")

while True:
    schedule.run_pending()
    time.sleep(1)
