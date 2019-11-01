import mne
import numpy as np
from utilities import set_diff, remove_reference
from pyprep import noisy
from reference import ReferenceStruct
from scipy.signal import detrend
import logging
import matplotlib.pyplot as plt
from matplotlib import figure

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

raw = mne.io.read_raw_edf('S001R04.edf', preload=True)
sfreq = raw.info['sfreq']
raw.plot()

raw.rename_channels(lambda s: s.strip("."))
ch_names = raw.info['ch_names']

reference_out = ReferenceStruct()

reference_out.referenceChannels = ch_names
reference_out.evaluationChannels = ch_names

# Warn if evaluation and reference channels are not the same for robust
if not set(reference_out.referenceChannels) == set(reference_out.evaluationChannels):
    logger.warning('robustReference: Reference channels and'
                   'evaluation channels should be same for robust reference')

# Determine unusable channels and remove them from the reference channels
raw._data = detrend(raw.get_data())
# raw.plot()

signal_noisy = noisy.Noisydata(raw)
signal_noisy.find_all_bads()
unusable_channels = list(set(signal_noisy.bad_by_nan + signal_noisy.bad_by_flat))
reference_channels = set_diff(reference_out.referenceChannels, unusable_channels)

# Get initial estimate of the mean by the specified method
signal = raw.get_data()
ref_initial = np.median(raw.get_data(picks=reference_channels), axis=0)
unusable_index = [ch_names.index(ch) for ch in unusable_channels]
signal_tmp = remove_reference(signal, ref_initial, unusable_index)

# Remove reference from signal, iteratively interpolating bad channels
raw_tmp = raw.copy()

montage_kind = 'standard_1020'
montage = mne.channels.read_montage(kind=montage_kind, ch_names=raw_tmp.ch_names)
raw_tmp.set_montage(montage)

iterations = 0
noisy_channels_old = []
max_iteration_num = 4
while True:
    raw_tmp._data = signal_tmp
    raw_tmp.plot()
    plt.title('Iteration {}'.format(iterations), loc='center')
    signal_noisy = noisy.Noisydata(raw_tmp)
    signal_noisy.find_all_bads()
    noisy_channels = signal_noisy.get_bads()
    if iterations > 1 and (not noisy_channels or
                           set(noisy_channels) == set(noisy_channels_old)) or \
            iterations > max_iteration_num:
        break
    noisy_channels_old = noisy_channels.copy()

    if raw_tmp.info['nchan']-len(noisy_channels) < 2:
        logger.error('robustReference:TooManyBad '
                     'Could not perform a robust reference -- not enough good channels')

    if noisy_channels:
        raw_tmp._data = signal
        raw_tmp.info['bads'] = noisy_channels
        raw_tmp.interpolate_bads()
        signal_tmp = raw_tmp.get_data()
    else:
        signal_tmp = signal
    reference_signal = np.nanmean(raw_tmp.get_data(picks=reference_channels), axis=0)
    signal_tmp = remove_reference(signal, reference_signal, unusable_index)
    iterations = iterations + 1
    logger.info('Iterations: {}'.format(iterations))

logger.info('Robust reference done')
plt.show()
