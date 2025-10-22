import matplotlib.pyplot as plt
import spikeinterface.full as si
import streamlit as st


def plot_all_channels(sort_data):
    recording = sort_data["recording"]
    trial_frame = sort_data["trial_frame"]
    drop_channels = sort_data["drop_channels"]

    if drop_channels:
        recording = recording.remove_channels(drop_channels)

    fig, ax = plt.subplots()

    si.plot_traces(
        recording, 
        ax=ax, 
        time_range=trial_frame, 
        show_channel_ids=True, 
        add_legend=False
    )
    
    ax.set_ylabel('Channel')
    ax.set_xlabel('Time (s)')

    with st.expander("All Traces", expanded=True):
        st.pyplot(fig)
        plt.close(fig)

    sort_data["recording"] = recording

    return sort_data
