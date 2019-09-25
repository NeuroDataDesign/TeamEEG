import numpy as np
eeg_t=np.transpose(np.array([[1,2,4,0.8],[0.1,0.2,0.4,0.9]]))
eog_t=np.transpose(np.array([[9,10,11,12],[10,12,3,4]]))
pseudoinv=np.linalg.pinv(np.dot(np.transpose(eog_t),eog_t))
inv=np.dot(pseudoinv,np.transpose(eog_t))
subtract_eog=np.dot(eog_t,np.dot(inv,eeg_t))
cleanEEG=np.transpose(np.subtract(eeg_t,subtract_eog))
print(cleanEEG)




