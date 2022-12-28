# Display the pomodoro stats!

import pandas as pd

POMO_DATA_PATH = "./pomo_data.csv"

data = pd.read_csv(POMO_DATA_PATH)


print(data.session_length.sum())
