# What is the first thing we have to do
import time

from colorama import Fore, Style

from dcpy import clear


def timer(minutes):
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

        print(Fore.RED + "➜  " + Style.RESET_ALL + f"{count_min}:{count_sec}  🍅")
        time.sleep(1)
        seconds -= 1


def pomo(minutes):
    timer(minutes)
    return


def break_time(minutes):
    timer(minutes)
    return


def main():

    POMO = 50
    SHORT_BREAK = 10
    LONG_BREAK = 30

    return


main()
