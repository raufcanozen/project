def sha1(data):
    bytes = ""

    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for n in range(len(data)):
        bytes += '{0:08b}'.format(ord(data[n]))
    bits = bytes + "1"
    pBits = bits
    # pad until length equals 448 mod 512
    while len(pBits) % 512 != 448:
        pBits += "0"
    # append the original length
    pBits += '{0:064b}'.format(len(bits) - 1)

    def chunks(l, n):
        return [l[i:i + n] for i in range(0, len(l), n)]

    def rol(n, b, i):
        if i == 1:
            return ((n << b) | (n >> (32 - b))) & 0xffffffff  # Dairesel sol
        elif i == 2:
            return (n << b) & 0xffffffff  # Normal sol
        elif i == 3:
            return ((n >> b) | (n << (32 - b))) & 0xffffffff  # Dairesel sağ
        elif i == 4:
            return (n >> b) & 0xffffffff  # Normal sağ

    for c in chunks(pBits, 512):
        words = chunks(c, 32)
        w = [0] * 80
        for n in range(0, 16):
            w[n] = int(words[n], 2)
        for i in range(16, 80):
            w[i] = rol((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1, 1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # Main loop
        for i in range(0, 80):

            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (((rol(a, 10, 4) ^ (f ^ e)) ^ w[i]) ^ k) & 0xffffffff
            e = d
            d = c
            c = rol(b, 20, 4)
            b = a
            a = temp

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def sha1_compare(data1, data2):
    """
    İki SHA-1 fonksiyonunun çıktılarını karşılaştırır.

    Args:
    data1 (str): Karşılaştırılacak ilk veri.
    data2 (str): Karşılaştırılacak ikinci veri.

    Returns:
    bool: İki SHA-1 çıktısının eşit olup olmadığını döndürür.
    """
    sha1_result1 = sha1(data1)
    sha1_result2 = sha1(data2)

    print(f"Data 1 SHA-1: {sha1_result1}")
    print(f"Data 2 SHA-1: {sha1_result2}")

    return sha1_result1 == sha1_result2


data1 = "MESAJ"
data2 = "abc"

result = sha1_compare(data1, data2)
print("SHA-1 çıktıları eşleşiyor mu?", result)
