import random

from mycrypto import *

p = generate_sophie_germain(1, 10 ** 9)
g = generate_primitive_root(p)
m = random.randrange(1, p)

cb = random.randrange(1, p)
db = modular_exponentiation(g, cb, p)

k = random.randrange(1, p - 2)
r = modular_exponentiation(g, k, p)
e = m * modular_exponentiation(db, k, p) % p

m_res = e * modular_exponentiation(r, p - 1 - cb, p) % p

print(m, m_res)
