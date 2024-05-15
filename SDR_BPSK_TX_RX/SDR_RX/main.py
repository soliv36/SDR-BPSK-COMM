import adi
import matplotlib.pyplot as plt
import numpy as np
import rx
import process
import sys

sample_rate = 1e6
center_freq = 915e6
buff_size = 4096

sdr = adi.Pluto("ip:192.168.2.1")
rx.config_rx(sdr, sample_rate, center_freq, buff_size, 'manual', -40)

is_signal = False
while is_signal == False:
    samples = sdr.rx()
    fft = np.fft.fft(samples)
    psd = np.abs(fft)**2
    x = np.fft.fftfreq(len(psd), 1/sample_rate)
    plt.plot(x, psd)
    plt.show()
    
    user_input = input('If the FFT looks like BPSk enter y, if not, enter n (enter / to quit): ')

    if user_input == 'y':
        is_signal = True
    elif user_input == '/':
        sys.exit()
    else:
        is_signal = False

if is_signal == True:
    #plot corrected samples
    fig0, axs0 = plt.subplots(2)
    axs0[0].plot(samples[0:2000])
    samples = process.correct_received_signal(samples)
    axs0[1].plot(samples[0:2000])


    start_index = process.find_start_index(samples)
    end_index = process.find_end_index(samples, start_index)

    ascii = process.samples_to_ascii(samples, start_index, end_index)

    text = process.ascii_to_text(ascii)
    print(text)
