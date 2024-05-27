#correct the samples to be either 0 or 1
def correct_samples(samples):
    index = 0
    corrected_samples = []

    for sample in samples:
        if sample >= 1:
            corrected_samples.append(1)
        else:
            corrected_samples.append(0)
    
    return corrected_samples

#find the index of the start or stop bits in the corrected samples
def find_index(samples, start_index, is_start):
    #start_bits = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    #stop_bits = [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    error_tolerance = 3
    index = start_index
    count = 0
    num_8_bit_seqs = 0
    num_3_bit_seqs = 0
    count_total = 0

    while index != len(samples):
        if samples[index] == 1:
            while samples[index] == 1:
                index += 1
                count += 1

                if index == len(samples):
                    return -1

            if 24*8-error_tolerance <= count <= 24*8 + error_tolerance:
                num_8_bit_seqs += 1
                count_total += count
                if num_8_bit_seqs == 2 and num_3_bit_seqs == 1:
                    if is_start == True:
                        return index
                    else:
                        return index - (count_total-24)
            elif (24*3-error_tolerance <= count <= 24*3) + (error_tolerance and num_8_bit_seqs == 1):
                num_3_bit_seqs = 1
                count_total += count
            else:
                num_8_bit_seqs = 0
                num_3_bit_seqs = 0
                count_total = 0
            count = 0
        else:
            while samples[index] == 0 and index != len(samples):
                index += 1
                count += 1

                if index == len(samples):
                    return -1

            if 24*8-error_tolerance <= count <= 24*8 + error_tolerance:
                num_8_bit_seqs += 1
                count_total += count
                if num_8_bit_seqs == 2 and num_3_bit_seqs == 1:
                    if is_start == True:
                        return index
                    else:
                        return index - (count_total-24)
            elif (24*3-error_tolerance <= count <= 24*3) + (error_tolerance and num_8_bit_seqs == 1):
                num_3_bit_seqs = 1
                count_total += count
            else:
                num_8_bit_seqs = 0
                num_3_bit_seqs = 0
                count_total = 0
            count = 0
    return -1

#convert corrected samples to bits taking into account that they may not always be 24 samples per bit       
def samples_to_bits(samples, start_index, end_index, samps_per_symbol):
    count = 0
    index = 0
    count_append = 0
    samples = samples[start_index:end_index+1]
    temp = []

    while index <= len(samples):
        count_append = 0
        count = 0
        if samples[index] == 1:
            while samples[index] == 1 and index <= len(samples):
                count += 1
                index += 1

                if index == len(samples):
                    return temp
            
            count_append = round(count/samps_per_symbol)
            for i in range(0, count_append):
                temp.append(1)
        else:
            while samples[index] == 0 and index <= len(samples):
                count += 1
                index += 1

                if index == len(samples):
                    return temp
            
            count_append = round(count/samps_per_symbol)
            for i in range(0, count_append):
                temp.append(0)

    return temp

#convert ascii binary to text
def ascii_to_text(bits):
    remainder = len(bits) % 8

    for i in range(0, remainder):
        bits.pop()

    letters =  [bits[i:i+8] for i in range(0, len(bits), 8)]
    text = []

    for letter in letters:
        temp = ''.join(str(bit) for bit in letter)
        temp = int(temp, 2)
        temp = chr(temp)
        text.append(temp)

    return text

# Checks if the text received contains valid characters (alpha-numeric only)
def is_valid_text(text):
    for i in text:
        ascii_value = ord(i)
        if not (48 <= ascii_value <= 57 or 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122):
            return False
    return True




