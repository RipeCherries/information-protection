import sys

from mycrypto import *


def encrypt_data(data, base, power, mod):
    return [byte * modular_exponentiation(base, power, mod) % mod for byte in data]


def write_bytes_to_file(data, file_name):
    file = open(file_name, "wb")

    for byte in data:
        file.write(byte.to_bytes(1, sys.byteorder))


p = generate_sophie_germain(1 << 8, 10 ** 9)
g = generate_primitive_root(p)

# приватный ключ
cb = random.randrange(1, p)

# открытый ключ
db = modular_exponentiation(g, cb, p)

k = random.randrange(1, p - 2)
r = modular_exponentiation(g, k, p)

print(f'p = {p}\ng = {g}\ncb = {cb}\tdb = {db}')

orig_data = open('data/image.jpg', 'rb').read()

# шифрование
encrypted = encrypt_data(orig_data, db, k, p)


open('data/image_encrypted.jpg', 'w').write(str(encrypted))


# расшифровка
decrypted = encrypt_data(encrypted, r, p - 1 - cb, p)
write_bytes_to_file(decrypted, 'data/image_decrypted.jpg')
