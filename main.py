# What is the first thing we have to do
import csv
import os
import time
from datetime import datetime

from colorama import Fore, Style
from playsound import playsound

from dcpy import clear

# USER CHANGEABLE VARIABLES
POMO = 0.1 or 50
SHORT_BREAK = 0.1 or 10
LONG_BREAK = 0.1 or 30
SESSIONS_UNTIL_LONG_BREAK = 2
ALARM_PATH = "./assets/alarm_sound.mp3"
BREAK_SOUND_PATH = "./assets/break_sound.mp3"


def timer(minutes, message):
    # counts down a time
    # seconds is the amount of seconds to count down, this is
    # an integer
    seconds = minutes * 60  # certain amount of seconds

    while seconds >= 0:
        clear()
        count_min = seconds // 60
        count_sec = seconds % 60

        if count_sec < 10:
            count_sec = f"0{count_sec}"

        if count_min < 10:
            count_min = f"0{count_min}"

        print(message)
        print(Fore.RED + "➜  " + Style.RESET_ALL + f"{count_min}:{count_sec}  🍅")
        time.sleep(1)
        seconds -= 1


def main():

    # APP VARIABLES
    session_number = 0

    while True:
        try:
            # ============== POMO SESSION ======================= #

            desired_sessions = SESSIONS_UNTIL_LONG_BREAK
            if not session_number % SESSIONS_UNTIL_LONG_BREAK and session_number:
                desired_sessions = SESSIONS_UNTIL_LONG_BREAK + session_number

            session_number += 1

            timer(
                POMO,
                f"You are currently on session {session_number}/{desired_sessions}",
            )

            # after pomo timer finishes, then play annoying sound
            print("\nPomo session finished!")
            playsound(ALARM_PATH, False)

            print("Give me a brief sentence on what you completed.")
            pomo_description = input("What did you accomplish during this session?\n\n")

            # If file doesn't exist, write the headers
            if not os.path.exists("./pomo_data.csv"):
                with open("pomo_data.csv", "w") as file:
                    file.write("date,session_number,session_length,description\n")

            # if the file exists, append data
            with open("pomo_data.csv", "a") as csv_file:
                fieldnames = ["date", "session_number", "session_length", "description"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow(
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "session_number": session_number,
                        "session_length": POMO,
                        "description": pomo_description,
                    }
                )

            # =============== BREAK ======================== #
            if not session_number % SESSIONS_UNTIL_LONG_BREAK:
                timer(LONG_BREAK, "Long break")
                print("Break is finished, its go time")
                playsound(BREAK_SOUND_PATH, False)
                input("press enter to continue")
            else:
                timer(SHORT_BREAK, "Short break")
                print("Chess break is over, time to work")
                playsound(BREAK_SOUND_PATH, False)
                input("press enter to continue")

        except KeyboardInterrupt:
            print("\nExited")
            return


main()
