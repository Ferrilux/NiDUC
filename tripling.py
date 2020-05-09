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

# konwersja na obraz czarno-biały
def img_to_bw(image):
    _, bw_img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return bw_img

# konwersja obrazu czarno-białego do postaci zerojedynkowej listy
def bw_to_bin(image):
    size_x = len(image)
    size_y = len(image[0])
    bin_out = []
    for i in range(size_x):
        for j in range(size_y):
            if image[i][j]:
                bin_out.append(1)
            else: 
                bin_out.append(0)
    return {'x': size_x, 'y': size_y}, bin_out

# konwersja postaci zerojedynkowej listy na obraz czarno-biały
def bin_to_bw(bin_in, size):
    image = np.empty([size['x'], size['y']])
    for i in range(size['x']):
        for j in range(size['y']):
            index = i*size['y']+j
            if bin_in[index]:
                image[i][j] = 255
            else:
                image[i][j] = 0
    return image

# przekłamanie wartości podanej ilości losowych bitów
def gen_trans_err(data_bin, err_percent, seed=None):
    length = len(data_bin)
    bit_cnt = math.ceil(err_percent * len(data_bin) / 100)
    
    if not seed:
        seed = random.randint(0, sys.maxsize * 2 + 1)
    random.seed(seed)
    
    for _ in range(bit_cnt):
        rand_l = random.randint(0, length-1)

        if data_bin[rand_l]:
            data_bin[rand_l] = 0
        else:
            data_bin[rand_l] = 1
    return data_bin, seed

# powielenie bitów
def multiple_bits(bin_in, bit_cnt):
    bin_out = []
    for _, value in enumerate(bin_in):
        for _ in range(bit_cnt):
            bin_out.append(value)
    return bin_out

# odpowielenie bitów
def demultiple_bits(bin_in, bit_cnt):
    bin_out = []
    for i in range(int(len(bin_in)/bit_cnt)):
        index = i*bit_cnt
        bin_out.append(bin_in[index])
    return bin_out

# naprawa przekłamań w powielonych bitach
def fix_multiple_bits(bin_in, bit_cnt):
    bin_out = []
    for i in range(int(len(bin_in)/bit_cnt)):
        ones_cnt = 0
        set_all = 0
        index = i*bit_cnt
        for j in range(bit_cnt):
            if bin_in[index+j]:
                ones_cnt = ones_cnt + 1
        if ones_cnt > bit_cnt/2:
            set_all = 1
        for _ in range(bit_cnt):
            bin_out.append(set_all)
    return bin_out

def main():
    file = 'example.jpg'
    trans_err = 5 # liczba bitów do przekłamania w procentach
    multiple_by = 3 # liczba powielenia kazdego bitu
    
    # wczytanie pliku jpg w skali szarości
    image = cv2.imread(file, 0)
    show_img(image)

    # konwersja na czarno-biały
    bw_image = img_to_bw(image)
    show_img(bw_image)

    # Konwersja do listy zero-jedynkowej
    size, data_bin = bw_to_bin(bw_image)

    # Powielenie bitów
    data_bin = multiple_bits(data_bin, multiple_by)

    # Przekłamanie losowych bitów
    data_bin, seed = gen_trans_err(data_bin, trans_err, 123)

    # Wyświetlenie zakłóconego obrazu
    distorted_img = bin_to_bw(demultiple_bits(data_bin, multiple_by), size)
    show_img(distorted_img)

    # Naprawa błędów
    fixed_data_bin = demultiple_bits(fix_multiple_bits(data_bin, multiple_by), multiple_by)

    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_bw(fixed_data_bin, size)
    show_img(fixed_img)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
