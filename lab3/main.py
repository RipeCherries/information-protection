from rsa_sign import rsa_sign
from elgamal_sign import elgamal_sign
from gost_sign import gost_sign


def read_file(path):
    with open(path, "rb") as file:
        return file.read()


def main():
    message = read_file("data/sample_text.txt")

    rsa_sign(message)
    print()
    elgamal_sign(message)
    print()
    gost_sign(message)


if __name__ == "__main__":
    main()
