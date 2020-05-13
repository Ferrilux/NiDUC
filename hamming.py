import sys
import signal
import random
import math
import numpy as np
import  cv2

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


# zakodowanie bitów za pomocą kodu Hamminga (7,4)
# skaczemy co 4 bity i kodujemy je
def encode_Hamming(bin_in):
    new_data = ""

    while len(bin_in) >= 4:
        new_data += append_parity(bin_in[0:4])
        bin_in = bin_in[4:]

    return new_data

# dodajemy do każdych 4 bitów (d1, d2, d3, d4 ) 3 bity kontrolne (t1, t2, t3)
# służące do kontroli parzystości bitów oryginalnych
# p1 = (d1 + d2 + d4) % 2
# p2 = (d1 + d3 + d4) % 2
# p3 = (d2 + d3 + d4) % 2
# zwracamy ciąg bitów w postaci p1 p2 d1 p3 d2 d3 d4
def append_parity(data):
    p1 = compute_parity(data, [0,1,3])
    p2 = compute_parity(data, [0,2,3])
    p3 = compute_parity(data, [1,2,3])
    return p1 + p2 + data[0] + p3 + data[1] + data[2] + data[3] 

# obliczenie parzystości 
# positions przekazuje, dla których bitów chcemy obliczyć parzystość
def compute_parity(bin_in, positions):
    temp = ""
    for i in positions:
        temp += bin_in[i]
    
    return str(str.count(temp, "1") % 2)

# odkodowanie bitów za pomocą kodu Hamminga (7,4)
def decode_Hamming(bin_in):
    errors = 0
    corrected = 0

    while len(bin_in) >= 7:
        new_data = bin_in[0:7]

        bin_in = bin_in[7:]

    return new_data

def main():
    file = 'example.jpg'
    trans_err = 2 # liczba bitów do przekłamania w procentach

    # Wczytanie pliku jpg w skali szarości
    image = cv2.imread(file, 0)
    show_img(image)

    # Wyświetlenie obrazu
    size, data_bin = img_to_bin(image)

    # Zakodowanie bitów za pomocą kodu Hamminga
    data_bin = encode_Hamming(data_bin)

    # Przekłamanie losowych bitów
    data_bin, _ = gen_trans_err(data_bin, trans_err)

    # Odkodowanie bitów
    data_bin = decode_Hamming(data_bin)

    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_img(data_bin, size)
    show_img(fixed_img)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
