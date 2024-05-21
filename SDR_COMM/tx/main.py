import tx
import rx
import process as pr
import numpy as np
import adi
import matplotlib.pyplot as plt
import threading
import logging
import queue

#initialize logging
logging.basicConfig(level=logging.INFO)

#configure the SDR to receive and transmit
sample_rate = 1e6
center_freq_tx = 915e6
center_freq_rx = 900e6
rx_buff_size = 2048

sdr = adi.Pluto('ip:192.168.2.1')
tx.config_tx(sdr, sample_rate, center_freq_tx, -10)
rx.config_rx(sdr, sample_rate, center_freq_rx, rx_buff_size, 'manual', 70.0)


#get the data to send and convert to ascii binary
message = input('Enter a message to send: ')
bits = tx.str_to_binary(message)

#add the start and stop bits to the data, convert to IQ samples
bits = tx.frame_bits(bits)
samples = tx.bits_to_samples(bits)

#start the transmit thread
tx_thread = threading.Thread(target=tx.tx_cyclic(sdr, samples))
tx_thread.start()

#start the receive thread
output = queue.Queue()
rx_thread = threading.Thread(target=rx.receive_and_check_samples(sdr, output))
rx_thread.start()

#wait until the samples with the signal are received
rx_thread.join()
samples = output.get()

fft = np.fft.fftshift(np.fft.fft(samples))
plt.plot(samples)
plt.suptitle('FFT')
plt.show()

#correct the samples to be either 0 or 1
samples_correct = pr.correct_received_signal(samples)

#plot the corrected vs received signals
fig0, axs0 = plt.subplots(2)
axs0[0].plot(samples)
axs0[0].set_title('Received Samples')
axs0[1].plot(samples_correct)
axs0[1].set_title('Corrected Samples')
plt.show()

#check if the samples contain the stop sequence
contains_stop_bits = pr.find_stop_bits(samples_correct)

if samples_correct != -1:
    logging.info('Stop Received')
    tx.close_tx_buffer(sdr)
    tx_thread.join()
else:
    print('ERROR')
    exit(-1)
