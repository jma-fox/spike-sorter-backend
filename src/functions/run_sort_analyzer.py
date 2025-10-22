from spikeinterface.core.globals import set_global_job_kwargs
from pathlib import Path
import shutil
import spikeinterface.full as si


job_kwargs = {"pool_engine": "process", "n_jobs": 30}
set_global_job_kwargs(**job_kwargs)


def run_sort_analyzer(sort_data):
    recording_path = sort_data["recording_path"]
    recording = sort_data["recording"]
    sorting = sort_data["sorting"]

    parent_dir = Path(recording_path).parent
    analysis_path = parent_dir / "si_analysis"

    if analysis_path.exists():
        shutil.rmtree(analysis_path)

    analysis_path = str(analysis_path)
    analysis = si.create_sorting_analyzer(sorting=sorting, recording=recording, sparse=False)

    analysis.compute({
        'waveforms': {},
        'random_spikes': {},
        'noise_levels': {},
        'templates': {},
        'template_similarity': {},
        'unit_locations': {},
        'spike_amplitudes': {},
        'correlograms': {}
    })

    analysis.save_as(folder=analysis_path, format='binary_folder')

    sort_data["analysis_path"] = analysis_path
    sort_data["analyzer"] = analysis

    return sort_data
