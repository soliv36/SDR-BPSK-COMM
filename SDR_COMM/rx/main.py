import adi
import numpy as np
import matplotlib.pyplot as plt
import tx_rx
import process as pr


#SDR setup
sample_rate = 1e6
rx_center_freq = 915e6
tx_center_freq = 895e6
buff_size = 8192

sdr = adi.Pluto('ip:192.168.2.1')
tx_rx.config_rx(sdr, sample_rate, rx_center_freq, buff_size, 'manual', 70.0)
tx_rx.config_tx(sdr, sample_rate, tx_center_freq, -40)

while True:
    samples = sdr.rx()
    s_temp = samples
    samples = pr.correct_samples(samples)
    if pr.has_signal(samples) == True:
        plt.plot(np.real(s_temp), np.imag(s_temp), '.')
        plt.show()
        print('SAMPLES DETECTED')
        samples = pr.detect_phase(samples)
        if samples == -1:
            print('ERROR')
            exit()
        start_index = pr.find_index(samples, 0, True)
        end_index = pr.find_index(samples, start_index, False)
        ascii_samples = pr.samples_to_ascii(samples, start_index, end_index)
        text = pr.ascii_to_text(ascii_samples)
        if text == []:
            continue
        else:
            print(text)

        #send stop bits
