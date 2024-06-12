import random

def generate_map(min_value, max_value, size):
    return [[random.randint(min_value, max_value) for _ in range(size)] for _ in range(size)]

def xor_encrypt(numbers, key):
    return [number ^ key for number in numbers]

def produce_key(map, start_x, start_y, path_choice):
    size = len(map)
    x, y = start_x, start_y
    key = 0

    for _ in range(size * size):  # En az bir kez tüm haritayı dolaşabilsin
        key ^= map[x][y]
        if path_choice == 1:  # Yatay sağa
            y = (y + 1) % size
        elif path_choice == 2:  # Dikey aşağı
            x = (x + 1) % size
        elif path_choice == 3:  # Çapraz sağ aşağı
            x = (x + 1) % size
            y = (y + 1) % size

    return key

def main():
    print("Min değerini girin")
    min_value = int(input())
    print("Max değerini girin")
    max_value = int(input())
    print("Boyut değerini girin")
    size = int(input())

    map = generate_map(min_value, max_value, size)

    start_x = random.randint(0, size - 1)
    start_y = random.randint(0, size - 1)
    path_choice = random.randint(1, 3)
    key = produce_key(map, start_x, start_y, path_choice)
    print(f"Generated key: {key}")

    s1 = int(input('Birinci sayıyı giriniz:'))  # Kullanıcıdan birinci sayıyı istedik.
    s2 = int(input('İkinci sayıyı giriniz:'))  # Kullanıcıdan ikinci sayıyı istedik.

    user_numbers = [random.randint(min_value, max_value) for _ in range(s1, s2)]
    print(f"User numbers: {user_numbers}")

    encrypted_numbers = xor_encrypt(user_numbers, key)
    print(f"Encrypted numbers: {encrypted_numbers}")

if __name__ == "__main__":
    main()
