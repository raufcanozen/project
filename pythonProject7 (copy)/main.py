


 def sbox(s):
    s[0] ^= s[4]; s[4] ^= s[3]; s[2] ^= s[1]; s[0] ^= s[2]; s[2] ^= s[4]; s[4] = ~s[4]
    s[1] ^= s[0]; s[0] ^= s[3]; s[3] ^= s[2]; s[2] ^= s[1]; s[1] ^= s[4]; s[4] ^= s[3]
    return s

def permutation(s, rounds):
    for i in range(12 - rounds, 12):
        s[2] ^= (0xf0 - i * 0x10 + i)
        s = sbox(s)
        s[0] ^= (s[4] & s[3]); s[4] ^= (s[3] & s[2]); s[3] ^= (s[2] & s[1])
        s[2] ^= (s[1] & s[0]); s[1] ^= (s[0] & s[4]); s[0] ^= s[4]
    return s

def int_to_bytes(x, length, byteorder='little'):
    x &= (1 << (length * 8)) - 1  # Belirtilen uzunluğa göre kes
    return x.to_bytes(length, byteorder)

def ascon128a_encrypt(key, nonce, associated_data, plaintext):
    K = [int.from_bytes(key[i: i +8], 'little') for i in range(0, 16, 8)]
    N = [int.from_bytes(nonce[i: i +8], 'little') for i in range(0, 16, 8)]
    S = [0x80400c0600000000, 0x0000000000000000, K[0], K[1], N[0]]
    S = permutation(S, 12)
    S[3] ^= K[0]
    S[4] ^= K[1]

    for i in range(0, len(associated_data), 8):
        S[0] ^= int.from_bytes(associated_data[i: i +8], 'little')
        S = permutation(S, 8)

    S[4] ^= 1  # Finalizasyon

    ciphertext = b""
    for i in range(0, len(plaintext), 8):
        P = int.from_bytes(plaintext[i: i +8], 'little')
        S[0] ^= P
        ciphertext += int_to_bytes(S[0], 8, 'little')
        S = permutation(S, 8)

    S[1] ^= K[0]
    S[2] ^= K[1]
    S = permutation(S, 12)
    S[3] ^= K[0]
    S[4] ^= K[1]

    tag = int_to_bytes(S[3], 8, 'little') + int_to_bytes(S[4], 8, 'little')

    return ciphertext, tag


key = b'\x01' * 16
nonce = b'\x02' * 16
associated_data = b'\x03' * 8
plaintext = b'\x04' * 8

ciphertext, tag = ascon128a_encrypt(key, nonce, associated_data, plaintext)

print("Şifreli Metin:", ciphertext)
print("Etiket:", tag)
