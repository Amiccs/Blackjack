class ButtonStatus:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.play = False
        self.hit = False
        self.stand = False
        self.add_player = False

    def reset(self):
        self.play = False
        self.hit = False
        self.stand = False
        self.add_player = False
