import cv2
import numpy as np

image = cv2.imread('example.jpg', 0)  # wczytanie pliku jpg

_, bw_img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)  # konwersja na tablice binara
cv2.imshow("Binary Image",bw_img) #testowe wyswietlenie przekonwertowanego obrazu

data_bin = np.empty([len(bw_img), len(bw_img[0])])
# zamiana wszystkich 255 na 1
for i in range(len(bw_img)):
    for j in range(len(bw_img[i])):
        if bw_img[i][j] > 0:
            data_bin[i][j] = 1
        else:
            data_bin[i][j] = 0

print(data_bin)
data_len = len(data_bin)
print("Długość przesyłanego ciągu bitów: ")
print(data_len * len(data_bin[0]))