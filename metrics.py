# Python 2.7.15
import os

import museval
import librosa
import numpy as np

#TODO: ask about if metric computation should be mono

METRICS_SAMPLE_RATE = 44100

def metrics_from_numpy_arrays(real_sources, estimated_sources):
    """ real_sources : np.ndarray, shape=(nsrc, nsampl, nchan)
        estimated_sources : np.ndarray, shape=(nsrc, nsampl, nchan)
        Return values (all shapes=(nsrc, nwin)):
        - SDR: signal to distortion ratios
        - ISR: image to spatial distortion ratios
        - SIR: signal to interference ratios
        - SAR: signal to artifacts ratios
    """
    print(real_sources.ndim, estimated_sources.ndim)
    assert real_sources.ndim == estimated_sources.ndim == 3, 'metrics_from_numpy_arrays: inputs have invalid # of dims'
    museval.metrics.validate(real_sources, estimated_sources)
    sdr, isr, sir, sar, _ = museval.metrics.bss_eval(real_sources, estimated_sources, window=np.inf, hop=0)
    return sdr, isr, sir, sar

def load_audio(filepath, sr=METRICS_SAMPLE_RATE, is_mono=True):
    loaded_audio, _ = librosa.core.load(filepath, sr=sr, mono=is_mono)
    if is_mono:
        loaded_audio = np.expand_dims(loaded_audio, 1)
    else:
        loaded_audio = np.swapaxes(loaded_audio, 0, 1)
    return loaded_audio

def compute_results_from_directory(dirpath, estimated_suffix, true_suffix):
    estimated_filenames, true_filenames = [], []
    for filename in sorted(os.listdir(dirpath)):
        if filename.rfind('.') == -1:
            continue
        file_title = filename[:filename.rfind('.')]
        if file_title[-len(estimated_suffix):] == estimated_suffix:
            estimated_filenames.append(filename)
        elif file_title[-len(true_suffix):] == true_suffix:
            true_filenames.append(filename)

    estimated_waveforms = [load_audio(os.path.join(dirpath,f)) for f in estimated_filenames]
    true_waveforms = [load_audio(os.path.join(dirpath,f)) for f in true_filenames]

    estimated_nparrays = np.array(estimated_waveforms)
    true_nparrays = np.array(true_waveforms)
    all_sdr, all_isr, all_sir, all_sar = metrics_from_numpy_arrays(true_nparrays, estimated_nparrays)
    for i in range(len(all_sdr)):
        # Edit the following logic to take windows into account if windows are ever used.
        sdr, isr, sir, sar = float(all_sdr[i]), float(all_isr[i]), float(all_sir[i]), float(all_sar[i])
        print(estimated_filenames[i])
        print('SDR: {:.3f} \t ISR: {:.3f} \t SIR {:.3f} \t SIR: {:.3f}'.format(sdr, isr, sir, sar))

compute_results_from_directory('/Users/zhao/Downloads/test_metrics','estimate', 'true')