def modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """
    Функция быстрого возведения числа в степень по модулю.

    :param base: Основание.
    :param exponent: Показатель степени.
    :param modulus: Модуль.
    :return: Остаток от деления (base ** exponent) % modulus.
    """

    if modulus == 0:
        raise ValueError("Модуль не может быть равен 0!")

    if exponent < 0:
        raise ValueError("Показатель степени не может быть отрицательным!")

    if modulus == 1:
        return 0

    result = 1
    base %= modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus

        exponent = exponent >> 1
        base = (base * base) % modulus

    return result
