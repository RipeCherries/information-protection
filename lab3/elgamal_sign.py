import sys
from mycrypto import *
from hashlib import md5


def elgamal_sign(message):
    h = md5(message)
    h_int = int.from_bytes(h.digest(), byteorder=sys.byteorder)

    p = generate_sophie_germain(1 << h.digest_size * 8 + 1, 1 << h.digest_size * 8 + 2)
    g = generate_primitive_root(p)

    x = random.randrange(2, p - 1)  # Закрытый ключ
    y = modular_exponentiation(g, x, p)  # Открытый ключ

    k = generate_mutually_prime(p - 1)
    r = modular_exponentiation(g, k, p)

    u = (h_int - x * r) % (p - 1)
    gcd, kk, _ = generalized_gcd(k, p - 1)

    sign = (kk * u) % (p - 1)

    with open("data/elgamal_sign.txt", 'w') as file:
        file.write(str(sign))

    yr = (modular_exponentiation(y, r, p) * modular_exponentiation(r, sign, p)) % p
    gh = modular_exponentiation(g, h_int, p)

    is_real = yr == gh

    print("=== Электронная подпись Эль-Гамаля ===")
    print(f"p = {p}")
    print(f"g = {g}")
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"k = {k}")
    print(f"r = {r}")
    print(f"h = {h_int}")
    print(f"sign = {sign}")
    print(f"yr = {yr}")
    print(f"gh = {gh}")
    print(f"yr = gh = {is_real}")
