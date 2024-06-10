#Receive message

import numpy as np
import adi
import tx_rx

#sdr config
sample_rate = 1e6
tx_center_freq = 910e6
rx_center_freq = 915e6
num_samples = 100000
sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

#setup transmit
tx_rx.config_tx(sdr, sample_rate, tx_center_freq, -20)

#setup recieve
tx_rx.config_rx(sdr, sample_rate, rx_center_freq, num_samples, 'manual', 20.0)

message = []
i = 0

#Receive and process samples
while True:
    rx_samples = sdr.rx()
    
    #save the samples to the file
    np.save('samples.npy', rx_samples)

    #load the samples
    rx_samples = np.load('samples.npy')
        
    corrected_samples = tx_rx.correct_received_signal(rx_samples)

    decimated_samples = tx_rx.decimate_samples(corrected_samples, 24)
    
    start_index = tx_rx.find_start_index(decimated_samples)
    
    if start_index == -2: #samples were probably inverted
        decimated_samples = tx_rx.invert_samples(decimated_samples)
        start_index = tx_rx.find_start_index(decimated_samples)

    end_index = tx_rx.find_end_index(decimated_samples, start_index)
    
    if ((start_index < 0) or (end_index < 1)):
        #start or end index isn't valid, so try sending and recieving again
        continue
    
    #Convert message to ascii text
    ascii = decimated_samples[start_index: end_index]
    text = tx_rx.ascii_to_text(ascii)
    message.append(text)
    
    #Check if this message matches the previous 2
    try:
        if (len(message) > 3) and (message[i] == message[i-1]) and (message[i-1] == message[i-2]):
            #Message matches the previous 2
            break
    except:
        #Error has occured, probably because they are not the same length
        i += 1
        continue
    i += 1

#Message received correctly, send stop message
print("Message:", ''.join(message[i]))
sdr.tx_destroy_buffer()
samples = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
samples = tx_rx.prepare_to_send(samples, 24)
for i in range (200):
    sdr.tx(samples)
