import numpy as np
from scipy.io import loadmat
from statsmodels import robust
import mne
from scipy import signal

def performPrep(eeg, eog, refChan, srate, linenoise, referenceType='robust'):

    if refChan != 0:
        dim = np.shape(eeg)
        eeg_chans=np.setdiff1d(range(0, dim[0]), refChan-1) #remove the reference channel from the eeg channels
        eeg=eeg[eeg_chans,:]

    eeg=np.row_stack((eeg,eog)) #combine the eeg and eog matrices row-wise

    #perform high pass filtering and detrending
    mne.filter.filter_data(eeg, srate, 1, None, picks=None, filter_length='auto', l_trans_bandwidth='auto',
                           h_trans_bandwidth='auto', n_jobs=1, method='fir', iir_params=None, copy=True, phase='zero',
                           fir_window='hamming', fir_design='firwin', pad='reflect_limited', verbose=None)
    eeg = signal.detrend(eeg)


    #removing line noise
    mne.filter.notch_filter(eeg, srate, linenoise, filter_length='auto', notch_widths=None, trans_bandwidth=1, method='fir',
                            iir_params=None, mt_bandwidth=None, p_value=0.05, picks=None, n_jobs=1, copy=True,
                            phase='zero', fir_window='hamming', fir_design='firwin', pad='reflect_limited',
                            verbose=None)
    #finding bad channels

    dim = np.shape(eeg)
    channelsInterpolate = np.array(range(1, dim[0] + 1))
    nanChannelMask = np.zeros(dim[0])
    noSignalChannelMask = np.zeros(dim[0])
    badChannelsfromNans = np.zeros(dim[0])
    badChannelsfromNoData = np.zeros(dim[0])
    robustchanneldeviation = np.zeros(dim[0])
    badChannelFromDeviationMask = np.zeros(dim[0])
    badChannelFromDeviation=np.zeros(dim[0])
    channeldeviation = np.zeros(dim[0])
    for i in range(0, dim[0]):
        nanChannelMask[i] = np.int(np.sum(np.isnan(eeg[i, :])) > 0)

    for i in range(0, dim[0]):
        noSignalChannelMask[i] = np.int(robust.mad(eeg[i, :]) < 10 ** (-10) or np.std(eeg[i, :]) < 10 ** (-10))
    print(noSignalChannelMask)
    for i in range(0, dim[0]):
        if nanChannelMask[i] == 1:
            badChannelsfromNans[i] = i + 1
        if noSignalChannelMask[i] == 1:
            badChannelsfromNoData[i] = i + 1
    channelsInterpolate = np.setdiff1d(channelsInterpolate, np.union1d(badChannelsfromNans, badChannelsfromNoData)) #channels to be used for interpolation

    # find channels that are abnormally high or low amplitude
    for i in range(0, dim[0]):
        channeldeviation[i] = 0.7413 * (np.percentile(eeg[i, :], 75) - np.percentile(eeg[i, :], 25))

    channeldeviationSD = 0.7413 * (np.percentile(channeldeviation, 75) - np.percentile(channeldeviation, 25))
    channeldeviationMedian = np.nanmedian(channeldeviation)
    for i in range(0, dim[0]):
        robustchanneldeviation[i] = (channeldeviation[i] - channeldeviationMedian) / channeldeviationSD

    for i in range(0, dim[0]):
        badChannelFromDeviationMask[i] = np.int(abs(robustchanneldeviation[i]) > 5 or np.isnan(robustchanneldeviation[i]))
        if badChannelFromDeviationMask[i] == 1:
            badChannelFromDeviation[i]=i+1

    badChannels=np.union1d(np.union1d(badChannelsfromNoData, badChannelFromDeviation), badChannelsfromNans)


    #perform rereferencing and interpolation





