import pandas as pd


def get_task_data(task_file_path):
    task_data = pd.read_csv(task_file_path)
    task_data = task_data[task_data["Outcome"].isin(["Correct", "Miss"])]
    rf_x = task_data["RfPosX"].iloc[0]
    rf_y = task_data["RfPosY"].iloc[0]
    task_data = task_data[(task_data["TargPosX"] == rf_x) & (task_data["TargPosY"] == rf_y)]

    return task_data
