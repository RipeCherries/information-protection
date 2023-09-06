from mycrypto import modular_exponentiation
from mycrypto import generalized_gcd
from mycrypto.generators import *
from mycrypto import *


def main():
    aa = generate_prime(1, 1000)
    bb = generate_prime(1, 9999999999)
    cc = generate_prime(1, 9999999999999)

    print(aa)
    print(bb)
    print(cc)

    # aa = 853
    # bb = 923103073932
    # cc = 1854894355943

    print()

    x = modular_exponentiation(aa, bb, cc)
    print(x)
    print(baby_step_giant_step(aa, x, cc))



    print('\n\n\n\n')



    print(generalized_gcd(21, 5))
    print(miller_rabin(11))


    p = generate_sophie_germain(1, 10000000, 50)
    root = generate_primitive_root(1, 10000000, p)




    pub_key_1, priv_key_1 = generate_keys(root, p)
    pub_key_2, priv_key_2 = generate_keys(root, p)


    print(pub_key_1)
    print(priv_key_1)
    print()
    print(pub_key_2)
    print(priv_key_2)
    print()
    print(get_shared_secret_key(priv_key_1, pub_key_2, p))
    print(get_shared_secret_key(priv_key_2, pub_key_1, p))


if __name__ == '__main__':
    main()
