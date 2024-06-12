import matplotlib.pyplot as plt
import random
import hashlib




def create_map():
    # Kullanıcıdan harita boyutlarını al
    height = int(input("Haritanın yüksekliğini girin: "))
    width = int(input("Haritanın genişliğini girin: "))

    # Kare harita oluştur
    map = [['o'for _ in range(width)] for _ in range(height)]
    return map


# Haritayı oluştur ve ekrana yazdır
harita = create_map()
for row in harita:
    print(" ".join(row))


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

        # Başlangırları oluştur
        start_points = generate_start_points(map, 4)  # 4, şekillerin maksimum genişliğidir.
        keys_list = []
        for i in range(3):  # 3 anahtar oluştur
            keys_list.extend(generate_keys(map, start_points, i))

        # An
        plot_map(map, keys_list)

        # Kullanıcıdan hangi şekilin ana
        shape_index = int(input("Lütfen bir şekil seçin (0-2): "))
        if shape_index < 0 or shape_index > 2:
            print("Geçersiz seçim! Lütfen 0 ile 2 arasında bir sayı girin.")
            return

                key = generate_key(shape_index)
        print(f"Seçilen şekil için anahtar: {key}")

    except ValueError:
        print("Geçersiz bir değer girdiniz, lütfen bir tam sayı girin.")


if _name_ == "_main_":
    main()
