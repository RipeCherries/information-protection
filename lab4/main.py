import random
from mycrypto import *


def generate_cards():
    suits = ["♣", "♠", "♥", "♦"]
    nominals = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    cards = []
    for nominal in nominals:
        for suit in suits:
            cards.append(nominal + suit)

    return cards


def main():
    # ввод количества игроков
    while True:
        n_players = int(input("\n-> Введите количество игроков: "))
        if not 0 < n_players < 24:
            print("<- Количество игроков должно быть в диапазоне [1; 23].")
        else:
            break

    # генерация карт на доске
    cards = generate_cards()
    random.shuffle(cards)
    cards = {i: cards[i - 2] for i in range(2, 54)}
    cards_keys = list(cards.keys())

    # генерация Р
    p = generate_sophie_germain(10**8, 10**10)

    # генерация ключей С и D игроков
    c_keys_players = []
    d_keys_players = []
    for _ in range(n_players):
        c, d = generate_c_d(p - 1)
        c_keys_players.append(c)
        d_keys_players.append(d)

    # шифрование колоды каждым игроком и перемешивание
    for i in range(n_players):
        cards_keys = [modular_exponentiation(key, c_keys_players[i], p) for key in cards_keys]
        random.shuffle(cards_keys)

    # раздача карт игрокам
    hands = list()
    for i in range(n_players):
        hands.append([])
        for j in range(2):
            card = cards_keys[j]
            cards_keys.remove(card)
            hands[i].append(card)
    print(hands)

    table_keys = cards_keys[-5:]
    print(table_keys)

    # расшифровка карт на столе
    for key in d_keys_players:
        table_keys = [modular_exponentiation(table_key, key, p) for table_key in table_keys]

    # расшифровка карт игроков
    for i in range(len(hands)):
        for j in range(len(d_keys_players)):
            if i != j:
                hands[i] = [modular_exponentiation(item, d_keys_players[j], p) for item in hands[i]]
        hands[i] = [modular_exponentiation(item, d_keys_players[i], p) for item in hands[i]]

    print(*hands)






if __name__ == "__main__":
    main()
