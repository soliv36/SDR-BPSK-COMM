from rtlsdr import RtlSdr
import rx
import matplotlib.pyplot as plt
import numpy as np

sample_rate = 1e6
center_freq = 915e6
buff_size = 2048

sdr = RtlSdr()
rx.config_rtl(sdr, sample_rate, center_freq)

samples = rx.rx_rtl(sdr, buff_size)

plt.plot(samples)
plt.show()

"""
while True:
    samples = rx.rx_rtl(sdr, buff_size)

    samples = rx.correct_samples(samples)
    samples = rx.get_raw_data(samples)
    
    print(rx.decode(samples))
"""
