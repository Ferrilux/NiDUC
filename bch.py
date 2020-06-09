import signal
import cv2
import bchlib
import numpy

from functions import (
    signal_handler,
    show_img,
    img_to_bin,
    bin_to_img,
    gen_trans_err,
)

class BCH:
    def __init__(self, polynomial, bits):
        self.BCH_POLYNOMIAL = polynomial
        self.BCH_BITS = bits
        self.obj = bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)

    def encode(self, data):
        data = bytearray(data)
        ecc = self.obj.encode(data)
        packet = data + ecc
        packet = numpy.array(packet)
        
        return packet

    def decode(self, packet):
        packet = bytearray(packet)
        data, ecc = packet[:-self.obj.ecc_bytes], packet[-self.obj.ecc_bytes:]
        
        decoded = self.obj.decode_BCH(data, ecc)
        decoded_data = numpy.array(decoded[1])

        return decoded_data

def main():
    file = 'example_small.jpg'
    trans_err = 2  # liczba bitów do przekłamania w procentach

    # Stworzenie obiektu BCH
    BCH_POLYNOMIAL = 8219
    BCH_BITS = 16
    bch = bchlib.BCH(BCH_POLYNOMIAL,BCH_BITS)

    # Wczytanie pliku jpg w skali szarości
    image = cv2.imread(file, 0)
    show_img(image)

    # Wyświetlenie obrazu
    size, data_bin = img_to_bin(image)

    # Przekonwertowanie stringa na bajty - biblioteka bchlib działa na bajtach


    # Zakodowanie bitów za pomocą kodu BCH
    coded_bin = bch.encode(data_bin)

    # Przekłamanie losowych bitów
    corrupted_bin, _ = gen_trans_err(coded_bin, trans_err)

    # Odkodowanie bitów
    decoded_bin = bch.decode(corrupted_bin)

    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_img(decoded_bin, size)
    show_img(fixed_img)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()