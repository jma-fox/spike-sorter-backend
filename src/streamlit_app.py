import streamlit as st
import spikeinterface.full  as si
import pandas as pd

from functions.filter_trial_types import filter_trial_types
from functions.get_trial_frames import get_trial_frames
from functions.plot_all_channels import plot_all_channels
from functions.plot_per_channel import plot_per_channel
from functions.run_spike_sorter import run_spike_sorter
from functions.run_sort_analyzer import run_sort_analyzer


def streamlit_app():
    st.set_page_config(page_title="Spike Sorter")
    st.title("Spike Sorter")

    if 'sort_data' not in st.session_state:
        st.session_state['sort_data'] = None

    task_file_path = st.text_input("Task File Path:", "")
    recording_path = st.text_input("SI Recording Path:", "")

    st.write("")

    filter_trials = st.checkbox("Filter Trials", value=True)

    st.write("")

    event_name = st.text_input("Event Name:", value='gabors_on_time')
    frame_start = float(st.text_input("Frame Start (s):", value='-0.1'))
    frame_end = float(st.text_input("Frame End (s):", value='0.2'))

    st.write("")

    if st.button("Load Raw Data"):
        recording = si.load(recording_path)
        channel_ids = recording.get_channel_ids()
        task_data = pd.read_csv(task_file_path)

        if filter_trials:
            task_data = filter_trial_types(task_data)

        time_range = (frame_start, frame_end)
        trial_frames = get_trial_frames(task_data, time_range, event_name)

        sort_data = {
            "recording_path": recording_path,
            "recording": recording,
            "channel_ids": channel_ids,
            "trial_frames": trial_frames
        }

        st.session_state['sort_data'] = sort_data

    st.write("")

    sort_data = st.session_state.sort_data

    if sort_data is not None:
        trial_frames = sort_data['trial_frames']

        trial_num = st.slider("Trial Frame:", 1, len(trial_frames), 1)
        trial_frame = trial_frames[trial_num - 1]

        sort_data.update({'trial_frame': trial_frame})

        sort_data = plot_all_channels(sort_data)

        st.write("")

        threshold = float(st.text_input('Threshold (STD):', value='3.5'))
        polarity = int(st.text_input('Spike Polarity:', value=-1))

        sort_data.update({
            "threshold": threshold,
            "polarity": polarity
        })

        st.write("")

        sort_data = plot_per_channel(sort_data)

        st.write("")

        st.warning('Add channel menu and trace raster for selected channels here.')

        st.write("")

        if st.button("Analyze Spikes"):
            sort_data = run_spike_sorter(sort_data)
            sort_data = run_sort_analyzer(sort_data)


if __name__ == "__main__":
    streamlit_app()
