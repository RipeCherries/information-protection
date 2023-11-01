import math
import sys
from enum import Enum
from mycrypto import *
from hashlib import sha3_512


class Vote(Enum):
    YES = 1
    NO = 2
    ABSTAIN = 3


class Server:
    def __init__(self):
        # генерация p, q
        p, q = generate_prime(1 << 1023, (1 << 1024) - 1), generate_prime(1 << 1023, (1 << 1024) - 1)
        while p == q:
            q = generate_prime(1 << 1023, (1 << 1024) - 1)

        # вычисление n - общий параметр
        self.n = p * q

        # вычисление phi
        phi = (p - 1) * (q - 1)

        # генерация ключей: с - закрытый, d - открытый
        self._c, self.d = generate_c_d(phi)

        # список имён проголосовавших
        self._those_who_voted = set()

        # бюллетени
        self._blanks = set()

        print(f"СЕРВЕР ЗАПУЩЕН. Параметры:")
        print(f"p = {p}\nq = {q}\nn = {self.n}\nphi = {phi}\nc = {self._c}\nd = {self.d}")

    def get_blank(self, name: str, hh: int):
        print(f"-> СЕРВЕР: {name} запросил(а) бюллетень")
        if name in self._those_who_voted:
            print(f"-> СЕРВЕР: {name} отказано в выдаче бюллетени по причине повторного голосования")
            return None
        else:
            print(f"-> СЕРВЕР: выдал бюллетень {name}")
            self._those_who_voted.add(name)
            return modular_exponentiation(hh, self._c, self.n)

    def set_blank(self, n: int, sign: int) -> bool:
        print(f"-> СЕРВЕР: получен бюллетень")

        # проверка корректности бюллетеня
        hash_value = sha3_512(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder=sys.byteorder))
        hash10 = int(hash_value.hexdigest(), base=16)
        if hash10 == modular_exponentiation(sign, self.d, self.n):
            print(f"-> СЕРВЕР: полученный бюллетень принят")
            print(f"hash = {hash10}\ns^d%n = {modular_exponentiation(sign, self.d, self.n)}")
            self._blanks.add((n, sign))
            return True
        else:
            print(f"-> СЕРВЕР: полученный бюллетень отклонён")
            print(f"hash = {hash10}\ns^d%n = {modular_exponentiation(sign, self.d, self.n)}")
            return False


class Client:
    def __init__(self, server: Server, name: str) -> None:
        self.server = server
        self.name = name

    def vote(self, vote: Vote) -> None:
        # генерация числа, хранящего информацию о голосе
        rnd = generate_prime(1 << 511, (1 << 512) - 1)

        # добавление служебной информации
        n = rnd | vote.value

        # генерация r, взаимного простого с n
        r = generate_mutually_prime(self.server.n)

        # вычисление хэша от n
        hash_value = sha3_512(n.to_bytes(math.ceil(n.bit_length() / 8), byteorder=sys.byteorder))
        hash10 = int(hash_value.hexdigest(), base=16)
        hh = hash10 * modular_exponentiation(r, self.server.d, self.server.n)

        # отправка запроса на получение бюллетени
        ss = self.server.get_blank(self.name, hh)

        if ss:
            # вычисление r^(-1)
            _, _, r1 = generalized_gcd(r, self.server.n)
            # вычисление подписи бюллетеня
            sign = (ss * r1) % self.server.n

            # отправка подписанного бюллетеня
            if self.server.set_blank(n, sign):
                print(f"$ КЛИЕНТ: бюллетень принят")
            else:
                print(f"$ КЛИЕНТ: бюллетень не прошёл проверку был отклонён")
        else:
            print(f"$ КЛИЕНТ: {self.name} уже голосовал(а)")


def main():
    server = Server()
    print()

    client1 = Client(server, "Alice")
    client1.vote(Vote.ABSTAIN)


if __name__ == "__main__":
    main()
