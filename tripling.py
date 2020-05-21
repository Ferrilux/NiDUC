import signal
import cv2

from functions import (
    signal_handler,
    show_img,
    img_to_bin,
    bin_to_img,
    gen_trans_err,
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

def main():
    file = 'example.jpg'
    trans_err = 2 # liczba bitów do przekłamania w procentach
    multiple_by = 3 # liczba powielenia kazdego bitu

    # Wczytanie pliku jpg w skali szarości
    image = cv2.imread(file, 0)
    show_img(image)

    # Wyświetlenie obrazu
    size, data_bin = img_to_bin(image)

    # Powielenie bitów
    data_bin = multiple_bits(data_bin, multiple_by)

    # Przekłamanie losowych bitów
    data_bin, _ = gen_trans_err(data_bin, trans_err)

    # Wyświetlenie zakłóconego obrazu
    distorted_img = bin_to_img(demultiple_bits(data_bin, multiple_by), size)
    show_img(distorted_img)

    # Naprawa błędów
    fixed_data = demultiple_bits(fix_multiple_bits(data_bin, multiple_by), multiple_by)

    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_img(fixed_data, size)
    show_img(fixed_img)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
