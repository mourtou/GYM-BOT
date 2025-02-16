import sys
import time
import calendar
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ✅ **Ensure script receives arguments properly, otherwise use default values**
if len(sys.argv) < 5:
    print("Warning: No arguments provided. Using default values.")
    time_option = 7  # Default weekday time slot
    time_option2 = 9  # Default Saturday time slot
    future_date = datetime.now() + timedelta(days=5)  # Default to 5 days ahead
    next5day = future_date.day  # Correct day
    next_month = future_date.month  # Correct month
else:
    time_option = int(sys.argv[1])  # Time slot (1-8 for weekdays, 9-11 for Saturday)
    time_option2 = int(sys.argv[2])  # Saturday time slot
    next5day = int(sys.argv[3])  # The correct day to select
    next_month = int(sys.argv[4])  # The correct month

# ✅ **Paths for ChromeDriver & Chrome Profile**
driver_path ="C:\\Users\\Administrator\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe"
chrome_profile_path ="C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome for Testing\\User Data\\Default"

while True:  # **Loop to retry if reservation fails**
    try:
        # ✅ **Initialize WebDriver**
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={chrome_profile_path}")  
        chrome_options.add_argument("--profile-directory=Default")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print(f"[{datetime.now()}] Opening website...")
        driver.get("https://applications2.ucy.ac.cy/sportscenter/main_online_new?p_lang=")

        # ✅ **Step 1: Navigate to Reservations**
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Κρατήσεις"))).click()
        print(f"[{datetime.now()}] Navigated to reservations page.")

        # ✅ **Step 2: Select 'Γυμναστήριο'**
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "p_sport"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//option[@value='6']"))).click()
        print(f"[{datetime.now()}] Selected 'Γυμναστήριο'.")

        # ✅ **Step 3: Accept Terms and Click 'Επόμενο'**
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "terms_accepted"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')]"))).click()
        print(f"[{datetime.now()}] Clicked 'Επόμενο' button.")

        # ✅ **Step 4: Select the correct date (5 days ahead)**
        today = datetime.now()
        future_date = today + timedelta(days=5)
        future_weekday = future_date.weekday()  # 0=Monday, 5=Saturday, 6=Sunday

        # **Check if it's a Saturday**
        if future_weekday == 5:
            selected_time_option = time_option2  # Use Saturday time
            print(f"Selecting time for **Saturday** (Option {selected_time_option})")
        else:
            selected_time_option = time_option  # Use weekday time
            print(f"Selecting time for **Weekday** (Option {selected_time_option})")

        # **Check if we need to switch to next month**
        year = future_date.year
        month = future_date.month
        days_in_month = calendar.monthrange(year, month)[1]

        if next5day > days_in_month:
            next5day = next5day % days_in_month
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Επόμενος Μήνας')]"))).click()

        # **Click on the correct day button**
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{next5day}']"))).click()

        # ✅ **Step 5: Select Time Slot**
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "p_sttime")))
        time_dropdown = driver.find_element(By.NAME, "p_sttime")
        select = Select(time_dropdown)

        # **Map the `time_option` correctly for weekdays & Saturdays**
        weekday_mapping = {
            1: "07:45", 2: "09:30", 3: "11:15", 4: "13:00",
            5: "14:45", 6: "16:45", 7: "18:30", 8: "20:15"
        }
        saturday_mapping = {
            9: "08:45", 10: "10:30", 11: "12:15"
        }

        # **Choose correct time mapping**
        if future_weekday == 5:  # Saturday
            selected_time = saturday_mapping.get(selected_time_option, "08:45")
        else:  # Monday-Friday
            selected_time = weekday_mapping.get(selected_time_option, "18:30")

        select.select_by_visible_text(selected_time)
        print(f"[{datetime.now()}] Selected time slot: {selected_time}")

        # ✅ **Step 6: Enter Purpose & Submit**
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "textarea"))).send_keys("testomaxing")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Καταχώρηση']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Καταχώρηση']"))).click()

        print(f"[{datetime.now()}] Reservation submitted successfully.")

    except Exception as e:
        print(f"Error encountered: {e}")

    finally:
        # ✅ **Close WebDriver and retry after delay**
        driver.quit()
        print(f"[{datetime.now()}] Sleeping for 10 seconds before retrying...")
        time.sleep(10)  # Retry every 10 seconds in case of failure
