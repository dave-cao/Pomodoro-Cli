# Display the pomodoro stats!

import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from colorama import Fore, Style
from PyInquirer import print_json, prompt

from config import config
from dcpy import clear

POMO_DATA_PATH = config.get("POMO_DATA_PATH", "./pomo_data.csv")
pd.options.mode.chained_assignment = None

# If file doesn't exist, write the headers
if not os.path.exists(POMO_DATA_PATH):
    with open(POMO_DATA_PATH, "w") as file:
        file.write("date,session_number,session_length,streak,description\n")

data = pd.read_csv(POMO_DATA_PATH)
data.date = pd.to_datetime(data.date)
now = datetime.now().strftime("%Y-%m-%d")
time_studied_in_days = data.groupby("date", as_index=False).agg(
    {"session_length": pd.Series.sum}
)
today_stats = data[data.date == now]


def get_stats():
    """Gives the user a menu choice on which stat to display"""
    main_questions = [
        {
            "type": "list",
            "name": "user_choice",
            "message": "What stat information would you like to see?",
            "choices": ["Daily Stats", "Streaks", "General Stats", "Other"],
        }
    ]

    clear()
    answers = prompt(main_questions)
    answer = answers.get("user_choice")
    try:
        if answer == "Daily Stats":
            display_daily_stats()
        elif answer == "Streaks":
            display_streak()
        elif answer == "General Stats":
            display_general_stats()
        elif answer == "Other":
            get_other_stats()
    except TypeError:
        print("Sorry, please start a pomodoro so I can get more information")


def get_other_stats():
    """Gives the user a menu choice on the 'other' option for stat displays"""
    other_questions = [
        {
            "type": "list",
            "name": "user_choice",
            "message": "What stat information would you like to see?",
            "choices": [
                "Hours Studied",
                "Get Random Session",
                "Maximum time studied for one day",
                "Get longest session number",
                "A line chart of time studied over days",
            ],
        }
    ]
    clear()
    answers = prompt(other_questions)
    answer = answers.get("user_choice")
    if answer == "Hours Studied":
        display_hours_studied()
    elif answer == "Get Random Session":
        display_random()
    elif answer == "Maximum time studied for one day":
        max_time_studied_one_day()
    elif answer == "Get longest session number":
        display_longest_session_number()
    elif answer == "A line chart of time studied over days":
        display_line_chart_time_over_days()


def description_message(message):
    """Styles the description on top of the stats displayed"""
    print(Fore.YELLOW + message + Style.RESET_ALL)


def max_time_studied_one_day():
    """Displays your maximum time studied in one day"""
    index_max = time_studied_in_days.session_length.idxmax()
    max_row = time_studied_in_days.loc[index_max]
    max_row["hours"] = max_row.session_length // 60
    max_row["minutes"] = max_row.session_length % 60

    print(max_row)


def display_line_chart_time_over_days():
    """Usings MatPlotLib, display a line chart of time studied over days"""
    plt.plot(time_studied_in_days.date, time_studied_in_days.session_length)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Total time studied that day (minutes)", fontsize=14)
    plt.title("Total time studied over every day.")
    plt.show()


def display_general_stats():
    """Tells you the general stats of the time studied each day."""
    description_message(
        "This tells you the general stats of the time studied each day. 'mean' is the average time studied per day."
    )
    time_studied_in_days["hours"] = round(time_studied_in_days.session_length / 60)
    print(time_studied_in_days.describe())


# Simple Displays
def display_longest_session_number():
    """Tells you the longest continuous pomodoro session that you've ever done"""
    max_session_number = data.session_number.max()
    description_message(
        "This tells you the longest continuous pomodoro sessions you've ever done.\n"
    )
    print(data[data.session_number == max_session_number])


def display_random():
    """Display a random pomodoro stat session to the user"""
    print(data.sample())


def display_daily_stats():
    """Prints all sessions for the day, current streak, and total time studied today"""
    print(today_stats)

    current_streak = today_stats.streak.max()
    print(f"\nYour current streak is: {current_streak}")
    display_total_time_studied_today()


def display_total_time_studied_today():
    """Prints total time studied today"""
    time = today_stats.session_length.sum()
    print(f"Total time studied today: {round(time // 60)}h {round(time % 60)}m")


def display_total_time_studied_alltime():
    """Prints total time studied for all time"""
    time = data.session_length.sum()
    print(f"Total time studied in total: {round(time // 60)}h {round(time % 60)}m")


def display_streak():
    """Display streak information"""
    description_message(
        "Contains streak information as well as the general data of current streak."
    )
    current_streak = today_stats.streak.max()

    print(f"Your current streak is: {current_streak}")
    print(f"Your max streak is: {data.streak.max()}\n")

    try:
        index_max = today_stats.streak.idxmax()
        print(data.loc[index_max])
    except ValueError:
        print("Complete a pomodoro to increase your streak!")


def display_hours_studied():
    """Display total hours studied (daily and alltime)"""
    display_total_time_studied_today()
    display_total_time_studied_alltime()
