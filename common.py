import json
from globals import *
from image_db import ImageDB


def save(commons, button_status):
    players = []
    for player in commons.player_list:
        cards = []
        for card in player.hand:
            r = card.get_rank()
            s = card.get_suit()
            rank_suit = {
                'rank': r,
                'suit': s
            }
            cards.append(rank_suit)
        props = {
            'player_number': player.number,
            'player_status': player.status,
            'player_cards': cards
        }
        players.append(props)
    json_object = {
        'round': commons.game_rounds,
        'player_turn': commons.player_turn,
        'first_card_hidden': commons.first_card_hidden,
        'play': button_status.play,
        'hit': button_status.hit,
        'stand': button_status.stand,
        'add_player': button_status.add_player,
        "players": players
    }
    json_save = json.dumps(json_object, indent=4)
    print(json_save)
    with open('save.json', 'w') as saving:
        saving.write(json_save)


def get_player_statuses(commons, dealer_points, player_cards, player_number):
    p_index = player_number - 1
    player_points = get_players_points(player_cards)
    if dealer_points == 21:
        if player_points < 21:
            commons.player_list[p_index].status['loose'] = True
        elif player_points == 21:
            commons.player_list[p_index].status['push'] = True
    elif player_points == 21:
        commons.player_list[p_index].status['blackjack'] = True
    elif 21 > player_points > dealer_points or dealer_points > 21 > player_points:
        commons.player_list[p_index].status['win'] = True
    elif player_points == dealer_points:
        commons.player_list[p_index].status['push'] = True
    elif player_points < dealer_points < 21:
        commons.player_list[p_index].status['loose'] = True


def get_players_points(hand):
    total = 0
    point_ace = 0
    for card in hand:
        rank = card.get_rank()
        if rank > 10:
            total += 10
        elif rank == 1 and total <= 10:
            total += 11
            point_ace += 1
        else:
            total += rank
        if point_ace and total > 21:
            total -= 10
            point_ace -= 1

    return total


def get_dealers_points(hand):
    total = 0
    point_ace = 0
    for card in hand:
        rank = card.get_rank()
        if rank > 10:
            total += 10
        elif rank == 1:
            # Якщо є Туз та сума очок від 17 до 21, то Туз рахується як 11 очок
            if 17 <= (total + 11) < 22:
                total += 11
            else:
                # Інакше з Тузом буде більше за 22 очка, тоді він рахується як 1 очко
                point_ace = 1
                total += 1
                continue
        else:
            total += rank

        if point_ace and 17 <= (total + point_ace * 10) < 22:
            # Якщо при додаванні наступних карт сума очків з Тузом буде менше за 22, тоді рахуємо Туз як 11 очків
            total += 10

    return total


def show_all_info(commons, button_status):
    show_buttons(commons.screen, button_status)
    for player in commons.player_list:
        show_players_hand(commons.screen, player.hand, player.number)
    show_dealers_hand(commons.screen, commons.dealer_cards, commons.first_card_hidden)


def show_buttons(screen, button_status):
    button_x_pos, button_y_pos = BUTTON_POS
    image_db = ImageDB.get_instance()
    if button_status.play is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += SPACE_BETWEEN_BUTTONS

    if button_status.hit is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_ON), (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_OFF), (button_x_pos, button_y_pos))
    button_x_pos += SPACE_BETWEEN_BUTTONS

    if button_status.stand is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += SPACE_BETWEEN_BUTTONS

    if button_status.add_player is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + ADD_PLAYER_BUTTON_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + ADD_PLAYER_BUTTON_OFF),
                    (button_x_pos, button_y_pos))


def show_players_hand(screen, player_cards, player_number):
    player_x_pos, player_y_pos = PLAYER_POS
    if player_number > 1:
        player_x_pos = player_x_pos + SPACE_BETWEEN_PLAYERS * (player_number - 1)
    image_db = ImageDB.get_instance()
    for card in player_cards:
        image = get_card_filename(IMAGE_PATH_CARDS, card)
        screen.blit(image_db.get_image(image), (player_x_pos, player_y_pos))
        player_x_pos += SPACE_BETWEEN_CARDS
        player_y_pos -= 14


def show_dealers_hand(screen, dealer_cards, first_card_hidden):
    dealer_x_pos, dealer_y_pos = DEALER_POS
    image_db = ImageDB.get_instance()
    for card in dealer_cards:
        if first_card_hidden is True:
            # Показ першої картки дилера
            screen.blit(image_db.get_image(IMAGE_PATH_CARDS + CARD_HIDDEN),
                        (dealer_x_pos, dealer_y_pos))
        else:
            image = get_card_filename(IMAGE_PATH_CARDS, card)
            screen.blit(image_db.get_image(image), (dealer_x_pos, dealer_y_pos))
        first_card_hidden = False
        dealer_x_pos += SPACE_BETWEEN_CARDS
        dealer_y_pos += 14


def show_statuses(screen, players):
    player_x_pos, player_y_pos = PLAYER_POS
    image_db = ImageDB.get_instance()
    x_offset = -30
    y_offset = -110

    for player in players:
        if player.status['blackjack']:
            screen.blit(image_db.get_image(IMAGE_PATH_STATUSES + "blackjack.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif player.status['win']:
            screen.blit(image_db.get_image(IMAGE_PATH_STATUSES + "you_win.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif player.status['push']:
            screen.blit(image_db.get_image(IMAGE_PATH_STATUSES + "push.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif player.status['loose']:
            screen.blit(image_db.get_image(IMAGE_PATH_STATUSES + "you_loose.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif player.status['busted']:
            screen.blit(image_db.get_image(IMAGE_PATH_STATUSES + "busted.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        x_offset += int(BOARD_X_SIZE * 0.237)


def show_results(screen, text_font, message):
    text_to_plot = text_font.render(message, False, YELLOW_COLOR)
    x_pos, y_pos = STATUS_POS
    screen.blit(text_to_plot, (x_pos, y_pos + 50))


def get_card_filename(path, card):
    card_rank = ["Zero", "ace", "2", "3", "4", "5", "6", "7",
                 "8", "9", "10", "jack", "queen", "king"]
    card_suit = ["s", "c", "d", "h"]
    image = path + card_rank[card.get_rank()] + "_" + card_suit[card.get_suit()] + ".png"
    return image
