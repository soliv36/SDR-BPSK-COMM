import adi
import numpy as np

#configures the Pluto SDR for transmitting
def config_tx(sdr, sample_rate, center_freq, tx_hardwaregain_chan0):
    sdr.tx_rf_bandwidth = int(sample_rate)
    sdr.tx_lo = int(center_freq)
    sdr.tx_hardwaregain_chan0 = int(tx_hardwaregain_chan0)

#function to send the stop bits to tell the other SDR to stop transmitting
def send_stop_bits(sdr):
    stop_bits = [1, 1, 1, 1, 1, 1, 1, 1]
    x_bits = np.array(stop_bits)
    x_degrees = x_bits*360/2.0
    x_radians = x_degrees*np.pi/180
    x_symbols = np.cos(x_radians) + 0.0j*np.sin(x_radians) #create complex samples
    samples = np.repeat(x_symbols, 24)

    for i in range(0, 10000):
        sdr.tx(stop_bits)