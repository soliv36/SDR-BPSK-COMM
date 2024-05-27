import adi
import numpy as np
import matplotlib.pyplot as plt
import logging
import threading
import tx_rx
import process as pr

#initialize logging
logging.basicConfig(level=logging.INFO)

#SDR setup
sample_rate = 1e6
center_freq_tx = 915e6
center_freq_rx = 900e6
rx_buff_size = 4096

sdr = adi.Pluto('ip:192.168.2.1')
tx_rx.config_tx(sdr, sample_rate, center_freq_tx, -30)
tx_rx.config_rx(sdr, sample_rate, center_freq_rx, rx_buff_size, 'manual', 70.0)
logging.info('Pluto configured')


try:
    #get the data to transmit
    data = input('Enter something to transmit: ')
    samples = pr.text_to_bpsk_samps(data)
    logging.info('BPSK samples created')

    #start the transmit thread
    tx_thread = threading.Thread(target=tx_rx.tx_samples, args=(sdr, samples))
    tx_thread.start()
    logging.info('Transmit thread started')

    #start the receive thread, wait for the stop bits to be received and stop transmitting
    rx_thread = threading.Thread(target=tx_rx.check_stop_tx, args=(sdr,))
    rx_thread.start()
    logging.info('Receive thread started')

    rx_thread.join()
    tx_thread.join()

    logging.info('Message transmitted... exiting')

except KeyboardInterrupt:
    logging.info('Keyboard Interrupt: closing tx buffer')
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()
finally:
    logging.info('Cleanup Done: exiting')