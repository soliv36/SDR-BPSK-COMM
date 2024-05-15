import adi
import numpy as np
import keyboard
import tx

def str_to_binary_list(text):
    index = 0
    strings = []
    while index < len(text):
        strings.append(text[index])
        index = index + 1

    #convert to ascii binary
    strings = [bin(ord(char))[2:].zfill(8) for char in strings]

    #convert the list to indivdual bits
    bits = []

    for string in strings:
        for bit in string:
            bits.append(int(bit))

    return bits
    

sample_rate = 1e6
center_freq = 915e6

sdr = adi.Pluto("ip:192.168.2.1")

tx.config_tx(sdr, sample_rate, center_freq, -40)

run = True
while run == True:
    message = input("Enter something (type / to quit)")

    if message == '/':
        run = False

    else:
        message_bits = str_to_binary_list(message)
        tx.encode_bits(message_bits)
        tx.send_message(sdr, message_bits, sample_rate)

