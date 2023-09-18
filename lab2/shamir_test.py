from mycrypto import *

p = generate_prime(1, 10 ** 9)
m = random.randint(1, p)

ca, da = generate_c_d(p - 1)
cb, db = generate_c_d(p - 1)

x1 = modular_exponentiation(m, ca, p)
x2 = modular_exponentiation(x1, cb, p)
x3 = modular_exponentiation(x2, da, p)
x4 = modular_exponentiation(x3, db, p)

print(m, x4)
