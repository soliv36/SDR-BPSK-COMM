import adi
import numpy as np

def config_tx(sdr, sample_rate, center_freq, tx_hardwaregain_chan0):
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = int(tx_hardwaregain_chan0)

def encode_bits(bits):
    encoding = np.zeros((32,)) #encode the data with 32 zeros before and after
    encoding = encoding.tolist()

    encoded_bits = encoding + bits + encoding
    return encoded_bits

#convert text to a list of bits
def str_to_binary_list(text):
    index = 0
    text = str(text)
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

def send_message(sdr, x_bits, sample_rate):
    x_bits = encode_bits(x_bits) #encode the message
    x_bits = np.array(x_bits)
    x_degrees = x_bits*360/2.0
    x_radians = x_degrees*np.pi/180
    x_symbols = np.cos(x_radians) + 0.0j*np.sin(x_radians) #create complex samples
    samples = np.repeat(x_symbols, 24)
    samples *= 2**14 #scale samples for Pluto SDR

    #transmit samples 3 times to make sure message is received
    for i in range(3):
        sdr.tx(samples)
    
    sdr.tx_destroy_buffer()
