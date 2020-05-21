import signal
import  cv2

from functions import (
    signal_handler,
    show_img,
    img_to_bin,
    bin_to_img,
    gen_trans_err,
)

# zakodowanie bitów za pomocą kodu Hamminga (7,4)
# skaczemy co 4 bity i kodujemy je
def encode_Hamming(bin_in):
    new_data = ""

    bin_in, zeros = add_zeros(bin_in)
    while len(bin_in) >= 4:
        
        new_data += append_parity(bin_in[0:4])
        bin_in = bin_in[4:]

    return new_data, zeros

# jeśli długość ciągu bitów nie jest wielokrotnością 4
# trzeba dopisać odpowiednio dużo 0, a od wyniku końcowego je odjąć
def add_zeros(bin_in):
    mod4 = len(bin_in) % 4
    added_zeros = 0

    if mod4 != 0:
        if mod4 == 1:
            bin_in.append('000')
            added_zeros = 3

        elif mod4 == 2:
            bin_in.append('00')
            added_zeros = 2

        elif mod4 == 3:
            bin_in.append('0')
            added_zeros = 1

    return bin_in, added_zeros

def delete_zeros(bin_in, zeros):
    if zeros == 0:
        return bin_in
    elif zeros == 1:
        bin_in = bin_in[:-1]
    elif zeros == 2:
        bin_in = bin_in[:-2]
    elif zeros == 3:
        bin_in = bin_in[:-3]
    return bin_in

# dodajemy do każdych 4 bitów (d1, d2, d3, d4 ) 3 bity kontrolne (p1, p2, p3)
# służące do kontroli parzystości bitów oryginalnych
# p1 = (d1 + d2 + d4) % 2
# p2 = (d1 + d3 + d4) % 2
# p3 = (d2 + d3 + d4) % 2
# zwracamy ciąg bitów w postaci p1 p2 d1 p3 d2 d3 d4
def append_parity(data):
    p1 = compute_parity(data, [0, 1, 3])
    p2 = compute_parity(data, [0, 2, 3])
    p3 = compute_parity(data, [1, 2, 3])
    return p1 + p2 + data[0] + p3 + data[1] + data[2] + data[3]


# obliczenie parzystości
# positions przekazuje, dla których bitów chcemy obliczyć parzystość
def compute_parity(bin_in, positions):
    temp = ""
    for i in positions:
        temp += bin_in[i]

    return str(str.count(temp, "1") % 2)


# odkodowanie bitów za pomocą kodu Hamminga (7,4)
# bin_in [0] jest parzystością pozycji 2 4 6
# bin_in [1] jest parzystością pozycji 2 5 6
# bin_in [3] jest parzystością pozycji 4 5 6
def decode_Hamming(bin_in, zeros):
    errors = 0
    corrected = 0
    new_data = ""
    bin_in = list(bin_in)

    while len(bin_in) >= 7:
        p1 = compute_parity(bin_in, [2,4,6])
        p2 = compute_parity(bin_in, [2,5,6])
        p3 = compute_parity(bin_in, [4,5,6])
        if p1 == bin_in[0] :
            if p2 == bin_in[1] :
                if p3 == bin_in[3] : #brak błędu w bitach parzystości
                    new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
                else : #błąd tylko dla p3
                    errors += 1
                    new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
            elif p3 == bin_in[3] : #błąd tylko dla p2
                errors += 1
                new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
            else : #błąd w p2 i w p3 i brak błędu w p1 = przekłamany bit bin_in[5]
                errors += 1
                corrected += 1
                if bin_in[5] == '1' :
                    bin_in[5] = '0'
                else:
                    bin_in[5] = '1'
                new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
        elif p2 == bin_in[1] :
            if p3 == bin_in[3] : #błąd tylko dla p1
                errors += 1
                new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
            else : #błąd dla p1 i dla p3 i brak błędu w p2 = przekłamany bit bin_in[4]
                errors += 1
                corrected += 1
                if bin_in[4] == '1' :
                    bin_in[4] = '0'
                else :
                    bin_in[4] = '1'
                new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
        elif p3 == bin_in[3] : #błąd dla p1 i p2 i brak błędu w p3 = przekłamany bit bin_in[2]
            errors += 1
            corrected += 1
            if bin_in[2] == '1' :
                bin_in[2] = '0'
            else :
                bin_in[2] = '1'
            new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
        else : # błąd dla p1, p2 i p3 = przekłamany bit bin_in[6]
            errors += 1
            corrected += 1
            if bin_in[6] == '1' :
                bin_in[6] = '0'
            else :
                bin_in[6] = '1'
            new_data = new_data + bin_in[2] + bin_in[4] + bin_in[5] + bin_in[6]
        bin_in = bin_in[7:]

    return delete_zeros(new_data, zeros)


def main():
    file = 'example_small.jpg'
    trans_err = 2  # liczba bitów do przekłamania w procentach

    # Wczytanie pliku jpg w skali szarości
    image = cv2.imread(file, 0)
    show_img(image)

    # Wyświetlenie obrazu
    size, data_bin = img_to_bin(image)

    # Zakodowanie bitów za pomocą kodu Hamminga
    data_bin, zeros = encode_Hamming(data_bin)

    # Przekłamanie losowych bitów
    data_bin, _ = gen_trans_err(data_bin, trans_err)

    # Odkodowanie bitów
    data_bin = decode_Hamming(data_bin, zeros)
   
    # Wyświetlenie naprawionego obrazu
    fixed_img = bin_to_img(data_bin, size)
    show_img(fixed_img)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
