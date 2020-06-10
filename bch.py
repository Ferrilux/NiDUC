import signal
import numpy
import bchlib

from functions import (
    signal_handler,
    read_img,
    show_img,
    img_to_bin,
    bin_to_img,
    gen_trans_err,
    bin_diff,
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

def bin_to_bytes(bin_in):
    length = int(len(bin_in)/8)
    bytes_out = numpy.empty(length, 'uint8')

    for i in range(length):
        helper = ''
        for j in range(8):
            index = i*8 + j
            helper += bin_in[index]
        bytes_out[i] = int(helper, 2)
    return bytes_out

def bytes_to_bin(bytes_in):
    bin_out = ''
    fstring = '{:08b}'

    for _, value in enumerate(bytes_in):
        bin_out += fstring.format(value)
    return bin_out

def main():
    file = 'example_small.jpg'
    trans_err = 2  # liczba bitów do przekłamania w procentach

    # Stworzenie obiektu BCH
    BCH_POLYNOMIAL = 8219
    BCH_BITS = 16
    bch = bchlib.BCH(BCH_POLYNOMIAL,BCH_BITS)

    # Wczytanie pliku jpg w skali szarości
    image = read_img(file)
    show_img(image)

    # Wyświetlenie obrazu
    size, data_bin = img_to_bin(image)
    bin_before = data_bin

    # Zakodowanie bitów za pomocą kodu BCH
    coded_bin = bch.encode(bin_to_bytes(data_bin))

    # Przekłamanie losowych bitów
    corrupted_bin, _ = gen_trans_err(bytes_to_bin(coded_bin), trans_err)

    # Odkodowanie bitów
    decoded_bin = bch.decode(bin_to_bytes(corrupted_bin))
    bin_after = bytes_to_bin(decoded_bin)

    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_img(bin_after, size)
    show_img(fixed_img)

    print('Liczba bitow niezgodnych z oryginalnym obrazem: ' + str(bin_diff(bin_before, bin_after)))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
