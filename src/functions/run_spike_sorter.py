from spikeinterface.core.globals import set_global_job_kwargs
from pathlib import Path
import spikeinterface.full as si


job_kwargs = {"pool_engine": "process", "n_jobs": 30}
set_global_job_kwargs(**job_kwargs)


def run_spike_sorter(sort_data):
    recording_path = sort_data["recording_path"]
    recording = sort_data["recording"]
    threshold = sort_data["threshold"]
    polarity = sort_data["polarity"]
    drop_channels = sort_data["drop_channels"]

    parent_dir = Path(recording_path).parent
    sorting_path = str(parent_dir / "sorting" / "si_sorting")

    if drop_channels:
        recording = recording.remove_channels(drop_channels)

    recording = si.common_reference(recording, reference="global", operator="median")
    
    sorting = si.run_sorter(
        sorter_name="mountainsort5",
        recording=recording,
        detect_sign=polarity,
        detect_threshold=threshold,
        whiten=True,
        folder=sorting_path,
        remove_existing_folder=True
    )

    sorting.save(folder=sorting_path, overwrite=True)

    sort_data["sorting_path"] = sorting_path
    sort_data["sorting"] = sorting

    return sort_data
