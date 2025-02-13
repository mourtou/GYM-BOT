# 🏋️ Gym Automation & Timer Script

This repository contains two Python scripts that automate gym reservations at the University of Cyprus Sports Center. The scripts handle the booking process and run at scheduled times to ensure you never miss a reservation.



## 📌 Project Overview
- GymAutomation.py → Handles the reservation process by interacting with the sports center's website.
- TimerScript.py → Schedules the automation script to run at specific times.

These scripts are designed to book a gym slot automatically and retry if the booking fails.



## 🔧 How It Works
1. TimerScript.py runs every day at scheduled times.
2. It calculates the correct date and time slot for the reservation.
3. It launches GymAutomation.py, which:
   - Opens the university sports center reservation page.
   - Selects the correct date and time.
   - Fills in the reservation form and submits it.
   - Retries if the booking is unsuccessful.

