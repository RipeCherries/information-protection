import sys

from mycrypto import *


def encrypt_data(data, power, mod):
    return [modular_exponentiation(byte, power, mod) for byte in data]


def write_bytes_to_file(data, file_name):
    file = open(file_name, "wb")

    for byte in data:
        file.write(byte.to_bytes(1, sys.byteorder))


p = generate_prime(1 << 8, 10 ** 9)
q = generate_prime(1 << 8, 10 ** 9)

n = p * q
phi = (p - 1) * (q - 1)

d, c = generate_c_d(phi)

print(f'p = {p}\nq = {q}\nn = {n}\tphi = {phi}\td = {d}\tc = {c}')

orig_data = open('data/image.jpg', 'rb').read()

# шифрование
encrypted = encrypt_data(orig_data, d, n)


open('data/image_encrypted.jpg', 'w').write(str(encrypted))


# расшифровка
decrypted = encrypt_data(encrypted, c, n)
write_bytes_to_file(decrypted, 'data/image_decrypted.jpg')
