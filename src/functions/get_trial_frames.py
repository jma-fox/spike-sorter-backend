

def get_trial_frames(task_data,time_range, event_name):
    trial_frames = []
    for onset_time in task_data[event_name]:
        start = onset_time + time_range[0]
        end = onset_time + time_range[1]
        trial_frame = (start, end)
        trial_frames.append(trial_frame)

    return trial_frames
