import math
import random

from . import generalized_gcd
from .utils.miller_rabin import miller_rabin
from .modular_exponentiation import modular_exponentiation


def generate_prime(l: int, r: int, k: int = 20) -> int:
    """
    Функция, генерирующая случайное простое число.

    :param l: Начальное значение интервала.
    :param r: Конечное значение интервала.
    :param k: Количество раундов.
    :return: Случайное простое число из интервала [l, r].
    """

    while True:
        candidate = random.randint(l, r)
        if miller_rabin(candidate, k):
            return candidate


def generate_sophie_germain(l: int, r: int, k: int = 20) -> int:
    """
    Функция, генерирующая случайное число p, которое является числом Софи Жермен.

    :param l: Начальное значение интервала.
    :param r: Конечное значение интервала.
    :param k: Количество раундов.
    :return: Случайное число Софи Жермен p, такое что p и 2*p + 1 оба являются простыми числами.
    """

    while True:
        candidate = generate_prime(l // 2, (r - 1) // 2, k)
        if miller_rabin(p := candidate * 2 + 1):
            return p


def generate_primitive_root(p: int) -> int:
    """
    Функция, генерирующая первообразный корень.

    :param p: число Софи Жермен.
    :return: Первообразный корень.
    """

    while True:
        candidate = random.randint(2, p)
        if modular_exponentiation(candidate, (p - 1) // 2, p) != 1:
            return candidate


def generate_mutually_prime(p: int):
    while True:
        candidate = random.randrange(2, p)
        if math.gcd(p, candidate) == 1:
            return candidate


def generate_c_d(p: int):
    c = generate_mutually_prime(p)
    gcd, _, d = generalized_gcd(c, p)

    while d < 0:
        d += p

    return c, d
