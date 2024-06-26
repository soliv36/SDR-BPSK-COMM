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

#add the start and stop sequence to the bits, tells when the data starts and ends
def frame_bits(bits):
    start_stop_bits = [1, 1, 1, 1, 1, 1, 1, 1]
    encoded = start_stop_bits + bits + start_stop_bits
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
    
