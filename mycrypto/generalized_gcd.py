def generalized_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Функция, реализующая обобщённый алгоритм Евклида.

    :param a: Первое целое число.
    :param b: Второе целое число.
    :return: Кортеж, содержащий НОД (gcd), коэффициент x и коэффициент y такие, что gcd(a, b) = ax + by.
    """

    if a <= 0:
        raise ValueError('Первое число не натуральное!')

    if b <= 0:
        raise ValueError('Второе число не натуральное!')

    if a < b:
        a, b = b, a

    u = a, 1, 0
    v = b, 0, 1

    while v[0] != 0:
        q = u[0] // v[0]
        t = u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2]
        u, v = v, t

    return u
