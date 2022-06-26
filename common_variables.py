class CommonVariables:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.button_image_height = None
        self.button_image_width = None
        self.dealer_cards = None
        self.deck = None
        self.display_status = None
        self.done = None
        self.first_card_hidden = None
        self.game_rounds = None
        self.pause_time = None
        self.player_list = None
        self.player_turn = None
        self.screen = None
        self.text_font = None
