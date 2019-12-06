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
import matplotlib.pyplot as plt

def performPrep(eeg, refChan, srate, linenoise, referenceType='robust'):
    dim = np.shape(eeg)
    if refChan != 0:
        eeg_chans=np.setdiff1d(range(0, dim[0]), refChan-1) #remove the reference channel from the eeg channels
        eeg=eeg[eeg_chans,:]

    #finding bad channels

    #finding channels with NaNs or constant values for long periods of time
    org_dim = np.shape(eeg)

    originalChannels=np.arange(org_dim[0])
    channelsInterpolate=originalChannels
    nanChannelMask=[False]*org_dim[0]
    noSignalChannelMask = [False] * org_dim[0]

    for i in range(0, org_dim[0]):
        nanChannelMask[i] = np.sum(np.isnan(eeg[i, :])) > 0
    for i in range(0, org_dim[0]):
        noSignalChannelMask[i] = robust.mad(eeg[i, :]) < 10 ** (-10) or np.std(eeg[i, :]) < 10 ** (-10)
    badChannelsfromNans=channelsInterpolate[nanChannelMask]
    badChannelsfromNoData=channelsInterpolate[noSignalChannelMask]
    for i in range(0, org_dim[0]):
         if nanChannelMask[i]==True or noSignalChannelMask[i]==True:
            eeg=np.delete(eeg,i,axis=0)

    channelsInterpolate = np.setdiff1d(channelsInterpolate, np.union1d(badChannelsfromNans, badChannelsfromNoData)) #channels to be used for interpolation
    evaluationChannels=channelsInterpolate
    new_dim=np.shape(eeg)

    # find channels that have abnormally high or low amplitude
    robustchanneldeviation = np.zeros(org_dim[0])
    badChannelFromDeviationMask = [False] * (new_dim[0])
    channeldeviation = np.zeros(new_dim[0])
    for i in range(0, new_dim[0]):
        channeldeviation[i] = 0.7413 * iqr(eeg[i, :])

    channeldeviationSD = 0.7413 * iqr(channeldeviation)
    channeldeviationMedian = np.nanmedian(channeldeviation)
    robustchanneldeviation[evaluationChannels] = np.divide(np.subtract(channeldeviation, channeldeviationMedian),
                                                           channeldeviationSD)
    for i in range(0, new_dim[0]):
        badChannelFromDeviationMask[i] = abs(robustchanneldeviation[i]) > 5 or np.isnan(robustchanneldeviation[i])

    badChannelsfromDeviation = evaluationChannels[badChannelFromDeviationMask]

    #finding channels with high frequency noise
    if srate>100:
        eeg = np.transpose(eeg)
        dim = np.shape(eeg)
        X = np.zeros((dim[0], dim[1]))
        B=filter_design(100,A=np.array([1,1,0,0]),F=np.array([0,.36, 0.4, 1]),srate=250)
        for i in range(0, dim[1]):
            X[:, i] = signal.filtfilt(B, 1, eeg[:, i])

        noisiness = np.divide(robust.mad(np.subtract(eeg, X)), robust.mad(X))
        noisinessmedian = np.nanmedian(noisiness)
        noiseSD = np.median(np.absolute(np.subtract(noisiness,np.median(noisiness))))*1.4826
        zscoreHFNoise = np.divide(np.subtract(noisiness, noisinessmedian), noiseSD)
        HFnoisemask=[False]*new_dim[0]
        for i in range(0,new_dim[0]):
            HFnoisemask[i] = zscoreHFNoise[i] > 5 or np.isnan(zscoreHFNoise[i])
    else:
        X = eeg
        noisinessmedian = 0
        noisinessSD = 1
        zscoreHFNoise = np.zeros(dim[1], 1)
        badChannelsfromHFnoise=[]
    badChannelsfromHFnoise=evaluationChannels[HFnoisemask]
    #finding channels by correlation
    correlationSeconds = 1  # default value
    correlationFrames = correlationSeconds * srate
    correlationWindow = np.arange(correlationFrames)
    correlationOffsets = np.arange(1, dim[0] - correlationFrames, correlationFrames)
    Wcorrelation = len(correlationOffsets)
    maximumCorrelations = np.ones((org_dim[0], Wcorrelation))
    drop_out=np.zeros((dim[1],Wcorrelation))
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

    maximumCorrelations[evaluationChannels,:]=np.transpose(channelCorrelation)
    drop_out[:]=np.transpose(drop)
    noiselevels_out=np.transpose(noiselevels)
    channelDeviations_out=np.transpose(channelDeviations)
    thresholdedCorrelations=maximumCorrelations < 0.4
    thresholdedCorrelations=thresholdedCorrelations.astype(int)
    fractionBadCorrelationWindows=np.mean(thresholdedCorrelations,axis=1)
    fractionBadDropOutWindows=np.mean(drop_out,axis=1)


    badChannelsFromCorrelation = np.where(fractionBadCorrelationWindows > 0.01)
    badChannelsFromCorrelation_out = badChannelsFromCorrelation[:]
    badChannelsFromDropOuts = np.where(fractionBadDropOutWindows > 0.01)
    badChannelsFromDropOuts_out = badChannelsFromDropOuts[:]
    #medianMaxCorrelation = np.median(maximumCorrelations, 2);

    badChannelsfromSNR=np.union1d(badChannelsFromCorrelation_out,badChannelsfromHFnoise)
    noisyChannels = np.union1d(np.union1d(np.union1d(badChannelsfromDeviation, np.union1d(badChannelsFromCorrelation_out, badChannelsFromDropOuts_out)),badChannelsfromSNR),np.union1d(badChannelsfromNans,badChannelsfromNoData));
    print(noisyChannels)


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



a=loadmat('S001R04.mat')
b=loadmat('S01T.mat')
eeg=a['record']
performPrep(eeg,0,160,50)