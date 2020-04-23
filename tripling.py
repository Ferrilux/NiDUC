import random
import cv2
import numpy as np

def img_to_bin(file):
    image = cv2.imread(file, 0)  # wczytanie pliku jpg

    _, bw_img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)  # konwersja na tablice binara
    #cv2.imshow("Binary Image",bw_img) #testowe wyswietlenie przekonwertowanego obrazu

    data_bin = np.empty([len(bw_img), len(bw_img[0])])
    # zamiana wszystkich 255 na 1
    for i in range(len(bw_img)):
        for j in range(len(bw_img[i])):
            if bw_img[i][j] > 0:
                data_bin[i][j] = 1
            else:
                data_bin[i][j] = 0
    return data_bin

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
    data_bin = img_to_bin('example.jpg')

    print(data_bin)
    data_len = len(data_bin)
    print("Długość przesyłanego ciągu bitów: ")
    print(data_len * len(data_bin[0]))

    print("Po przekłamaniu niektórych bitów: ")
    print(gen_trans_err(data_bin, 100000))

if __name__ == '__main__':
    main()
