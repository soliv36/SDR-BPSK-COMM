import numpy as np
import adi
import tx_rx
import matplotlib.pyplot as plt
import rx

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
    


#sdr config
sample_rate = 1e6
center_freq = 915e6
num_samples = 100000
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

#setup transmit
tx_rx.config_tx(sdr, sample_rate, center_freq, -40)

#setup recieve
tx_rx.config_rx(sdr, sample_rate, center_freq, num_samples, 'manual', 20.0)

#get message to send, convert to ascii binary
x_bits = input('Enter message: ')
x_bits = str_to_binary_list(x_bits)

x_bits = tx_rx.encode_bits(x_bits) #encode the message
x_bits = np.array(x_bits)
x_degrees = x_bits*360/2.0
x_radians = x_degrees*np.pi/180
x_symbols = np.cos(x_radians) + 0.0j*np.sin(x_radians) #create complex samples
samples = np.repeat(x_symbols, 24)

plt.plot(samples)
plt.show()

samples *= 2**14 #scale samples for Pluto SDR

#transmit and recieve the samples
rx_samples = tx_rx.transmit_receive_cyclic(sdr, samples)

#save the samples to the file
np.save('samples.npy', rx_samples)
