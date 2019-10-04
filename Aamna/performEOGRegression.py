import numpy as np


def performEOGRegression(eeg ,eog):

    """clean_eeg = performEOGRegression(eeg,eog)
        performs linear regression to remove eog artifacts from eeg data
        eeg and eog are input matrices
        clean_eeg is the eeg data matrix with no eog artifacts"""

    size_tuple = np.shape(eog)  # resizing the EOG array so that its pseudoinverse can be calculated
    dimension = len(size_tuple)
    if dimension == 1:
        eog.resize((1, size_tuple[0]))
    eeg_t = np.transpose(eeg)
    eog_t = np.transpose(eog)
    pseudoinv = np.linalg.pinv(np.dot(np.transpose(eog_t), eog_t))  # performing pseudoinverse
    inv = np.dot(pseudoinv,np.transpose(eog_t))
    subtract_eog = np.dot(eog_t,np.dot(inv,eeg_t))
    clean_eeg = np.transpose(np.subtract(eeg_t, subtract_eog))  # subtracting the EOG noise from the EEG signal
    return clean_eeg;





