import adi
import numpy as np
import rtlsdr

def config_rx(sdr, sample_rate, center_freq, num_samples, gain_control_mode_chan0, rx_hardwaregain_chan0):
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samples
    sdr.gain_control_mode_chan0 = gain_control_mode_chan0
    sdr.rx_hardwaregain_chan0 = int(rx_hardwaregain_chan0)

def rx(sdr):
    samples = sdr.rx()
    return samples

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
    
#returns a list of the value of the samples as 1 or 0
def correct_samples(rx_samples):
    corrected_samples = []
    for s in rx_samples:
        if s >= 1:
            corrected_samples.append(0)
        
        if s <= -2:
            corrected_samples.append(1)

    return corrected_samples

def get_raw_data(samples):
    #assume samples that are -1 are 1s and 1s are 0s, each message has 32 zeros encoded before and after it
    count = 0
    message = []
    index = 0

    #get start of first message
    while samples[index] != 1:
        index = index + 1


    while index <= len(samples):
        if samples[index] == 0:
            if index + 32 <= len(samples):
                for i in range(1, 32):
                    if samples[index + i] == 0:
                        count = count + 1
                    else:
                        break

                if count >= 20:
                    message.append(0)
                    index = index + 24


                else:
                    index = index + 32
                
            else:
                return message
            count = 0

        else:
            if index + 24 <= len(samples):
                message.append(1)
                index = index + 24

            else: 
                return message
            
def decode(message):
    letters =  [message[i:i+8] for i in range(0, len(message), 8)]

    for letter in letters:
        temp = ''.join(str(bit) for bit in letter)
        temp = int(temp, 2)
        temp = chr(temp)
        print(temp)

    





