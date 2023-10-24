from datetime import datetime
import tkinter as tk
from math import cos, sin, pi
import random
from mycrypto import *

player_names = ["Мастер Трюков", "Граф Шуток", "Чародей Столов", "Шут Бульвара", "Барон Карт",
                "Король Партий", "Дама Веселья", "Карточный Шериф", "Покерная Вдова", "Джентльмен Фарта",
                "Мистер Магический", "Загадочный Крупье", "Баронесса Блефа", "Магия Азарта", "Королева Фейков",
                "Ловкач-Любитель", "Волшебник Козырей", "Тайный Дилер", "Леди Асов", "Виртуоз Ведения",
                "Маэстро Карточек", "Чародей Тузов", "Маг Треф"]

class PokerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №4 | Ментальный покер")

        self.player_count_frame = None
        self.game_frame = None
        self.n_players = None

        self.setup_player_count_frame()

    def setup_player_count_frame(self):
        self.player_count_frame = tk.Frame(self.root)
        self.player_count_frame.pack()
        self.player_count_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.player_count_label = tk.Label(self.player_count_frame, text="Введите количество игроков (2-23):")
        self.player_count_label.pack()

        self.player_count_entry = tk.Entry(self.player_count_frame)
        self.player_count_entry.pack()

        self.player_count_button = tk.Button(self.player_count_frame, text="Начать игру", command=self.start_game)
        self.player_count_button.pack()

        self.error_label = tk.Label(self.player_count_frame, text="", fg="red")
        self.error_label.pack()

    def start_game(self):
        n_players = int(self.player_count_entry.get())
        if not 1 < n_players < 24:
            self.error_label.config(text="Количество игроков должно быть\n больше 1 и меньше 24.")
        else:
            self.n_players = n_players
            self.setup_game_frame()

    def setup_game_frame(self):
        self.game_frame = tk.Toplevel(self.root)
        self.game_frame.title("Карточный стол")
        self.game_frame.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        canvas_width = self.root.winfo_screenwidth()
        canvas_height = self.root.winfo_screenheight()
        canvas = tk.Canvas(self.game_frame, width=canvas_width, height=canvas_height, bg="green")
        canvas.pack()

        radius = min(canvas_width, canvas_height) / 3

        center_x, center_y = canvas_width / 2, canvas_height / 2 - 50

        self.player_image = tk.PhotoImage(file="./assets/player.png")

        self.card_images = [tk.PhotoImage(file=f"./assets/card{i}.png") for i in range(1, 53)]
        self.card_flip = tk.PhotoImage(file="./assets/card_flip.png")

        self.player_labels = []
        self.card_labels = []
        for i in range(self.n_players):
            angle = 2 * pi * i / self.n_players
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            player_label = tk.Label(self.game_frame, image=self.player_image)
            player_label.place(x=x, y=y - 20)
            self.player_labels.append(player_label)
            name_label = tk.Label(self.game_frame, text=player_names[i], font=("Helvetica", 8))
            name_label.place(x=x-20, y=y - 35)

            card_label1 = tk.Label(self.game_frame, bg="green")
            card_label1.place(x=x - 25, y=y + 35)
            card_label2 = tk.Label(self.game_frame, bg="green")
            card_label2.place(x=x + 25, y=y + 35)
            self.card_labels.append([card_label1, card_label2])

        self.deck_count = 52

        self.deck_image = tk.PhotoImage(file="./assets/deck.png")
        self.deck_label = tk.Label(self.game_frame, image=self.deck_image)
        self.deck_label.place(x=20, y=20)
        self.deck_count_label = tk.Label(self.game_frame, text=str(self.deck_count) + " в колоде", font=("Helvetica", 12))
        self.deck_count_label.place(x=20, y=150)

        self.actions_functions = [
            self.shuffle_deck,
            self.assign_card_values,
            self.generate_p,
            self.generate_c_d_keys_players,
            self.encryption_and_mixing,
            self.give_hands,
            self.give_cards_to_table,
            self.decoding_cards_on_table,
            self.decoding_other_players_cards,
            self.decoding_your_own_cards
        ]

        self.action_index = 0
        self.actions = [
            "Перемешана колода карт",
            "Каждой карте сопоставлено своё числовое значение",
            "Сгенерировано число Р",
            "Сгенерированы ключи C и D каждого игрока",
            "Каждым игроком зашифрована колода и перемешана",
            "Каждому игроку роздано по 2 карты",
            "На стол выложено 5 карт",
            "Каждый игрок расшифровал карты на столе",
            "Каждый игрок расшифровал карты других",
            "Каждый игрок расшифровал свои карты"
        ]

        self.next_button = tk.Button(self.game_frame, text="Начать", command=self.game)
        self.next_button.place(x=1300, y=50)

    def shuffle_deck(self):
        self.shuffle_card_images()
        self.log_action(self.actions[self.action_index])

    def assign_card_values(self):
        self.cards_keys = list(range(2, 54))
        self.log_action(self.actions[self.action_index] + f" \n{self.cards_keys}")

    def generate_p(self):
        self.p = generate_sophie_germain(10 ** 8, 10 ** 10)
        self.log_action(self.actions[self.action_index] + f" {self.p}")

    def generate_c_d_keys_players(self):
        self.c_keys_players = []
        self.d_keys_players = []
        for _ in range(self.n_players):
            c, d = generate_c_d(self.p - 1)
            self.c_keys_players.append(c)
            self.d_keys_players.append(d)
        self.log_action(self.actions[self.action_index] + f" \nc_keys={self.c_keys_players}\nd_keys={self.d_keys_players}")

    def encryption_and_mixing(self):
        for i in range(self.n_players):
            self.cards_keys = [modular_exponentiation(key, self.c_keys_players[i], self.p) for key in self.cards_keys]
            random.shuffle(self.cards_keys)
        self.log_action(self.actions[self.action_index] + f" \n{self.cards_keys}")

    def give_hands(self):
        self.hands = list()
        for i in range(self.n_players):
            self.hands.append([])
            for j in range(2):
                card = self.cards_keys[j]
                self.cards_keys.remove(card)
                self.hands[i].append(card)
                self.card_labels[i][j].config(image=self.card_flip)

        self.deck_count -= 2 * self.n_players
        self.deck_count_label.config(text=str(self.deck_count) + " в колоде")

        self.log_action(self.actions[self.action_index] + f" \n{self.hands}")

    def give_cards_to_table(self):
        self.table_keys = self.cards_keys[-5:]

        self.deck_count -= 5
        self.deck_count_label.config(text=str(self.deck_count) + " в колоде")

        self.table_cards_labels = []
        table_x = self.root.winfo_screenwidth() / 2
        table_y = self.root.winfo_screenheight() / 2 - 50

        for i in range(len(self.table_keys)):
            x = table_x - 100 + i * 60
            y = table_y - 50
            card_label = tk.Label(self.game_frame, image=self.card_flip)
            card_label.place(x=x, y=y)
            self.table_cards_labels.append(card_label)

        self.log_action(self.actions[self.action_index] + f" \n{self.table_keys}")

    def decoding_cards_on_table(self):
        for key in self.d_keys_players:
            self.table_keys = [modular_exponentiation(table_key, key, self.p) for table_key in self.table_keys]

        for i, card_key in enumerate(self.table_keys):
            self.table_cards_labels[i].config(image=self.card_images[card_key - 2])

        self.log_action(self.actions[self.action_index] + f" \n{self.table_keys}")

    def decoding_other_players_cards(self):
        for i in range(len(self.hands)):
            for j in range(len(self.d_keys_players)):
                if i != j:
                    self.hands[i] = [modular_exponentiation(item, self.d_keys_players[j], self.p) for item in self.hands[i]]

        self.log_action(self.actions[self.action_index] + f" \n{self.hands}")

    def decoding_your_own_cards(self):
        for i in range(len(self.hands)):
            self.hands[i] = [modular_exponentiation(item, self.d_keys_players[i], self.p) for item in self.hands[i]]

        print(self.hands)

        for i in range(len(self.hands)):
            for j, card_key in enumerate(self.hands[i]):
                self.card_labels[i][j].config(image=self.card_images[card_key - 2])

        self.log_action(self.actions[self.action_index] + f" \n{self.hands}")

    def game(self):
        if self.action_index == 0:
            self.next_button.config(text="Далее", command=self.next_action)
            self.action_label = tk.Label(self.game_frame, text=self.actions[0], font=("Helvetica", 12), wraplength=150)
            self.action_label.place(x=1300, y=100)

        if self.action_index < len(self.actions_functions):
            self.actions_functions[self.action_index]()
            self.action_index += 1


    def shuffle_card_images(self):
        random.shuffle(self.card_images)
        deck_image = tk.PhotoImage(file="./assets/deck_shuffled.png")
        self.deck_label.config(image=deck_image)
        self.deck_label.image = deck_image

    def log_action(self, action):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{current_time} - {action}\n\n")
        log_file.close()

    def next_action(self):
        if self.action_index < len(self.actions):
            self.action_label.config(text=self.actions[self.action_index])
        else:
            self.next_button.config(state=tk.DISABLED)

        self.game()


if __name__ == "__main__":
    root = tk.Tk()
    poker_game = PokerGame(root)
    root.mainloop()