import numpy as np
import matplotlib.pyplot as plt

#detect if the samples received by the SDR contain a signal
def detect_signal(samples, threshold, percentage):
    fft = np.fft.fft(samples)
    fft = np.abs(samples)

    above_threshold = np.sum(fft > threshold)
    total_bin = len(fft)
    percentage_above = (above_threshold / total_bin) * 100
    
    if percentage_above >= percentage:
        return True
    else:
        return False
    
#calculate the PSD
def psd(samples, sample_rate):
    fft = np.fft.fft(samples)
    fft_freq = np.fft.fftfreq(len(samples), 1/sample_rate)
    psd = np.abs(fft)**2 / len(samples)

    return psd

#make the samples either ones or zeros
def correct_received_signal(rx_samples):
    corrected_samples = []
    for s in rx_samples:
        if s >= 1:
            corrected_samples.append(1)
        
        if s <= -1:
            corrected_samples.append(0)

    return corrected_samples

def synchronize(samples):
    new_samples = []
    index = 0
    count = 0

    while index <= len(samples):
        if samples[index] == 1:
            while samples[index] == 1:
                index += 1
                count += 1
            
            if count >= 24*8:
                return samples
            else:
                count = 0
        else:
            while samples[index] == 0:
                index += 1
                count += 1
            
            if count >= 24*8:
                for sample in samples:
                    if sample == 1:
                        new_samples.append(0)
                    else:
                        new_samples.append(1)
                return new_samples
            
            else:
                count = 0

#finds the index of the begining or the end of the data, is_start should equal True if looking for the start index, False otherwise
def find_index(samples, start_index, is_start):
    #start_stop_data = [1, 1, 1, 1, 1, 1, 1, 1]
    index = start_index
    count = 0

    while index < len(samples):
        if samples[index] == 1:
            while samples[index] == 1:
                count += 1
                index += 1
            
            if count >= 24*8:
                if is_start == True:
                    return index
                else:
                    return index - 24*16
            else:
                count = 0
        else:
            while samples[index] == 0:
                index += 1

#convert the binary to ascii binary
def samples_to_ascii(samples, start_index, end_index):
    index = start_index
    count = 0
    data = []

    while index <= end_index:
        if samples[index] == 0:
            if index + 24 <= len(samples):
                data.append(0)
                index = index + 24

        else:
            if index + 24 <= len(samples):
                data.append(1)
                index = index + 24
    return data

#convert the ascii to text
def ascii_to_text(samples):
    remainder = len(samples) % 8

    for i in range(0, remainder):
        samples.pop()

    letters =  [samples[i:i+8] for i in range(0, len(samples), 8)]

    for letter in letters:
        temp = ''.join(str(bit) for bit in letter)
        temp = int(temp, 2)
        temp = chr(temp)
        print(temp)

    
#load the samples
rx_samples = np.load('samples.npy')

#take the PSD
psd = psd(rx_samples, 1e6)

freq_axis = np.fft.fftfreq(len(rx_samples), 1/1e6)
plt.plot(freq_axis, psd)
plt.show()

#check whether the samples contain a signal or are just noise
is_signal = detect_signal(rx_samples, 2, 1)
print(is_signal)

plt.plot(rx_samples[0:4000])
plt.show()

if is_signal == True:
    corrected_samples = correct_received_signal(rx_samples)
    corrected_samples = synchronize(corrected_samples)

    fig0, axs0 = plt.subplots(2)

    axs0[0].plot(rx_samples[0:6000])
    axs0[0].set_title('Received samples')

    axs0[1].plot(corrected_samples[0:6000])
    axs0[1].set_title('Corrected samples')
    plt.show()

    start_index = find_index(corrected_samples, 0, True)
    end_index = find_index(corrected_samples, start_index, False)

    print('Start', start_index)
    print('end', end_index)

    ascii = samples_to_ascii(corrected_samples, start_index, end_index)

    ascii_to_text(ascii)
