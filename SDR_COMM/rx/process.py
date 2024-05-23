import numpy as np
import matplotlib.pyplot as plt

#correct the samples to be either 0 or 1
def correct_samples(samples):
    index = 0
    corrected_samples = []

    for sample in samples:
        if sample >= 1:
            corrected_samples.append(1)
        else:
            corrected_samples.append(0)
    
    return corrected_samples

#detects if the samples has a signal by counting consecutive ones or zeros (used on corrected samples)
def has_signal(samples):
    index = 0
    count = 0

    while True:
        if samples[index] == 0:
            while samples[index] == 0:
                count += 1
                index += 1

                if index == len(samples) or count > 24*16:
                    return False
            
            if count == 24*16:
                return True
            elif count > 24*16:
                return False
            else:
                count = 0
        else:
            while samples[index] == 1:
                count += 1
                index += 1

                if index == len(samples) or count > 24*16:
                    return False
            
            if count == 24*16:
                return True
            elif count > 24*16:
                return False
            else: 
                count = 0
            
            
#detects if the samples have been phase shifted (used if the samples have a confirmed signal)
def detect_phase(samples):
    index = 0
    count = 0

    while True:
        if samples[index] == 0:
            while samples[index] == 0:
                count += 1
                index += 1
            
                if index == len(samples):
                    return -1

            if count >= 24*8:
                temp = []
                for sample in samples:
                    if sample == 1:
                        temp.append(0)
                    else:
                        temp.append(1)

                return temp
        else:
            while samples[index] == 1:
                count += 1
                index += 1

                if index == len(samples):
                    return -1
                
            if count >= 24*8:
                return samples


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
    text = []

    for letter in letters:
        temp = ''.join(str(bit) for bit in letter)
        temp = int(temp, 2)
        temp = chr(temp)
        text.append(temp)

    return text