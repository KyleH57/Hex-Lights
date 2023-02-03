import numpy as np
import pyaudio
import wave
from scipy.fft import rfft, rfftfreq
from matplotlib import pyplot as plt
import socket

import ledCtrl

UDP_IP = "192.168.0.156"
UDP_PORT = 4210

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

test167 = ledCtrl.square_LED_panel(8, 10)


# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     print(p.get_device_info_by_index(i))

bins = [70, 210, 350, 500, 750, 1000, 1500, 2000]

# function that takes a list of bins and max integer and returns a list of the power in each bin
def get_bin_power(bins, max_int):
    # find the index of the bins
    bin_index = []
    for i in range(len(bins)):
        bin_index.append(np.argmin(np.abs(xf - bins[i])))

    # find the power in each bin
    bin_power = []
    for i in range(len(bin_index)):
        bin_power.append(np.abs(yf[bin_index[i]]))

    # change to integers
    bin_power = [int(i) for i in bin_power]

    # normalize the power
    bin_power_normalized = [i / np.sum(bin_power) for i in bin_power]

    # multiply by maxInt and round up to nearest integer
    bin_power_normalized = [int(np.ceil(i * max_int)) for i in bin_power_normalized]

    return bin_power_normalized

sound = True
# CHUNK = 1024
CHUNK = 1837
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5000
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=1,
                frames_per_buffer=CHUNK)
print("* recording")
# frames = []
# fft_frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # data is a byte array that is really long
    data = stream.read(CHUNK)
    test123 = np.frombuffer(data, dtype=np.int16)  # the length is = to CHUNK
    yf = rfft(test123)
    xf = rfftfreq(CHUNK, 1 / RATE)

    #print(get_bin_power(bins, 8))

    #clear the panel
    ledCtrl.clearPanel(test167, client_socket)

    ledCtrl.drawColumn(get_bin_power(bins, 8), test167, client_socket, [0, 55, 0])

    # frames.append(data)

print("* done recording")

# convert byte array to numpy array
# test123 = np.frombuffer(frames[0], dtype=np.int16) #the length is = to CHUNK
test123 = np.frombuffer(data, dtype=np.int16)  # the length is = to CHUNK

plt.figure()

yf = rfft(test123)

# total_power = np.sum(np.abs(yf)**2)
# yf_normalized = np.abs(yf) / np.sqrt(total_power)


xf = rfftfreq(CHUNK, 1 / RATE)
plt.plot(xf, np.abs(yf))

plt.xlim(0, 2000)
# plt.show()

# plt.figure()

# #plot normalized fft
# plt.plot(xf, yf_normalized)
# plt.xlim(0, 2000)
#
# plt.figure()

# 8 bins from 70 to 2000



#
#
# # find the index of the bins
# bin_index = []
# for i in range(len(bins)):
#     bin_index.append(np.argmin(np.abs(xf - bins[i])))
#
# # print(bin_index)
#
# # find the power in each bin
# bin_power = []
# for i in range(len(bin_index)):
#     bin_power.append(np.abs(yf[bin_index[i]]))
#
# # change to integers
# bin_power = [int(i) for i in bin_power]
#
# # normalize the power
# bin_power_normalized = [i / np.sum(bin_power) for i in bin_power]
#
# # multiply by 8 round up to nearest integer
# bin_power_normalized = [int(np.ceil(i * 8)) for i in bin_power_normalized]
#
# print(bin_power_normalized)

# test data
test1 = [[8, 1, 1, 1, 1, 1, 1, 1], [1, 1, 5, 1, 2, 1, 1, 1], [4, 1, 1, 1, 1, 1, 1, 1], [4, 1, 2, 1, 1, 2, 1, 1],
         [1, 2, 2, 1, 2, 1, 2, 1]]

# stream.stop_stream()
# stream.close()
# p.terminate()
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

#ledCtrl.setPanelColor([5, 0, 0], test167)

#send data to arduino
#ledCtrl.sendPanelData(test167, client_socket)

#FRAME_RATE = 24

# drawAnimatedRing(0, 20, 100, 20, [0, 0, 5], FRAME_RATE, .6, p1, client_socket)
#
# drawAnimatedRing(0, 10, 50, 15, [5, 0, 0], FRAME_RATE, .4, p1, client_socket)
#
# drawAnimatedRing(-50, -50, 200, 15, [0, 5, 0], FRAME_RATE, 1, p1, client_socket)

#ledCtrl.drawAnimatedRing(-50, -50, 200, 15, [0, 5, 0], FRAME_RATE, 1, test167, client_socket)

client_socket.close()
