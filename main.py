"""
Pomodoro CLI

The purpose of this program is a simple CLI solution to the Pomodoro technique. It's fast, works, and records data properly. 

I wanted to make a customizable and simple time tracker variant using the Pomodoro technique.
"""
import csv
import os
import time
from datetime import datetime

from colorama import Fore, Style
from playsound import playsound

from dcpy import clear, hide_cursor, show_cursor

# USER CHANGEABLE VARIABLES
POMO = None or 50
SHORT_BREAK = None or 10
LONG_BREAK = None or 30
SESSIONS_UNTIL_LONG_BREAK = 2
ALARM_PATH = "./assets/alarm_sound.mp3"
BREAK_SOUND_PATH = "./assets/break_sound.mp3"
POMO_DATA_PATH = "./pomo_data.csv"


def main():

    # APP VARIABLES
    session_number = 0
    desired_sessions = SESSIONS_UNTIL_LONG_BREAK
    date = datetime.now().strftime("%Y-%m-%d")
    total_minutes_studied_today = 0

    while True:
        try:

            # ============= Getting Stats ======================== #

            # If file doesn't exist, write the headers
            if not os.path.exists(POMO_DATA_PATH):
                with open("pomo_data.csv", "w") as file:
                    file.write("date,session_number,session_length,description\n")

            # Read data and get total minutes studied today
            with open(POMO_DATA_PATH, "r") as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    if row.get("date") == date:
                        print(row)
                        total_minutes_studied_today += float(
                            row.get("session_length", 0)
                        )

            # Get Hours and Minutes Studied today
            hours_studied_today = total_minutes_studied_today // 60
            minutes_studied_today = total_minutes_studied_today % 60

            # ============== POMO SESSION ======================= #

            # Update desired sessions after completing a full cycle
            # A cycle is sessions until a long break
            # eg: 3 sessions until long break --> after 3 sessions 3/3 we update
            #   the desired session to 4/6 for the next cycle
            if not session_number % SESSIONS_UNTIL_LONG_BREAK and session_number:
                desired_sessions = SESSIONS_UNTIL_LONG_BREAK + session_number

            session_number += 1

            timer(
                POMO,
                f"You are currently on session {session_number}/{desired_sessions}",
            )

            # After pomo timer finishes, then play annoying sound
            print(
                Fore.GREEN
                + f"\nDone! Total Time Studied Today: {hours_studied_today}hr(s), {minutes_studied_today}min(s)\n"
                + Style.RESET_ALL
            )
            show_cursor()
            playsound(ALARM_PATH, False)

            # Encourage user to update me on their progress
            pomo_description = input(
                "Give me a brief sentence on what you accomplished this session:\n\n"
            )

            # if the file exists, append data
            with open(POMO_DATA_PATH, "a") as csv_file:
                fieldnames = ["date", "session_number", "session_length", "description"]
                writer = csv.DictWriter(
                    csv_file, fieldnames=fieldnames, lineterminator=os.linesep
                )
                writer.writerow(
                    {
                        "date": date,
                        "session_number": session_number,
                        "session_length": POMO,
                        "description": pomo_description,
                    }
                )

            # =============== BREAK ======================== #
            if not session_number % SESSIONS_UNTIL_LONG_BREAK:
                timer(LONG_BREAK, "Long break. Go on a walk or rest up.", True)
                print("Break is finished, its go time.")
                play_short_break_sound()
            else:
                timer(
                    SHORT_BREAK,
                    "Short break. Maybe you can go play a game of chess.",
                    True,
                )
                print("Chess break is over, time to work.")
                play_short_break_sound()

        except KeyboardInterrupt:
            # ctrl + z on linux to exit the program
            print("\nExited")
            show_cursor()
            return


def timer(minutes, message, on_break=False):
    """
    Prints the countdown numbers of the minutes passed.

    minutes(int): the amount of minutes that you want to countdown
    message(str): a message displayed on top of the countdown
    on_break(bool): is True whether the timer is used for a break, false otherwise
                    default param is False

    return: None
    """
    seconds = minutes * 60  # certain amount of seconds

    while seconds >= 0:
        clear()
        count_min = seconds // 60
        count_sec = seconds % 60

        if count_sec < 10:
            count_sec = f"0{count_sec}"

        if count_min < 10:
            count_min = f"0{count_min}"

        if not on_break:
            print(Fore.RED + message)
            print(
                Fore.RED
                + "➜  "
                + Style.RESET_ALL
                + Fore.YELLOW
                + f"{count_min}:{count_sec}  🍅"
                + Style.RESET_ALL
            )
        else:
            print(Fore.GREEN + message)
            print(
                Fore.GREEN
                + "➜  "
                + Style.RESET_ALL
                + Fore.YELLOW
                + f"{count_min}:{count_sec}  ☕"
                + Style.RESET_ALL
            )
        hide_cursor()
        time.sleep(1)
        seconds -= 1


def play_short_break_sound():
    """Plays the break sound. Needs input to continue."""
    playsound(BREAK_SOUND_PATH, False)
    input("Press enter to continue")


main()
