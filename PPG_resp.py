
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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


def read_window(line, period):
    i = 0
    line.flush()
    window = np.empty(period)
    while( i < period):
        window[i] = line.readline()
        i += 1
    return window



fs = 1/ 0.005
# lowcut = 2
# highcut = 6
lowcut = 4
highcut = 10

dict_resp = {}
dict_resp[0] = "Inhaling"
dict_resp[1] = "Exhaling"


line = serial.Serial('/dev/cu.usbmodem144201')
window = read_window(line, 1000)
print("ok")
j = 0

try:
    while(j < 5000):
        rt_data= read_window(line, 3)
        window = np.concatenate([window[3:], rt_data])
        x = window
        x = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)
        peaks, params = find_peaks(x, height = 0.25 * np.mean(x), width = 20)

        x = x[peaks]

        x[x < 0.6 * np.mean(params['peak_heights'])] = 0
        x[x > 0.6 * np.mean(params['peak_heights'])] = 1


        breath_list = []
        print(dict_resp[x[-1]])
                

        peaks, params = find_peaks(x, plateau_size = 2)
        
        
        j+=1

    line.close()

except:
    line.close()





