import adi
import numpy as np
import matplotlib.pyplot as plt

sample_rate = 1e6
center_freq = 915e6
buff_size = 4096

def config_rx(sdr, sample_rate, center_freq, num_samples, gain_control_mode_chan0, rx_hardwaregain_chan0):
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samples
    sdr.gain_control_mode_chan0 = gain_control_mode_chan0
    sdr.rx_hardwaregain_chan0 = int(rx_hardwaregain_chan0)
