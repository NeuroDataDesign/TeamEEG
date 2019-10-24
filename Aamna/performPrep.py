import numpy as np
from scipy.io import loadmat
from statsmodels import robust
import mne
from scipy import signal
from scipy.stats import iqr
import scipy.interpolate
import math
from cmath import sqrt
import numpy as np
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
    # performFilter(eeg,srate,filter_type='high',filter_freq=1)
    eeg = signal.detrend(eeg)


    #removing line noise
    mne.filter.notch_filter(eeg, srate, linenoise, filter_length='auto', notch_widths=None, trans_bandwidth=1, method='fir',
                            iir_params=None, mt_bandwidth=None, p_value=0.05, picks=None, n_jobs=1, copy=True,
                            phase='zero', fir_window='hamming', fir_design='firwin', pad='reflect_limited',
                            verbose=None)
    # performFilter(eeg,srate,filter_type='notch',filter_freq=50)

    #finding bad channels

    #finding channels with NaNs or constant values for long periods of time
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

    # find channels that have abnormally high or low amplitude
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

    #finding channels with high frequency noise
    if srate>100:
        eeg = np.transpose(eeg)
        dim = np.shape(eeg)
        X = np.zeros((dim[0], dim[1]))
        B=filter_design(100,A=np.array([1,1,0,0]),F=np.array([0,.36, 0.4, 1]),srate=250)
        for i in range(0, dim[1]):
            X[:, i] = signal.filtfilt(B, -1, eeg[:, i])
        noisiness = np.divide(robust.mad(np.subtract(eeg, X)), robust.mad(X))
        noisinessmedian = np.nanmedian(noisiness)
        noiseSD = robust.mad(noisiness) * 1.4826
        zscoreHFNoise = np.divide(np.subtract(noisiness, noisinessmedian), noiseSD)
        HFnoisemask = np.zeros(dim[1])
        for i in range(0, dim[1]):
            HFnoisemask[i] = np.int(np.int(zscoreHFNoise[i] > 5 or np.isnan(zscoreHFNoise[i])))

    else:
        X = eeg
        noisinessmedian = 0
        noisinessSD = 1
        zscoreHFNoise = np.zeros(dim[1], 1)

    #finding channels by correlation
    correlationSeconds = 1  # default value
    correlationFrames = correlationSeconds * srate
    correlationWindow = np.arange(correlationFrames)
    correlationOffsets = np.arange(1, dim[0] - correlationFrames, correlationFrames)
    Wcorrelation = len(correlationOffsets)
    channelCorrelation = np.ones((Wcorrelation, dim[1]))
    noiselevels = np.zeros((Wcorrelation, dim[1]))
    channelDeviations = np.zeros((Wcorrelation, dim[1]))
    drop = np.zeros((Wcorrelation, dim[1]))
    n = len(correlationWindow)
    XWin = np.reshape(np.transpose(X[0:n * Wcorrelation, :]), (dim[1], n, Wcorrelation), order='F')
    dataWin = np.reshape(np.transpose(eeg[0:n * Wcorrelation, :]), (dim[1], n, Wcorrelation), order='F')
    for k in range(0, Wcorrelation):
        eegportion = np.transpose(np.squeeze(XWin[:, :, k]))
        dataportion = np.transpose(np.squeeze(dataWin[:, :, k]))
        windowCorrelation = np.corrcoef(np.transpose(eegportion))
        abs_corr = np.abs(np.subtract(windowCorrelation, np.diag(np.diag(windowCorrelation))))
        channelCorrelation[k, :] = np.quantile(abs_corr, 0.98, axis=0)  # problem is here is solved
        noiselevels[k, :] = np.divide(robust.mad(np.subtract(dataportion, eegportion)), robust.mad(eegportion))
        channelDeviations[k, :] = 0.7413 * iqr(dataportion, axis=0)

    for i in range(0, Wcorrelation):
        for j in range(0, dim[1]):
            drop[i, j] = np.int(np.isnan(channelCorrelation[i, j]) or np.isnan(noiselevels[i, j]))
            if drop[i, j] == 1:
                channelDeviations[i, j] = 0
                noiselevels[i, j] = 0
#perform rereferencing and interpolation

def filter_design(N,A,F,srate):

            nfft = np.maximum(512, 2 ** (np.ceil(math.log(100) / math.log(2))))

            W = np.subtract(0.54, np.multiply(0.46, np.cos(np.divide(np.multiply(2 * math.pi, np.arange(N + 1)), N))))
            S = scipy.interpolate.PchipInterpolator(np.round(np.multiply(nfft, F)), A)
            F = S(np.arange(nfft + 1))
            F = np.multiply(F,np.exp(np.divide(np.multiply(-(0.5 * N) * sqrt(-1) * math.pi, np.arange(nfft + 1)), nfft)))
            B = np.real(np.fft.ifft(np.concatenate([F, np.conj(F[len(F) - 2:0:-1])])))
            B = np.multiply(B[0:N + 1], (np.transpose(W[:])))
            return B







