import random
from .modular_exponentiation import modular_exponentiation


def generate_keys(g: int, p: int) -> tuple[int, int]:
    """
    Функция, генерирующая ключи для алгоритма Диффи-Хеллмана.

    :param g: Первообразный корень.
    :param p: Число Софи Жермен.
    :return: Пара ключей - открытый и закрытый ключи, представленные в виде кортежа.
    """

    private_key = random.randint(1, p)
    public_key = modular_exponentiation(g, private_key, p)

    return public_key, private_key


def get_shared_secret_key(private_key: int, public_key: int, p: int) -> int:
    """
    Функция, вычисляющая общий секретный ключ.

    :param private_key: Закрытый ключ одной из сторон обмена данными.
    :param public_key: Открытый ключ другой стороны обмена данными.
    :param p: Число Софи Жермен.
    :return: Общий секретный ключ, который может быть использован обеими сторонами для шифрования и расшифрования сообщений.
    """

    return modular_exponentiation(public_key, private_key, p)
