import adi
import numpy as np

#configures the Pluto SDR to receive samples
def config_rx(sdr, sample_rate, center_freq, num_samples, gain_control_mode_chan0, rx_hardwaregain_chan0):
    sdr.rx_lo = int(center_freq)
    sdr.rx_rf_bandwidth = int(sample_rate)
    sdr.rx_buffer_size = num_samples
    sdr.gain_control_mode_chan0 = gain_control_mode_chan0
    sdr.rx_hardwaregain_chan0 = int(rx_hardwaregain_chan0)

#computes the signal to noise ratio
def compute_snr(samples):
        signal_power = np.mean(np.abs(samples)**2)
        noise = samples - np.mean(samples)
        noise_power = np.mean(np.abs(noise)**2)
        snr = signal_power / noise_power
        snr_db = 10 * np.log10(snr)
        return snr_db
