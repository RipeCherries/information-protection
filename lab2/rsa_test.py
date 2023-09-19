
from mycrypto import *

p = generate_prime(1 << 8, 10 ** 9)
q = generate_prime(1 << 8, 10 ** 9)

n = p * q
phi = (p - 1) * (q - 1)

m = random.randrange(1, n) # сообщение

d, c = generate_c_d(phi)

e = modular_exponentiation(m, d, n)

m_res = modular_exponentiation(e, c, n)

print(m, m_res)
