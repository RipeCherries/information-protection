from .modular_exponentiation import modular_exponentiation


def baby_step_giant_step(base, target, prime):
    """
    Функция, реализующая алгоритм "Baby Step Giant Step" для вычисления дискретного логарифма по модулю.

    :param base: Основание степени.
    :param target: Целевое значение, которое необходимо получить в результате вычислений.
    :param prime: Модуль, по которому выполняются вычисления.
    :return: Значение x, удовлетворяющее условию base^x ≡ target (mod prime), если такое значение существует, иначе -1.
    """

    sqrt_prime = int(prime ** 0.5)

    baby_step_table = {}
    baby_step = 1
    for j in range(sqrt_prime + 1):
        baby_step_table[baby_step] = j
        baby_step = (baby_step * base) % prime

    giant_step_multiplier = modular_exponentiation(base, sqrt_prime * (prime - 2), prime)

    giant_step = target
    for i in range(sqrt_prime + 1):
        if giant_step in baby_step_table:
            return i * sqrt_prime + baby_step_table[giant_step]
        giant_step = (giant_step * giant_step_multiplier) % prime

    return -1
