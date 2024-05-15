import adi
import tx
import time
import sys

#configure SDR
sample_rate = 1e6
center_freq = 915e6
sdr = adi.Pluto("ip:192.168.2.1")
tx.config_tx_pluto(sdr, sample_rate, center_freq, 20)

#get the data from the user
data = ''
while True:
    data = input('Enter something (type / to quit): ')

    if data == '/':
        sys.exit()

    #convert to binary and transmit
    data = tx.str_to_binary_list(input)
    tx.send_message(sdr, data, sample_rate)


