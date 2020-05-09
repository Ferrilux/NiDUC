import sys
import signal
import random
import math
import numpy as np
import cv2

# obsługa przerwań
def signal_handler(sig, frame):
    raise SystemExit

# wyświetlenie obrazu (klikniecie dowolnego klawisza mając
# aktywne okno obrazu zamyka obraz i kontynuuje program)
def show_img(image):
    window = 'image'
    cv2.imshow(window, image)
    key = -1
    while key < 0:
        key = cv2.waitKey(300)
    cv2.destroyAllWindows()

# konwersja obrazka na ciąg zer i jedynek
def img_to_bin(image):
    fstring = '{:08b}'
    size_x = len(image)
    size_y = len(image[0])
    bin_out = ''
    for i in range(size_x):
        for j in range(size_y):
            bin_out = bin_out + fstring.format(image[i][j])
    return {'x': size_x, 'y': size_y}, bin_out

# konwersja stringa z zerami i jedynkami na obrazek
def bin_to_img(bin_in, size):
    helper = []
    for i in range(int(len(bin_in)/8)):
        helper.append('')
        for j in range(8):
            index = i*8 + j
            helper[i] = helper[i] + bin_in[index]

    image = np.empty([size['x'], size['y']], 'uint8')
    for i in range(size['x']):
        for j in range(size['y']):
            index = i*size['y']+j
            image[i][j] = int(helper[index], 2)
    return image

# przekłamanie wartości podanej ilości losowych bitów
def gen_trans_err(bin_in, err_percent, seed=None):
    length = len(bin_in)
    bit_cnt = math.ceil(err_percent * length / 100)
    bin_in = list(bin_in)
    bin_out = ''
    # jeśli nie podano ziarna generowanie losowego ziarna w zakresie [0, INT_MAX]
    if not seed:
        seed = random.randint(0, sys.maxsize * 2 + 1)
    # użycie ziarna do generowania losowości
    random.seed(seed)

    for _ in range(bit_cnt):
        rand_l = random.randint(0, length-1)

        if bin_in[rand_l] == '1':
            bin_in[rand_l] = '0'
        else:
            bin_in[rand_l] = '1'
    for _, value in enumerate(bin_in):
        bin_out += value

    return bin_out, seed

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
