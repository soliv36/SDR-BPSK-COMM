import adi
import numpy as np

#configure the Pluto SDR to transmit samples
def config_tx(sdr, sample_rate, center_freq, tx_hardwaregain_chan0):
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = int(tx_hardwaregain_chan0)

#configure the Pluto SDR to receive samples
def config_rx(sdr, sample_rate, center_freq, num_samples, gain_control_mode_chan0, rx_hardwaregain_chan0):
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samples
    sdr.gain_control_mode_chan0 = gain_control_mode_chan0
    sdr.rx_hardwaregain_chan0 = int(rx_hardwaregain_chan0)

#transmit and receive samples at the same time
def transmit_receive_cyclic(sdr, samples):
    sdr.tx_cyclic_buffer = True
    sdr.tx(samples)

    for i in range(0, 10):
        raw_data = sdr.rx()

    rx_samples = sdr.rx()
    return rx_samples

#add a sequence of bits before and after the data given
def encode_bits(bits):
    start_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
    end_data =   [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    encoded = start_data + bits + end_data
    return encoded
    
