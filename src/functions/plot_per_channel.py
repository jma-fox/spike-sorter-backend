import matplotlib.pyplot as plt
import spikeinterface.full as si
import streamlit as st
import numpy as np


def plot_per_channel(sort_data):
    recording = sort_data["recording"]
    trial_frame = sort_data["trial_frame"]
    channel_ids = sort_data["channel_ids"]
    threshold = sort_data["threshold"]
    polarity = sort_data["polarity"]
    downsample_factor = 100000

    drop_channels = []
    with st.expander("Channel Traces", expanded=True):
        channel_ids = sorted(channel_ids, reverse=True)
        for channel in channel_ids:
            channel_trace = recording.get_traces(channel_ids=[channel])[::downsample_factor]
            channel_std = np.std(channel_trace)
            detection = threshold * polarity * channel_std

            fig, ax = plt.subplots()
            si.plot_traces(
                recording, 
                ax=ax, 
                time_range=trial_frame, 
                channel_ids=[channel], 
                add_legend=False
            )

            ax.axhline(detection, color='r', linestyle='-', alpha=0.7)
            ax.set_title(f'Channel {channel}')
            ax.set_xlabel('Time (s)')

            drop_channel = st.checkbox(f"Drop Channel {channel}", value=False)
            if drop_channel:
                drop_channels.append(channel)
            st.pyplot(fig)
            plt.close(fig)

    sort_data["drop_channels"] = drop_channels

    return sort_data
