import signal
import random
import math
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

# konwersja obrazu czarno-białego do postaci zerojedynkowej
def bw_to_bin(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j]:
                image[i][j] = 1
    return image

# konwersja postaci zerojedynkowej na obraz czarno-biały
def bin_to_bw(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j]:
                image[i][j] = 255
    return image

# przekłamanie wartości podanej ilości losowych bitów
def gen_trans_err(data_bin, bit_cnt):
    for _ in range(bit_cnt):
        size_x = len(data_bin)
        size_y = len(data_bin[0])
        rand_x = random.randint(0, size_x-1)
        rand_y = random.randint(0, size_y-1)

        if data_bin[rand_x][rand_y]:
            data_bin[rand_x][rand_y] = 0
        else:
            data_bin[rand_x][rand_y] = 1
    return data_bin

def main():
    file = 'example.jpg'
    trans_err = 5 # liczba bitów do przekłamania w procentach

    # wczytanie pliku jpg w skali szarości
    image = cv2.imread(file, 0)
    show_img(image)

    # konwersja na czarno-biały
    bw_image = img_to_bw(image)
    show_img(bw_image)

    # przekłamanie losowych bitów
    data_bin = bw_to_bin(bw_image)
    print(data_bin)

    bit_count = len(data_bin) * len(data_bin[0])
    print("Długość przesyłanego ciągu bitów: ")
    print(bit_count)

    trans_err = trans_err/100
    data_bin = gen_trans_err(data_bin, math.ceil(bit_count * trans_err))
    print("Po przekłamaniu losowych bitów: ")
    print(data_bin)

    # wyświetlenie obrazu z przekłamanymi bitami
    bw_image = bin_to_bw(data_bin)
    show_img(bw_image)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
