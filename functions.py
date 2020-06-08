import sys
import random
import math
import numpy as np
import cv2

# obsługa przerwań
def signal_handler(sig, frame):
    raise SystemExit

# wczytanie obrazu
def read_img(file):
    return cv2.imread(file, 1)

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
            bin_out = bin_out + fstring.format(image[i][j][0])
            bin_out = bin_out + fstring.format(image[i][j][1])
            bin_out = bin_out + fstring.format(image[i][j][2])
    return {'x': size_x, 'y': size_y}, bin_out

# konwersja stringa z zerami i jedynkami na obrazek
def bin_to_img(bin_in, size):
    helper = []
    for i in range(int(len(bin_in)/24)):
        helper.append('')
        for j in range(24):
            index = i*24 + j
            helper[i] = helper[i] + bin_in[index]

    image = np.empty([size['x'], size['y'], 3], 'uint8')
    for i in range(size['x']):
        for j in range(size['y']):
            index = i*size['y']+j
            image[i][j][0] = int(helper[index][:8], 2)
            image[i][j][1] = int(helper[index][8:16], 2)
            image[i][j][2] = int(helper[index][16:], 2)
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

def bin_diff(bin_1, bin_2):
    diff_count = 0
    for key, value in enumerate(bin_1):
        if bin_2[key] != value:
            diff_count += 1
    return diff_count
