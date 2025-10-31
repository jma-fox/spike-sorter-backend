

def filter_trial_types(task_data):
    task_data = task_data[task_data["Outcome"].isin(["Correct"])]
    task_data = task_data[task_data['Cued'] == 1]
    task_data = task_data[task_data['GaborConfig'].isin([1])]
    task_data = task_data[task_data['TargQuad'] == 3]

    return task_data
