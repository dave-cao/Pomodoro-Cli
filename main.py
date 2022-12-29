#!/user/bin/python3
"""
Pomodoro CLI

The purpose of this program is a simple CLI solution to the Pomodoro technique. It's fast, works, and records data properly. 

I wanted to make a customizable and simple time tracker variant using the Pomodoro technique.
"""
import csv
import os
import time
from datetime import datetime, timedelta

from colorama import Fore, Style
from playsound import playsound
from PyInquirer import prompt

from config import config
from dcpy import clear, hide_cursor, show_cursor
from stats import get_stats

# USER CHANGEABLE VARIABLES
POMO = config.get("POMO")
SHORT_BREAK = config.get("SHORT_BREAK")
LONG_BREAK = config.get("LONG_BREAK")
SESSIONS_UNTIL_LONG_BREAK = config.get("SESSIONS_UNTIL_LONG_BREAK", 2)
ALARM_PATH = config.get("ALARM_PATH")
BREAK_SOUND_PATH = config.get("BREAK_SOUND_PATH")
POMO_DATA_PATH = config.get("POMO_DATA_PATH")


def main():
    """Questions the user on the main function of the app"""
    questions = [
        {
            "type": "list",
            "name": "user_choice",
            "message": "Start Pomo or view stats?",
            "choices": ["Start Pomo", "View Stats"],
        }
    ]

    clear()
    answers = prompt(questions)
    answer = answers.get("user_choice")
    if answer == "Start Pomo":
        play()
    elif answer == "View Stats":
        get_stats()


def play():

    # APP VARIABLES
    streak = 1
    session_number = 0
    total_minutes_studied_today = 0
    desired_sessions = SESSIONS_UNTIL_LONG_BREAK
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    while True:
        try:

            # ============= Getting Stats ======================== #

            # Read data and get total minutes studied today
            with open(POMO_DATA_PATH, "r") as file:
                reader = csv.DictReader(file, delimiter=",")
                for row in reader:
                    if row.get("date") == today:
                        total_minutes_studied_today += float(
                            row.get("session_length", 0)
                        )
                    if row.get("date") == yesterday:
                        streak = int(row.get("streak", 0)) + 1

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

            # ================ STREAKS ================= #

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
                fieldnames = [
                    "date",
                    "session_number",
                    "session_length",
                    "streak",
                    "description",
                ]
                writer = csv.DictWriter(
                    csv_file, fieldnames=fieldnames, lineterminator=os.linesep
                )
                writer.writerow(
                    {
                        "date": today,
                        "session_number": session_number,
                        "session_length": POMO,
                        "streak": streak,
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
