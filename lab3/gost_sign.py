import sys
from mycrypto import *
from hashlib import md5


def gost_sign(message):
    q = generate_prime(1 << 255, (1 << 256) - 1)

    # Генерация p
    while True:
        b = random.randint(math.ceil((1 << 1023) / q), ((1 << 1024) - 1) // q)
        if miller_rabin(p := b * q + 1):
            break

    # Генерация а
    while True:
        g = random.randrange(2, p - 1)
        if (a := modular_exponentiation(g, b, p)) > 1:
            break

    x = random.randrange(1, q)  # Закрытый ключ
    y = modular_exponentiation(a, x, p)  # Открытый ключ

    h = md5(message)
    h_int = int.from_bytes(h.digest(), byteorder=sys.byteorder)

    while True:
        k = random.randrange(1, q)

        if (r := modular_exponentiation(a, k, p) % q) == 0:
            continue

        if (sign := (k * h_int % q + x * r % q) % q) != 0:
            break

    with open("data/gost_sign.txt", 'w') as file:
        file.write(str(sign))

    gcd, _, hh = generalized_gcd(h_int, q)
    u1 = sign * hh % q
    u2 = -r * hh % q
    v = modular_exponentiation(a, u1, p) * modular_exponentiation(y, u2, p) % p % q

    is_real = v == r

    print("=== Электронная подпись ГОСТ ===")
    print(f"q = {q}")
    print(f"p = {p}")
    print(f"a = {a}")
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"h = {h_int}")
    print(f"k = {k}")
    print(f"sign = {sign}")
    print(f"v = {v}")
    print(f"r = {r}")
    print(f"v = r = {is_real}")
