import adi
import numpy as np
import numpy as np


"""
TX
"""
#converts a string to ascii binary
def str_to_binary(text):
    index = 0
    strings = []
    while index < len(text):
        strings.append(text[index])
        index = index + 1

    #convert to ascii binary
    strings = [bin(ord(char))[2:].zfill(8) for char in strings]

    #convert the list to indivdual bits
    bits = []

    for string in strings:
        for bit in string:
            bits.append(int(bit))

    print('bits: ',bits)
    return bits

#adds start and stop bits to the data
def frame_bits(bits):
    start_bits = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    stop_bits = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    framed_bits = np.concatenate((start_bits, bits, stop_bits))
    return framed_bits

#converts binary data to IQ samples
def bits_to_samples(bits):
    x_bits = np.array(bits)
    x_degrees = x_bits* -180 + 180
    x_radians = x_degrees*np.pi/180
    x_symbols = np.cos(x_radians) + 0.0j*np.sin(x_radians) #create complex samples
    samples = np.repeat(x_symbols, 24)
    samples *= 2**14

    return samples

#converts text to BPSK complex samples, returns a list
def text_to_bpsk_samps(text):
    bits = str_to_binary(text)
    bits = frame_bits(bits)
    samples = bits_to_samples(bits)
    return samples

"""
RX
"""
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

def has_stop_bits(samples):
    #start_stop_bits = [0, 0, 0, 0, 1, 1, 1, 1]
    index = 0
    count_ones = 0
    count_zeros = 0

    while index <= len(samples)/4:
        if samples[index] == 1:
            while samples[index] == 1 and index <= len(samples)/4:
                count_ones += 1
                index += 1
            if count_ones == 24*4 and count_zeros == 24*4:
                return True
            elif count_ones < 24*4 or count_ones > 24*4:
                count_ones = 0
                count_zeros = 0
            else:
                continue
        else:
            while samples[index] == 0 and index <= len(samples)/4:
                count_zeros += 1
                index += 1
            if count_zeros == 24*4 and count_ones == 24*4:
                return True
            elif count_zeros < 24*4 or count_zeros > 24*4:
                count_zeros = 0
                count_ones = 0
            else:
                continue

    return False


            







