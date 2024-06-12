import struct

def shift(n, b, shift_type):
    if shift_type == 'sola':
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF
    elif shift_type == 'saga':
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF
    elif shift_type == 'dairesel sola':
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF
    elif shift_type == 'dairesel saga':
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF
    else:
        raise ValueError('Geçersiz kaydırma türü: {}'.format(shift_type))

def sha1(data):
    # Constants
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing
    original_byte_len = len(data)
    original_bit_len = original_byte_len * 8

    # Append the bit '1' to the message
    data += b'\x80'

    # Append k bits, where k is the minimum number >= 0 such that the resulting message length (in bits)
    # is congruent to 448 (mod 512)
    data += b'\x00' * ((56 - len(data) % 64) % 64)

    # Append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    data += struct.pack('>Q', original_bit_len)

    # Process the message in successive 512-bit chunks
    for i in range(0, len(data), 64):
        w = [0] * 80
        for j in range(16):
            w[j] = struct.unpack('>I', data[i + j*4:i + j*4 + 4])[0]

        for j in range(16, 80):
            w[j] = shift(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1, 'dairesel sola')

        a, b, c, d, e = h0, h1, h2, h3, h4

        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (shift(a, 5, 'dairesel sola') + f + e + k + w[j]) & 0xFFFFFFFF
            e = d
            d = c
            c = shift(b, 30, 'dairesel saga')
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def sha1_modified(data, shift_type_a, shift_type_b):
    # Constants
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing
    original_byte_len = len(data)
    original_bit_len = original_byte_len * 8

    # Append the bit '1' to the message
    data += b'\x80'

    # Append k bits, where k is the minimum number >= 0 such that the resulting message length (in bits)
    # is congruent to 448 (mod 512)
    data += b'\x00' * ((56 - len(data) % 64) % 64)

    # Append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    data += struct.pack('>Q', original_bit_len)

    # Process the message in successive 512-bit chunks
    for i in range(0, len(data), 64):
        w = [0] * 80
        for j in range(16):
            w[j] = struct.unpack('>I', data[i + j*4:i + j*4 + 4])[0]

        for j in range(16, 80):
            w[j] = shift(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1, shift_type_a)

        a, b, c, d, e = h0, h1, h2, h3, h4

        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (shift(a, 5, shift_type_a) ^ f ^ e ^ k ^ w[j]) & 0xFFFFFFFF
            e = d
            d = c
            c = shift(b, 30, shift_type_b)
            b = a
            a = temp

        h0 = (h0 ^ a) & 0xFFFFFFFF
        h1 = (h1 ^ b) & 0xFFFFFFFF
        h2 = (h2 ^ c) & 0xFFFFFFFF
        h3 = (h3 ^ d) & 0xFFFFFFFF
        h4 = (h4 ^ e) & 0xFFFFFFFF

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def compare(data):
    original_hash = sha1(data)
    modified_hash = sha1_modified(data, 'dairesel sola', 'dairesel saga')

    original_bits = ''.join(format(byte, '08b') for byte in bytes.fromhex(original_hash))
    modified_bits = ''.join(format(byte, '08b') for byte in bytes.fromhex(modified_hash))

    stage_differences = []

    for i in range(0, 160, 32):
        orig_stage = original_bits[i:i+32]
        mod_stage = modified_bits[i:i+32]
        bit_diff = sum(1 for ob, mb in zip(orig_stage, mod_stage) if ob != mb)
        stage_differences.append((orig_stage, mod_stage, bit_diff))

    total_diff = sum(diff[2] for diff in stage_differences)

    return {
        'original_hash': original_hash,
        'modified_hash': modified_hash,
        'stage_differences': stage_differences,
        'total_diff': total_diff
    }

# Test the comparison function with a sample message
data = b'Test message for SHA-1 comparison'
result = compare(data)

# Print the comparison results
print('Original Hash:', result['original_hash'])
print('Modified Hash:', result['modified_hash'])
print('Total Bit Differences:', result['total_diff'])
for i, (orig_stage, mod_stage, bit_diff) in enumerate(result['stage_differences']):
    print(f'Stage {i + 1} Bit Differences: {bit_diff}')
    print('Original Stage:', orig_stage)
    print('Modified Stage:', mod_stage)
