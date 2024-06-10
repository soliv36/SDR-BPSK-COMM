import adi
import numpy as np

def config_tx(sdr, sample_rate, center_freq, tx_hardwaregain_chan0):
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = int(tx_hardwaregain_chan0)

def config_rx(sdr, sample_rate, center_freq, num_samples, gain_control_mode_chan0, rx_hardwaregain_chan0):
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samples
    sdr.gain_control_mode_chan0 = gain_control_mode_chan0
    sdr.rx_hardwaregain_chan0 = int(rx_hardwaregain_chan0)

def transmit_receive_cyclic(sdr, samples):
    sdr.tx_cyclic_buffer = True
    sdr.tx(samples)

    for i in range(0, 10):
        raw_data = sdr.rx()

    rx_samples = sdr.rx()
    return rx_samples

def encode_bits(bits):
    start_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
    end_data =   [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    encoded = start_data + bits + end_data
    return encoded

def str_to_binary_list(text):
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

    return bits

def prepare_to_send(bits, repeat_num):
    bits = np.array(bits)
    x_degrees = bits*360/2.0
    x_radians = x_degrees*np.pi/180
    x_symbols = np.cos(x_radians) + 0.0j*np.sin(x_radians) #create complex samples
    samples = np.repeat(x_symbols, repeat_num)
    samples *= 2**14 #scale samples for Pluto SDR
    return samples

def correct_received_signal(rx_samples):
    corrected_samples = []
    for s in rx_samples:
        if s >= 1:
            corrected_samples.append(1)
        
        if s <= -2:
            corrected_samples.append(0)
    return corrected_samples

def decimate_samples(samples, dec_num):
    #Skip over the first group of 1s or 0s (because there probably won't be 24 of them)
    first_value = samples[0]
    start = 0
    while samples[start] == first_value:
        start += 1
        
    #Take every dec_num element (after the initial 1s or 0s)    
    decimated = samples[start::dec_num]
    return decimated
    
def invert_samples(samples):
    inverted_samples = []
    for sample in samples:
        if sample == 0:
            inverted_samples.append(1)
        elif sample == 1:
            inverted_samples.append(0)
    return inverted_samples
            

def find_start_index(samples):
    start_data = [1, 1, 1, 0, 0, 0, 1, 1, 1]
    inverted_check = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    
    start_data_length = 9
    samples_length = len(samples)
    num_starting_positions = samples_length - start_data_length + 1
    
    for index in range(num_starting_positions):
        
        samples_slice = samples[index:index + start_data_length] #Take a chunk of samples to compare
        if samples_slice == start_data:
            #Start sequence found
            return (index + start_data_length)
        
        elif samples_slice == inverted_check:
            #Samples was likely inverted
            return -2
        
        elif samples_slice == [0, 1, 0, 1, 0, 1, 0, 1, 0]:
            #The stop signal is likely being sent
            if samples[index: index + 18] == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
                #Stop signal is definitely being sent
                return -3
    
    return -1 #start data not found

def find_end_index(samples, start_index):
    #Check that start_index is valid
    if start_index < 0:
        return -2
    
    end_data = [1, 1, 1, 1, 0, 1, 1, 1, 1]
        
    end_data_length = 9
    samples_length = len(samples)
    num_starting_positions = samples_length - end_data_length + 1
    
    for index in range(start_index, num_starting_positions):
        if samples[index:index + end_data_length] == end_data:
            return index
    
    return -1 #end data not found


def ascii_to_text(samples):
    remainder = len(samples) % 8

    for i in range(0, remainder):
        samples.pop()

    letters =  [samples[i:i+8] for i in range(0, len(samples), 8)]
    
    message = []
    temp = ''
    for letter in letters:
        temp = ''.join(str(bit) for bit in letter)
        temp = int(temp, 2)
        temp = chr(temp)
        message.append(temp)
        
    return message
