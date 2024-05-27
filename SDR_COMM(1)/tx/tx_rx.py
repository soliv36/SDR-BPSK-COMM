import adi
import process as pr
import numpy as np

#configures the Pluto SDR to receive samples
def config_rx(sdr, sample_rate, center_freq, num_samples, gain_control_mode_chan0, rx_hardwaregain_chan0):
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samples
    sdr.gain_control_mode_chan0 = gain_control_mode_chan0
    sdr.rx_hardwaregain_chan0 = int(rx_hardwaregain_chan0)

#configures the Pluto SDR to transmit
def config_tx(sdr, sample_rate, center_freq, tx_hardwaregain_chan0):
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = int(tx_hardwaregain_chan0)
    sdr.tx_cyclic_buffer = True

def tx_samples(sdr, samples):
    #cyclic buffer has been enabled in tx config
    sdr.tx(samples)

def tx_destroy_buffer(sdr):
    sdr.tx_destroy_buffer()

def check_stop_tx(sdr):
    while True:
        samples = sdr.rx()
        samples = pr.correct_samples(samples)

        if pr.has_stop_bits == True:
            print('-------- Message Delivered --------')



