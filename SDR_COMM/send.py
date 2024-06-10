#Send message

import numpy as np
import adi
import tx_rx

#sdr config
sample_rate = 1e6
tx_center_freq = 915e6
rx_center_freq = 910e6
num_samples = 100000
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

#setup transmit
tx_rx.config_tx(sdr, sample_rate, tx_center_freq, -20)

#setup recieve
tx_rx.config_rx(sdr, sample_rate, rx_center_freq, num_samples, 'manual', 20.0)

x_bits = input('Enter message to send: ')

x_bits = tx_rx.str_to_binary_list(x_bits)
x_bits = tx_rx.encode_bits(x_bits) #encode the message
samples = tx_rx.prepare_to_send(x_bits, 24)
    
#Send symbol while receiving samples
sdr.tx_cyclic_buffer = True
sdr.tx(samples)

#Receive and process samples to check for confirmation
while True:
    rx_samples = sdr.rx()
    
    #save the samples to the file
    np.save('samples.npy', rx_samples)

    #load the samples
    rx_samples = np.load('samples.npy')
        
    corrected_samples = tx_rx.correct_received_signal(rx_samples)
    
    decimated_samples = tx_rx.decimate_samples(corrected_samples, 24)
    
    start_index = tx_rx.find_start_index(decimated_samples)
    end_index = tx_rx.find_end_index(decimated_samples, start_index)
    
    if start_index == -3:
        #Stop signal found
        break
    elif ((start_index < 0) or (end_index < 1)):
        #start or end index isn't valid, so try sending and recieving again
        continue
    
sdr.tx_destroy_buffer()
print("Message successfully sent and received!")
