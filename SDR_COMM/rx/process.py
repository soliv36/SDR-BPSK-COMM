import numpy as np

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