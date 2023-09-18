import sys
from mycrypto import *


def encrypt_data(data, power, mod):
    return [modular_exponentiation(byte, power, mod) for byte in data]


def write_bytes_to_file(data, file_name):
    file = open(file_name, "wb")

    for byte in data:
        file.write(byte.to_bytes(1, sys.byteorder))


p = generate_prime(1 << 8, 10 ** 9)

ca, da = generate_c_d(p - 1)
cb, db = generate_c_d(p - 1)

print(f'p = {p}\nca = {ca}\tda = {da}\ncb = {cb}\tdb = {db}')

orig_data = open('data/image.jpg', 'rb').read()

# шифрование Алиса
alice_encrypted = encrypt_data(orig_data, ca, p)

# шифрование Боб
alice_and_bob_encrypted = encrypt_data(alice_encrypted, cb, p)


open('data/image_encrypted.jpg', 'w').write(str(alice_and_bob_encrypted))


# расшифровка Алиса
alice_encrypted = encrypt_data(alice_and_bob_encrypted, da, p)

# расшифровка Боб
decrypted = encrypt_data(alice_encrypted, db, p)

write_bytes_to_file(decrypted, 'data/image_decrypted.jpg')
