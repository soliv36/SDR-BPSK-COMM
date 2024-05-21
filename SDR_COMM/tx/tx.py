import adi
import numpy as np
import logging

#configures the Pluto SDR to transmit
def config_tx(sdr, sample_rate, center_freq, tx_hardwaregain_chan0):
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = int(tx_hardwaregain_chan0)

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

    return bits

#adds start and stop bits to the data
def frame_bits(bits):
    start_stop_bits = [1, 1, 1, 1, 1, 1, 1, 1]
    encoded = start_stop_bits + bits + start_stop_bits
    return encoded

#converts binary data to IQ samples
def bits_to_samples(bits):
    x_bits = np.array(bits)
    x_degrees = x_bits*360/2.0
    x_radians = x_degrees*np.pi/180
    x_symbols = np.cos(x_radians) + 0.0j*np.sin(x_radians) #create complex samples
    samples = np.repeat(x_symbols, 24)
    samples *= 2**14

    return samples

#threading function to transmit the samples
def tx_cyclic(sdr, samples):
    logging.info("Transmit Thread Started")
    sdr.tx_cyclic_buffer = True
    sdr.tx(samples)

#destroys the transmit buffer
def close_tx_buffer(sdr):
    logging.info('Closing Transmit Buffer')
    sdr.tx_destroy_buffer()
    sdr.tx_enabled = False
    del sdr
