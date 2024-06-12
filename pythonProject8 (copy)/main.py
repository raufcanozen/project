
'''
import numpy as np


with open('message.txt', 'r') as file:
    hex_data = file.read().strip()


binary_data = ''.join(format(int(c, 16), '04b') for c in hex_data)


assert len(binary_data) == 64 * 64 * 4


matrix = np.array([list(map(int, binary_data[i:i + 256])) for i in range(0, len(binary_data), 256)])


def trng(input_data):

    print(f"sonuc: {input_data}")


for row in matrix:
    trng(row)


with open('message.txt', 'r') as file:
    data = file.read().strip()

# Veriyi 64x64'lük matrise dönüştürme
n = 64
matrix = [data[i:i+n] for i in range(0, len(data), n)]

# Her elemanı 4 bitlik binary elemanına dönüştürme
binary_matrix = []
for row in matrix:
    binary_row = [format(int(row[i:i+1], 16), '04b') for i in range(len(row))]
    binary_matrix.append(binary_row)

# PRNG fonksiyonunu tanımlama
def prng(input_bits):
    # Bu örnek için basit bir PRNG fonksiyonu kullanıyorum
    import random
    random.seed(int(input_bits, 2))
    return [random.getrandbits(1) for _ in range(512)]

# Her bir satırı PRNG ile işleme
prng_outputs = []
for row in binary_matrix:
    input_bits = ''.join(row)
    prng_output = prng(input_bits)
    prng_outputs.append(prng_output)

# Sonuçları ekrana yazdırma
for i, output in enumerate(prng_outputs):
    print(f"Row {i+1}: {output}")


import matplotlib.pyplot as plt
import random
import hashlib

def create_map(height, width):
    # Kare harita oluştur
    map = [['.' for _ in range(width)] for _ in range(height)]
    return map

def plot_map(map, keys_list):
    # Haritayı çiz
    plt.figure(figsize=(len(map[0]) / 3, len(map) / 3))
    for y in range(len(map)):
        for x in range(len(map[0])):
            if any((x, y) in keys for keys in keys_list):
                plt.plot(x, y, 'gs', markersize=15)  # Anahtarları yeşil kare olarak çiz
            elif map[y][x] == '#':
                plt.plot(x, y, 'ks', markersize=15)  # Kenarları kare olarak çiz
            else:
                plt.plot(x, y, 'ws', markersize=15)  # İç kısmı boşluk olarak çiz
    plt.xticks(range(len(map[0])))
    plt.yticks(range(len(map)))
    plt.grid(True)
    plt.gca().invert_yaxis()  # Koordinat düzlemini ters çevir
    plt.show()

def generate_start_points(map, shape_width):
    # Başlangıç noktalarını üret
    height = len(map)
    width = len(map[0])
    start_points = []
    for _ in range(3):  # 3 farklı tetris parçası için başlangıç noktası üret
        start_x = random.randint(0, width - shape_width)  # Harita sınırları içinde rastgele x koordinatı seç
        start_y = random.randint(0, height - 4)  # Harita sınırları içinde rastgele y koordinatı seç
        start_points.append((start_x, start_y))
    return start_points

def generate_keys(map, start_points, shape_index):
    # Anahtarları oluştur
    keys_list = []
    # Örnek olarak 5 farklı tetris şekli oluşturalım
    tetris_shapes = [
        [[(0, 0), (1, 0), (2, 0), (3, 0)],  # Uzun şekil
         [(0, 0), (0, 1), (0, 2), (0, 3)]],

        [[(0, 0), (1, 0), (0, 1), (1, 1)]],  # Kare

        [[(0, 0), (1, 0), (1, 1), (2, 1)],  # L şekli
         [(1, 0), (1, 1), (0, 1), (0, 2)],
         [(0, 0), (1, 0), (1, -1), (2, -1)],
         [(0, 0), (0, 1), (1, 1), (1, 2)]],

        [[(0, 1), (1, 1), (1, 0), (2, 0)],  # T şekli
         [(1, 0), (1, 1), (0, 1), (1, 2)],
         [(0, 0), (1, 0), (1, -1), (2, 0)],
         [(1, 0), (0, 1), (1, 1), (2, 1)]],

        [[(0, 0), (1, 0), (1, 1), (2, 1)],  # Ters L şekli
         [(0, 0), (0, 1), (1, 1), (1, 2)],
         [(0, 0), (1, 0), (1, -1), (2, -1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    ]
    chosen_shape = tetris_shapes[shape_index]

    for start in start_points:
        shape_start_x, shape_start_y = start
        keys = []
        for shape in chosen_shape:
            for x, y in shape:
                keys.append((shape_start_x + x, shape_start_y + y))
        keys_list.append(keys)
    return keys_list

def generate_key(shape_index):
    shapes = [
        [[(0, 0), (1, 0), (2, 0), (3, 0)],  # Uzun şekil
         [(0, 0), (0, 1), (0, 2), (0, 3)]],

        [[(0, 0), (1, 0), (0, 1), (1, 1)]],  # Kare

        [[(0, 0), (1, 0), (1, 1), (2, 1)],  # L şekli
         [(1, 0), (1, 1), (0, 1), (0, 2)],
         [(0, 0), (1, 0), (1, -1), (2, -1)],
         [(0, 0), (0, 1), (1, 1), (1, 2)]],

        [[(0, 1), (1, 1), (1, 0),(2, 0)],  # T şekli
         [(1, 0), (1, 1), (0, 1), (1, 2)],
         [(0, 0), (1, 0), (1, -1), (2, 0)],
         [(1, 0), (0, 1), (1, 1), (2, 1)]],

        [[(0, 0), (1, 0), (1, 1), (2, 1)],  # Ters L şekli
         [(0, 0), (0, 1), (1, 1), (1, 2)],
         [(0, 0), (1, 0), (1, -1), (2, -1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    ]

    chosen_shape = shapes[shape_index]
    chosen_rotation = random.choice(chosen_shape)

    # Anahtar oluştur
    key = hashlib.sha256(str(chosen_rotation).encode()).hexdigest()
    return key

def main():
    try:
        height = int(input("Harita yüksekliğini girin: "))
        width = int(input("Harita genişliğini girin: "))
        if height <= 0 or width <= 0:
            print("Geçersiz boyut! Pozitif bir tam sayı girin.")
            return
        # Harita oluştur
        map = create_map(height, width)
        # Tetris şekillerinin en geniş kısmının genişliğini belirle
        max_shape_width = max([len(shape[0]) for shape in [
            [(0, 0), (1, 0), (2, 0), (3, 0)],  # Uzun şekil
            [(0, 0), (1, 0), (0, 1), (1, 1)],  # Kare
            [(0, 0), (1, 0), (1, 1), (2, 1)],  # L şekli
            [(0, 1), (1, 1), (1, 0), (2, 0)],  # T şekli
            [(0, 0), (1, 0), (1, 1), (2, 1)]   # Ters L şekli
        ]])
        # Başlangıç noktalarını üret
        start_points = generate_start_points(map, max_shape_width)
        # Anahtarları üret
        print("Kullanılabilir Tetris Şekilleri:")
        print("0: Uzun Şekil")
        print("1: Kare")
        print("2: L Şekli")
        print("3: T Şekli")
        print("4: Ters L Şekli")
        shape_index = int(input("Lütfen bir tetris şekli seçin (0-4): "))
        if shape_index < 0 or shape_index > 4:
            print("Geçersiz seçim! Lütfen 0 ile 4 arasında bir sayı girin.")
            return
        keys_list = generate_keys(map, start_points, shape_index)
        # Harit çiz
        print("Oluşturulan Harita:")
        plot_map(map, keys_list)
        # Anah üret
        key = generate_key(shape_index)
        print("Oluşturulan Anahtar:", key)
    except ValueError:
        print("Geçersiz giriş! Bir tam sayı girin.")

if _name_ == "_main_":
    main()

import matplotlib.pyplot as plt
import random
import hashlib


def create_map(height, width):
    # Kare harita oluştur
    map = [['.' for _ in range(width)] for _ in range(height)]
    return map


def plot_map(map, keys_list):
    # Haritayı çiz
    plt.figure(figsize=(len(map[0]) / 3, len(map) / 3))
    for y in range(len(map)):
        for x in range(len(map[0])):
            if any((x, y) in keys for keys in keys_list):
                plt.plot(x, y, 'gs', markersize=15)  # Anahtarları yeşil kare olarak çiz
            elif map[y][x] == '#':
                plt.plot(x, y, 'ks', markersize=15)  # Kenarları kare olarak çiz
            else:
                plt.plot(x, y, 'ws', markersize=15)  # İç kısmı boşluk olarak çiz
    plt.xticks(range(len(map[0])))
    plt.yticks(range(len(map)))
    plt.grid(True)
    plt.gca().invert_yaxis()  # Koordinat düzlemini ters çevir
    plt.show()


def generate_start_points(map, shape_width):
    # Başlangıç noktalarını üret
    height = len(map)
    width = len(map[0])
    start_points = []
    for _ in range(3):  # 3 farklı tetris parçası için başlangıç noktası üret
        start_x = random.randint(0, width - shape_width)  # Harita sınırları içinde rastgele x koordinatı seç
        start_y = random.randint(0, height - 4)  # Harita sınırları içinde rastgele y koordinatı seç
        start_points.append((start_x, start_y))
    return start_points


def generate_keys(map, start_points, shape_index):
    # Anahtarları oluştur
    keys_list = []
    # Örnek olarak 3 farklı tetris şekli oluşturalım
    tetris_shapes = [
        [[(0, 0), (1, 0), (0, 1), (1, 1)]],  # Kare
        [[(0, 0), (1, 0), (1, 1), (2, 1)],  # L şekli
         [(1, 0), (1, 1), (0, 1), (0, 2)],
         [(0, 0), (1, 0), (1, -1), (2, -1)],
         [(0, 0), (0, 1), (1, 1), (1, 2)]],
        [[(0, 1), (1, 1), (1, 0), (2, 0)],  # T şekli
         [(1, 0), (1, 1), (0, 1), (1, 2)],
         [(0, 0), (1, 0), (1, -1), (2, 0)],
         [(1, 0), (0, 1), (1, 1), (2, 1)]]
    ]
    chosen_shape = tetris_shapes[shape_index]

    for start in start_points:
        shape_start_x, shape_start_y = start
        keys = []
        for shape in chosen_shape:
            for x, y in shape:
                keys.append((shape_start_x + x, shape_start_y + y))
        keys_list.append(keys)
    return keys_list


def generate_key(shape_index):
    shapes = [
        [(0, 0), (1, 0), (0, 1), (1, 1)],  # Kare
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # L şekli
        [(0, 1), (1, 1), (1, 0), (2, 0)]  # T şekli
    ]

    chosen_shape = shapes[shape_index]
    chosen_rotation = random.choice(chosen_shape)

    # Anahtar oluştur
    key = hashlib.sha256(str(chosen_rotation).encode()).hexdigest()
    return key


def main():
    try:
        height = int(input("Harita yüksekliğini girin: "))
        width = int(input("Harita genişliğini girin: "))
        if height <= 0 or width <= 0:
            print("Geçersiz boyut! Pozitif bir tam sayı girin.")
            return

        # Harita oluştur
        map = create_map(height, width)

        # Başlangıç noktalarını ve anahtarları oluştur
        start_points = generate_start_points(map, 4)  # 4, şekillerin maksimum genişliğidir.
        keys_list = []
        for i in range(3):  # 3 anahtar oluştur
            keys_list.extend(generate_keys(map, start_points, i))

        # Anahtarları çiz
        plot_map(map, keys_list)

        # Kullanıcıdan hangi şekilin anahtarını oluşturmak istediğini sor
        shape_index = int(input("Lütfen bir şekil seçin (0-2): "))
        if shape_index < 0 or shape_index > 2:
            print("Geçersiz seçim! Lütfen 0 ile 2 arasında bir sayı girin.")
            return

        # Anahtarları oluştur ve XOR ile anahtarı hesapla
        key = generate_key(shape_index)
        print(f"Seçilen şekil için anahtar: {key}")

    except ValueError:
        print("Geçersiz bir değer girdiniz, lütfen bir tam sayı girin.")


if _name_ == "_main_":
    main()
    '''
import random

def generate_map(min_value, max_value, size):
    return [[random.randint(min_value, max_value) for _ in range(size)] for _ in range(size)]

def xor_encrypt(numbers, key):
    return [number ^ key for number in numbers]

def produce_key(map, start_x, start_y, path_choice):
    size = len(map)
    x, y = start_x, start_y
    key = 0

    for _ in range(size * size):  # Ensure the entire map can be traversed at least once
        key ^= map[x][y]
        if path_choice == 1:  # Horizontal right
            y = (y + 1) % size
        elif path_choice == 2:  # Vertical down
            x = (x + 1) % size
        elif path_choice == 3:  # Diagonal down right
            x = (x + 1) % size
            y = (y + 1) % size

    return key

def main():
    min_value = int(input("Enter the minimum value: "))
    max_value = int(input("Enter the maximum value: "))
    size = int(input("Enter the size of the map: "))

    map = generate_map(min_value, max_value, size)

    start_x = random.randint(0, size - 1)
    start_y = random.randint(0, size - 1)
    path_choice = random.randint(1, 3)
    key = produce_key(map, start_x, start_y, path_choice)
    print(f"Generated key: {key}")

    s1 = int(input('Enter the first number: '))
    s2 = int(input('Enter the second number: '))

    user_numbers = [random.randint(min_value, max_value) for _ in range(s1, s2)]
    print(f"User numbers: {user_numbers}")

    encrypted_numbers = xor_encrypt(user_numbers, key)
    print(f"Encrypted numbers: {encrypted_numbers}")

if __name__ == "__main__":
    main()
