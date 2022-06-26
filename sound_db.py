import pygame


class SoundDB:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.sound_library = {}

    def get_sound(self, path):

        sound = self.sound_library.get(path)
        if sound is None:
            sound = pygame.mixer.Sound(path)
            self.sound_library[path] = sound
        return sound
