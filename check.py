#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.signal import find_peaks

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
    

x = np.load("/root/CMU-17722-Project-Breatheright/sample.npy")
peaks, params = find_peaks(x, height = 0.25 * np.mean(x), width = 20)
plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()

fs = 1/ 0.005
lowcut = 2
highcut = 6

x = np.load("/root/CMU-17722-Project-Breatheright/sample.npy")
x = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
peaks, params = find_peaks(x, height = 0.25 * np.mean(x), width = 20)
plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()

x = x[peaks]

dict = {}
dict[0] = "Inhaling"
dict[1] = "Exhaling"

x[x<0.6 * np.mean(params['peak_heights'])] = 0
x[x >0.6 * np.mean(params['peak_heights'])] = 1

breath_list = []
for i in range(len(x)):
    if(i!=0 and x[i-1]==x[i]):
        continue
    else:
        print(dict[x[i]])
        breath_list.append(dict[x[i]])

peaks, params = find_peaks(x, plateau_size = 2)
plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()

x[:] = 0
x[peaks] = 1
plt.plot(x)
plt.show()

# 1 - exh
# 0 -inhaling
