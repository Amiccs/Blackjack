import pygame
from globals import *


class ButtonArea:
    instance = None

    @classmethod
    def get_instance(cls, commons):
        if cls.instance is None:
            cls.instance = cls(commons)
        return cls.instance

    def __init__(self, commons):
        button_x_pos, button_y_pos = BUTTON_POS

        self.play_area = pygame.Rect(button_x_pos,
                                     button_y_pos,
                                     commons.button_image_width,
                                     commons.button_image_height)
        button_x_pos += SPACE_BETWEEN_BUTTONS
        self.hit_area = pygame.Rect(button_x_pos,
                                    button_y_pos,
                                    commons.button_image_width,
                                    commons.button_image_height)
        button_x_pos += SPACE_BETWEEN_BUTTONS
        self.stand_area = pygame.Rect(button_x_pos,
                                      button_y_pos,
                                      commons.button_image_width,
                                      commons.button_image_height)
        button_x_pos += SPACE_BETWEEN_BUTTONS
        self.add_player_area = pygame.Rect(button_x_pos,
                                           button_y_pos,
                                           commons.button_image_width,
                                           commons.button_image_height)
