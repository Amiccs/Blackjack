from random import shuffle
from playing_card import PlayingCard


class CardDeck(object):
    def __init__(self):
        # Створення колоди
        self.card_deck = []
        for suit in range(0, 4):
            for rank in range(1, 14):
                instance = PlayingCard(rank, suit)
                self.card_deck.append(instance)
        self.shuffle()

    def shuffle(self):
        # Перемішування колоди
        shuffle(self.card_deck)

    def pop(self):
        # Видалення останньої картки
        return self.card_deck.pop()
