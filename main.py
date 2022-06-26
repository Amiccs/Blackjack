import time
from states import *
from button_status import ButtonStatus
from common_variables import CommonVariables
from image_db import ImageDB


class BlackJack(object):
    # pygame
    pygame.init()
    pygame.display.set_caption('Black Jack')
    pygame.display.set_icon(pygame.image.load(IMAGE_PATH + ICON))
    pygame.font.init()
    clock = pygame.time.Clock()

    # Загальні змінні
    commons = CommonVariables.get_instance()
    button_status = ButtonStatus.get_instance()
    image_db = ImageDB.get_instance()

    # Ініціалізуємо потрібні для гри змінні
    commons.done = False
    commons.display_status = False
    commons.screen = pygame.display.set_mode(BOARD_SIZE)
    commons.game_rounds = 0
    commons.pause_time = 0
    commons.player_turn = 1
    commons.dealer_cards = []
    commons.first_card_hidden = True
    commons.button_image_width = image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_ON).get_width()
    commons.button_image_height = image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_ON).get_height()
    commons.text_font = pygame.font.SysFont('Arial', 21)
    players_font = pygame.font.SysFont('Arial', 16)

    current_state = InitialState()

    # Головний цикл
    while not commons.done:
        # Поле гри
        commons.screen.fill(BACKGROUND_COLOR)
        x_pos = int((BOARD_X_SIZE - image_db.get_image(IMAGE_PATH + LOGO).get_width()) / 2)
        y_pos = int(BOARD_Y_SIZE * 0.283)
        commons.screen.blit(image_db.get_image(IMAGE_PATH + LOGO), (x_pos, y_pos))
        # Виведення кількості очків гравців
        if commons.player_list is not None:
            x_pos = 22
            for player in commons.player_list:
                count = get_players_points(player.hand)
                message = players_font.render('{0}'.format(count), False, YELLOW_COLOR)
                commons.screen.blit(message, (x_pos, int(BOARD_Y_SIZE * 0.66)))
                x_pos = SPACE_BETWEEN_CARDS + int(BOARD_X_SIZE * 0.24) * player.number
        # Виведення кількості очків дилера
        if not commons.first_card_hidden:
            count = get_dealers_points(commons.dealer_cards)
            message = players_font.render('{0}'.format(count), False, YELLOW_COLOR)
            commons.screen.blit(message, (int(BOARD_X_SIZE * 0.4), int(BOARD_Y_SIZE * 0.166)))

        # Виведення кількості зіграних раундів
        x_pos, y_pos = STATUS_POS
        message1 = commons.text_font.render('Round: {0}'.format(commons.game_rounds), False, YELLOW_COLOR)
        commons.screen.blit(message1, (x_pos, y_pos))
        # Виведення черги гравця
        y_pos += 30
        message2 = commons.text_font.render('Player turn: {0}'.format(commons.player_turn + 1), False, YELLOW_COLOR)
        commons.screen.blit(message2, (x_pos, y_pos))

        # Перехід до поточного етапу
        current_state(commons, button_status)

        # Обновляємо екран
        pygame.display.flip()

        # Паузи
        if commons.pause_time:
            time.sleep(commons.pause_time)
            commons.pause_time = 0

        # ФПС
        clock.tick(30)


if __name__ == '__main__':
    GAME = BlackJack()
