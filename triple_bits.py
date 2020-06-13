import signal
from sys import argv
from math import ceil
from numpy import arange

from functions import (
    signal_handler,
    read_img,
    show_img,
    img_to_bin,
    bin_to_img,
    gen_trans_err,
    bin_diff,
)

# powielenie bitów
def multiple_bits(bin_in, bit_cnt):
    bin_out = ''
    for _, value in enumerate(bin_in):
        for _ in range(bit_cnt):
            bin_out += value
    return bin_out

# odpowielenie bitów
def demultiple_bits(bin_in, bit_cnt):
    bin_out = ''
    for i in range(int(len(bin_in)/bit_cnt)):
        index = i*bit_cnt
        bin_out += bin_in[index]
    return bin_out

# naprawa przekłamań w powielonych bitach
def fix_multiple_bits(bin_in, bit_cnt):
    bin_out = ''
    for i in range(int(len(bin_in)/bit_cnt)):
        ones_cnt = 0
        set_all = '0'
        index = i*bit_cnt
        for j in range(bit_cnt):
            if bin_in[index+j] == '1':
                ones_cnt = ones_cnt + 1
        if ones_cnt > bit_cnt/2:
            set_all = '1'
        for _ in range(bit_cnt):
            bin_out += set_all
    return bin_out

def test():
    file = 'example_small.jpg'
    multiple_by = 3 # liczba powielenia kazdego bitu

    print('err,bitcnt,unfixed')
    for i in arange(2, 10.1, 0.1):
        trans_err = round(i, 1)

        # Wczytanie obrazu z pliku
        image = read_img(file)

        _, data_bin = img_to_bin(image)
        bin_before = data_bin

        # Powielenie bitów
        data_bin = multiple_bits(data_bin, multiple_by)

        # Przekłamanie losowych bitów
        data_bin, _ = gen_trans_err(data_bin, trans_err)

        # Naprawa błędów
        fixed_data = demultiple_bits(fix_multiple_bits(data_bin, multiple_by), multiple_by)
        bin_after = fixed_data

        bit_cnt = bin_diff(bin_before, bin_after)
        diff_bits = round(bit_cnt*100/len(bin_after), 4)
        print(str(trans_err) + ',' + str(bit_cnt) + ',' + format(diff_bits, '.4f'))

def main():
    file = 'example_small.jpg'
    trans_err = 2 # liczba bitów do przekłamania w procentach
    multiple_by = 3 # liczba powielenia kazdego bitu

    # Wczytanie obrazu z pliku
    image = read_img(file)
    show_img(image)

    # Wyświetlenie obrazu
    size, data_bin = img_to_bin(image)
    bin_before = data_bin

    # Powielenie bitów
    data_bin = multiple_bits(data_bin, multiple_by)

    # Przekłamanie losowych bitów
    data_bin, _ = gen_trans_err(data_bin, trans_err)

    # Wyświetlenie zakłóconego obrazu
    distorted_img = bin_to_img(demultiple_bits(data_bin, multiple_by), size)
    show_img(distorted_img)

    # Naprawa błędów
    fixed_data = demultiple_bits(fix_multiple_bits(data_bin, multiple_by), multiple_by)
    bin_after = fixed_data

    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_img(fixed_data, size)
    show_img(fixed_img)

    print('Liczba bitow niezgodnych z oryginalnym obrazem: ' + str(bin_diff(bin_before, bin_after)))

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    if len(argv) > 1:
        if argv[1] == 'test':
            test()
        else:
            print('Invalid argument')
    else:
        main()
