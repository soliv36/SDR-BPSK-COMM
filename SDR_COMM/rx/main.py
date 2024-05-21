import adi
import numpy as np
import matplotlib.pyplot as plt
import rx
import tx
import process as pr

#sdr setup
sample_rate = 1e6
center_freq_tx = 920e6
center_freq_rx = 900e6
rx_buff_size = 2048

sdr = adi.Pluto('ip:192.168.2.1')
tx.config_tx(sdr, sample_rate, center_freq_tx, -10)
rx.config_rx(sdr, sample_rate, center_freq_rx, rx_buff_size, 'manual',70.0)

while True:
    #receive samples
    samples = sdr.rx()
    #compute SNR
    snr = rx.compute_snr(samples)
    if snr <= .001:
        #look for bit pattern in the received samples
        samples = pr.correct_received_signal(samples)
        samples = pr.synchronize(samples)
        data_start_index = pr.find_index(samples, 0, True)
        data_end_index = pr.find_index(samples, data_start_index, False)
        data_binary = pr.samples_to_ascii(samples, data_start_index, data_end_index)
        text = pr.ascii_to_text(samples)
        print(text)
        tx.send_stop_bits(sdr)


