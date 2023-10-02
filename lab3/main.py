from rsa_sign import rsa_sign
from elgamal_sign import elgamal_sign


def read_file(path):
    with open(path, "rb") as file:
        return file.read()


def main():
    message = read_file("data/sample_text.txt")

    rsa_sign(message)
    elgamal_sign(message)


if __name__ == "__main__":
    main()
