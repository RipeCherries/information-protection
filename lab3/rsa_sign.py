import sys
from mycrypto import *
from hashlib import md5


def rsa_sign(message):
    h = md5(message)
    h_int = int.from_bytes(h.digest(), byteorder=sys.byteorder)

    p = generate_prime(1 << h.digest_size * 8 // 2 + 1, 1 << h.digest_size * 8 // 2 + 2)
    q = generate_prime(1 << h.digest_size * 8 // 2 + 1, 1 << h.digest_size * 8 // 2 + 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    # c - закрытый, d - открытый
    c, d = generate_c_d(phi)
    if c < 0:
        c += phi

    sign = modular_exponentiation(h_int, c, n)

    with open("data/rsa_sign.txt", 'w') as file:
        file.write(str(sign))

    e = modular_exponentiation(sign, d, n)

    is_real = e == h_int

    print("=== Электронная подпись RSA ===")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}")
    print(f"phi = {phi}")
    print(f"d = {d}")
    print(f"c = {c}")
    print(f"h = {h_int}")
    print(f"sign = {sign}")
    print(f"e = {e}")
    print(f"e = h = {is_real}")