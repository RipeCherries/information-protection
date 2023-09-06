from ..modular_exponentiation import modular_exponentiation


def is_composite(a: int, t: int, n: int, s: int) -> bool:
    """
    Функция, выполняющая проверку числа n на составность с использованием алгоритма проверки чисел на простоту по методу Миллера-Рабина.

    :param a: Целое число, случайно выбранное из интервала [2, n-2].
    :param t: Целое число, такое что n - 1 = 2^s * t, где s - неотрицательное целое число и t - нечётное целое число.
    :param n: Число, которое проверяется на простоту.
    :param s: Неотрицательное целое число, такое что n - 1 = 2^s * t.
    :return: True, если число n составное (не простое), и False, если число n вероятно простое.
    """
    
    x = modular_exponentiation(a, t, n)

    if x == 1 or x == n - 1:
        return False

    for _ in range(s - 1):
        x = modular_exponentiation(x, 2, n)

        if x == n - 1:
            return False

    return True
