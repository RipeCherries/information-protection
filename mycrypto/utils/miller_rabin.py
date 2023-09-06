import random
from .is_composite import is_composite


def miller_rabin(n: int, k: int = 20) -> bool:
    """
    Функция, проверяющая является ли число n вероятным простым числом с использованием алгоритма Миллера-Рабина.

    :param n: Число для проверки на простоту.
    :param k: Количество раундов.
    :return: True, если число вероятно простое; False, если число составное.
    """

    if n <= 1:
        return False

    if n <= 3:
        return True

    s = 0
    t = n - 1

    while t % 2 == 0:
        s += 1
        t //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        if is_composite(a, t, n, s):
            return False

    return True
