import random
import sys


def write_bytes_to_file(data, file_name):
    file = open(file_name, "wb")

    for byte in data:
        file.write(byte.to_bytes(1, sys.byteorder))


orig_data = open('data/image.jpg', 'rb').read()

keys = [random.randrange(1 << 8) for _ in range(len(orig_data))]

# шифрование
encrypted = [x ^ y for x, y in zip(orig_data, keys)]

open('data/image_encrypted.jpg', 'w').write(str(encrypted))

# дешифрование
decrypted = [x ^ y for x, y in zip(encrypted, keys)]

write_bytes_to_file(decrypted, 'data/image_decrypted.jpg')
