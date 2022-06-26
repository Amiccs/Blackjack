import pygame


class ImageDB:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.image_library = {}

    def get_image(self, path):

        image = self.image_library.get(path)
        if image is None:
            image = pygame.image.load(path)
            self.image_library[path] = image
        return image
