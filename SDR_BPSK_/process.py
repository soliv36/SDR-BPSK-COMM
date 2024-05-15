import numpy as np
import matplotlib.pyplot as plt
import rx

#Detects whether there is a signal in received samples by how much of the PSD is above a given threshold
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

#Puts all samples as either 1 or 0
def correct_received_signal(rx_samples):
    corrected_samples = []
    for s in rx_samples:
        if s >= 1:
            corrected_samples.append(1)
        
        if s <= -2:
            corrected_samples.append(0)

    return corrected_samples

#finds the index of the start of the sent data
def find_start_index(samples):
    start_data = [1, 1, 1, 0, 0, 0, 1, 1, 1] #need 2 sets of 24*3 ones, 24*3 zeroes
    index = 0
    count = 0
    start_data = False
    prev_pattern = 'none'

    while index < len(samples):
        if samples[index] == 1:
            while samples[index] == 1:
                count = count + 1
                index = index + 1

            if count == 24*3:
                if prev_pattern == 'zero':
                    return index
                elif prev_pattern == 'none':
                    prev_pattern = 'one'

                
            count = 0
        
        else:
            while samples[index] == 0:
                index = index + 1
                count = count + 1

            if count == 24*3:
                if prev_pattern == 'one':
                    prev_pattern = 'zero'

            count = 0

#finds the end index of sent data
def find_end_index(samples, start_index):
    end_encoding = [1, 1, 1, 1, 0, 1, 1, 1, 1]
    index = start_index
    count = 0
    start_data = False
    prev_pattern = 'none'

    while index < len(samples):
        if samples[index] == 1:
            while samples[index] == 1:
                count = count + 1
                index = index + 1

            if count == 24*4:
                if prev_pattern == 'zero':
                    return index - 24 * 9
                
                elif prev_pattern == 'none':
                    prev_pattern = 'one'

            count = 0
        
        else:
            while samples[index] == 0:
                index = index + 1
                count = count + 1

            if count == 24:
                if prev_pattern == 'one':
                    prev_pattern = 'zero'

            count = 0

#converts the samples to ascii binary
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

#converts the ascii binary to text
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

    fig0, axs0 = plt.subplots(2)

    axs0[0].plot(rx_samples[0:6000])
    axs0[0].set_title('Received samples')

    axs0[1].plot(corrected_samples[0:6000])
    axs0[1].set_title('Corrected samples')
    plt.show()

    start_index = find_start_index(corrected_samples)
    end_index = find_end_index(corrected_samples, start_index)

    print('Start', start_index)
    print('end', end_index)

    ascii = samples_to_ascii(corrected_samples, start_index, end_index)
    print(len(ascii))

    ascii_to_text(ascii)


    

