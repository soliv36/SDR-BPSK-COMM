import adi
import numpy as np
import matplotlib.pyplot as plt
import process as pr
import tx_rx
import logging

#initialize logging
logging.basicConfig(level=logging.INFO)

#SDR setup
sample_rate = 1e6
rx_center_freq = 915e6
tx_center_freq = 900e6
rx_buff_size = 4096

sdr = adi.Pluto('ip:192.168.2.1')
tx_rx.config_rx(sdr, sample_rate, rx_center_freq, rx_buff_size, 'manual', 70.0)
tx_rx.config_tx(sdr, sample_rate, tx_center_freq, -40)

try:
    valid_text = []
    while True:
        samples = sdr.rx()
        samples = pr.correct_samples(samples)
        start_index = pr.find_index(samples[0:1000], 0, True)

        if start_index > 0:
            end_index = pr.find_index(samples, start_index, False)

            if end_index != -1:
                bits = pr.samples_to_bits(samples, start_index, end_index, 24) 
                text = pr.ascii_to_text(bits)

                if pr.is_valid_text(text):
                    valid_text.append(text)
                    if (all(i == valid_text[0] for i in valid_text) == True) and len(valid_text) == 3:
                        print(text) #print received message
                        tx_rx.tx_stop_bits(sdr) #send stop bits

                    elif (all(i == valid_text[0] for i in valid_text) == False) and len(valid_text) == 3:
                        valid_text = []

                    else:
                        continue
                    
except KeyboardInterrupt:
    logging.info('Keyboard Interrupt: destroying buffers, exiting')
    sdr.tx_destroy_buffer()
    sdr.rx_destroy_buffer()
finally:
    logging.INFO('Cleanup Done: exiting')
    exit(0)
                
        
