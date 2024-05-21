import numpy as np

#correct the samples so that the only possible values are 1 and 0
def correct_received_signal(rx_samples):
    corrected_samples = []
    for s in rx_samples:
        if s >= 1:
            corrected_samples.append(1)
        
        if s <= -1:
            corrected_samples.append(0)

    return corrected_samples

#detect if the stop bits are found in the received samples
def find_stop_bits(samples):
    #stop_bits = [1, 1, 1, 1, 1, 1, 1, 1]
    index = 0
    count = 0

    if samples[index] == 1:
        while samples[index] == 1:
            count += 1
            index += 1
        
        if count >= 24*8:
            return index
        else:
            count = 0
    else:
        while samples[index] == 0:
            count += 1
            index += 1
        
        if count >= 24*8:
            return index
        else:
            count = 0

    return -1