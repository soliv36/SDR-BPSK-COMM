import numpy as np
import matplotlib.pyplot as plt

def is_signal(samples, threshold, percentage):
    fft = np.fft.fft(samples)
    fft = np.abs(samples)

    above_threshold = np.sum(fft > threshold)
    total_bin = len(fft)
    percentage_above = (above_threshold / total_bin) * 100
    
    if percentage_above >= percentage:
        return True
    else:
        return False
    
def correct_received_signal(rx_samples):
    corrected_samples = []
    for s in rx_samples:
        if s >= 1:
            corrected_samples.append(1)
        
        if s <= -2:
            corrected_samples.append(0)

    return corrected_samples


def find_start_index(samples):
    start_data = [1, 1, 1, 0, 0, 0, 1, 1, 1] #need 2 sets of 24*3 ones, 24*3 zeroes
    index = 0
    count = 0
    start_data = False
    prev_pattern = 'none'

    while index <= len(samples):
        if samples[index] == 1 and index <= len(samples):
            while samples[index] == 1 and index <= len(samples):
                count = count + 1
                index = index + 1

            if count == 24*3:
                if prev_pattern == 'zero':
                    return index
                elif prev_pattern == 'none':
                    prev_pattern = 'one'

                
            count = 0
        
        else:
            while samples[index] == 0 and index < len(samples):
                index = index + 1
                count = count + 1

            if count == 24*3:
                if prev_pattern == 'one':
                    prev_pattern = 'zero'

            count = 0

        if index == len(samples):
            return []


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
