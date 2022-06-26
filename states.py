import pygame
from common import *
from globals import *
from card_deck import CardDeck
from player import Player
from button_area import ButtonArea
from sound_db import SoundDB


class State(object):
    def next_state(self, state):
        self.__class__ = state


class InitialState(State):
    # Скидання всіх змінних
    def __call__(self, commons, button_status):
        commons.player_turn = 0
        commons.game_rounds += 1
        commons.dealer_cards = []
        commons.display_status = False
        commons.first_card_hidden = True
        button_status.reset()
        if commons.game_rounds == 1:
            self.next_state(AddPlayersState)
        else:
            for player in commons.player_list:
                player.hand = []
                player.status = {'blackjack': False, 'win': False, 'push': False, 'loose': False, 'busted': False}
            self.next_state(PlayState)


class AddPlayersState(State):
    players_count = 1
    player_list = [Player(1, [], {'blackjack': False, 'win': False, 'push': False, 'loose': False, 'busted': False})]

    def __call__(self, commons, button_status):
        show_buttons(commons.screen, button_status)
        button_status.add_player = True
        button_status.play = True
        button_areas = ButtonArea.get_instance(commons)
        commons.player_list = self.player_list
        if self.players_count >= 4:
            button_status.add_player = False
            self.next_state(PlayState)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(commons, button_status)
                commons.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()  # повертає (x, y)
                if button_areas.add_player_area.collidepoint(mouse_pos[0], mouse_pos[1]) and self.players_count < 5:
                    self.players_count += 1
                    player = Player(self.players_count, [], {'blackjack': False,
                                                             'win': False,
                                                             'push': False,
                                                             'loose': False,
                                                             'busted': False})
                    self.player_list.append(player)
                if button_areas.play_area.collidepoint(mouse_pos[0], mouse_pos[1]):
                    commons.player_hit = False
                    button_status.play = False
                    button_status.add_player = False
                    self.next_state(DealingState)


class PlayState(State):

    def __call__(self, commons, button_status):
        show_buttons(commons.screen, button_status)
        button_status.play = True
        button_areas = ButtonArea.get_instance(commons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(commons, button_status)
                commons.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()  # повертає (x, y)
                if button_areas.play_area.collidepoint(mouse_pos[0], mouse_pos[1]):
                    commons.dealer_cards = []
                    commons.first_card_hidden = True
                    commons.player_hit = False
                    button_status.play = False
                    self.next_state(DealingState)


class DealingState(State):
    """
    1. Карта для гравця,
    2. Карта для дилера,
    3. Друга карта для гравця
    4. Друга карта для дилера
    5. Перевіряємо чи є блекджек у гравця
    """
    def __call__(self, commons, button_status):
        commons.deck = CardDeck()
        sound_db = SoundDB.get_instance()
        slide = sound_db.get_sound(SOUND_PATH + 'slide.wav')

        if len(commons.dealer_cards) < 2:
            # Пауза між роздачею перших двох карт
            commons.pause_time = PAUSE_05
            if not commons.player_list[0].hand:
                for player in commons.player_list:
                    # Перша карта для гравця
                    slide.play()
                    card = commons.deck.pop()
                    player.hand.append(card)
            elif not commons.dealer_cards:
                # Перша карта дилеру
                slide.play()
                card = commons.deck.pop()
                commons.dealer_cards.append(card)
            elif len(commons.player_list[0].hand) == 1:
                for player in commons.player_list:
                    # Друга карта гравцю
                    slide.play()
                    card = commons.deck.pop()
                    player.hand.append(card)
            elif len(commons.dealer_cards) == 1:
                # Друга карта дилеру
                slide.play()
                card = commons.deck.pop()
                commons.dealer_cards.append(card)
        else:
            blackjack_count = 0
            for player in commons.player_list:
                player_points = get_players_points(player.hand)
                if player_points == 21:
                    blackjack_count += 1
                    if blackjack_count == len(commons.player_list):
                        commons.first_card_hidden = False
                        self.next_state(FinalState)
                else:
                    button_status.hit = True
                    button_status.stand = True
        # області кнопок для зчитування кліку по ним
        button_areas = ButtonArea.get_instance(commons)
        show_buttons(commons.screen, button_status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(commons, button_status)
                commons.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()  # повертає (x, y)

                if button_status.hit and button_areas.hit_area.collidepoint(mouse_position[0], mouse_position[1]):
                    slide.play()
                    card = commons.deck.pop()
                    commons.player_list[commons.player_turn].hand.append(card)
                    self.next_state(PlayerHitState)
                elif button_status.stand and button_areas.stand_area.collidepoint(mouse_position[0], mouse_position[1]):
                    if commons.player_turn == len(commons.player_list) - 1:
                        commons.first_card_hidden = False
                        self.next_state(DealerInitialState)
                    else:
                        commons.player_turn += 1

        show_all_info(commons, button_status)


class PlayerHitState(State):

    def __call__(self, commons, button_status):
        button_areas = ButtonArea.get_instance(commons)
        last_player_index = len(commons.player_list) - 1
        player_points = get_players_points(commons.player_list[commons.player_turn].hand)
        sound_db = SoundDB.get_instance()
        slide = sound_db.get_sound(SOUND_PATH + 'slide.wav')

        if player_points > 21:
            # Перебор
            commons.player_list[commons.player_turn].status['busted'] = True
            if commons.player_turn == last_player_index:
                commons.pause_time = PAUSE_05
                self.next_state(DealerInitialState)
            else:
                commons.player_turn += 1

        elif player_points == 21:
            if commons.player_turn == last_player_index:
                self.next_state(DealerInitialState)
            else:
                commons.player_turn += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save(commons, button_status)
                commons.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if button_areas.hit_area.collidepoint(mouse_position[0], mouse_position[1]):
                    slide.play()
                    card = commons.deck.pop()
                    commons.player_list[commons.player_turn].hand.append(card)
                elif button_areas.stand_area.collidepoint(mouse_position[0], mouse_position[1]):
                    if commons.player_turn == last_player_index:
                        commons.first_card_hidden = False
                        self.next_state(DealerInitialState)
                    else:
                        commons.player_turn += 1
                        self.next_state(PlayerHitState)

        show_all_info(commons, button_status)


class DealerInitialState(State):
    # Перевіряємо чи виграє дилер. Якщо ні, то переходимо до DealerHit

    def __call__(self, commons, button_status):

        commons.first_card_hidden = False  # Розкриття прихованої карти дилера
        dealer_points = get_dealers_points(commons.dealer_cards)
        for player in commons.player_list:
            player_points = get_players_points(player.hand)
            if dealer_points == 21:
                if player_points < 21:
                    # Гравець програє
                    commons.pause_time = PAUSE_3
                    player.status['loose'] = True
                    if player.number == len(commons.player_list):
                        self.next_state(FinalState)
                elif player_points == 21:
                    commons.pause_time = PAUSE_3
                    player.status['push'] = True
                    if player.number == len(commons.player_list):
                        self.next_state(FinalState)
            elif dealer_points == player_points and player_points < 22:
                commons.pause_time = PAUSE_3
                player.status['push'] = True
            elif dealer_points > 15 and dealer_points > player_points:
                # У дилера не менше за 16 та більше за гравця
                commons.pause_time = PAUSE_3
                player.status['loose'] = True
                if player.number == len(commons.player_list):
                    self.next_state(FinalState)
            else:
                self.next_state(DealerHitState)

        show_all_info(commons, button_status)


class DealerHitState(State):

    def __call__(self, commons, button_status):
        dealer_points = get_dealers_points(commons.dealer_cards)
        first_player_points = get_players_points(commons.player_list[0].hand)
        sound_db = SoundDB.get_instance()
        slide = sound_db.get_sound(SOUND_PATH + 'slide.wav')
        if dealer_points > 21:
            self.next_state(FinalState)
        elif dealer_points < 16:
            # Дилер бере карти поки не буде 16 або більше
            slide.play()
            card = commons.deck.pop()
            commons.first_card_hidden = False
            commons.dealer_cards.append(card)
            commons.pause_time = 1.0
            self.next_state(DealerHitState)
        elif dealer_points < 17 and dealer_points < first_player_points:
            # У дилера менше 17 та менше ніж у гравця
            slide.play()
            card = commons.deck.pop()
            commons.first_card_hidden = False
            commons.dealer_cards.append(card)
            commons.pause_time = 1.0
            self.next_state(DealerHitState)
        else:
            self.next_state(FinalState)

        show_all_info(commons, button_status)


class FinalState(State):

    def __call__(self, commons, button_status):
        dealer_points = get_dealers_points(commons.dealer_cards)
        sound_db = SoundDB.get_instance()
        finish = sound_db.get_sound(SOUND_PATH + 'finish.wav')

        for player in commons.player_list:
            get_player_statuses(commons, dealer_points, player.hand, player.number)
            if player.number == len(commons.player_list):
                commons.status_display = True
                commons.pause_time = PAUSE_3
                self.next_state(InitialState)

        if commons.status_display is True or dealer_points > 21:
            finish.play()
            show_statuses(commons.screen, commons.player_list)
        show_all_info(commons, button_status)
