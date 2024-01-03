import pygame
from core.handlers.base import load_image

# класс перса
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cords = ()
        # его начальные корды
        self.x = 460
        self.y = 490
        self.f = False

    def __call__(self, screen, *args):
        # перерисовываем на новые корды (в args передеём х и у)
        self.x += args[0]
        self.y += args[1]

        self.cords = (self.x, self.y)

    def is_rotate(self):
        return self.f

    def rotate(self):
        if self.f:
            self.f = False
        else:
            self.f = True

    def get_cords(self):
        return self.cords


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cords = ()
        self.f = False

    def __call__(self, screen, *args):
        # перерисовываем на новые корды (в args передеём х и у)
        self.x += args[0]
        self.y += args[1]
        self.coords = (self.x, self.y)


    def get_cords(self):
        return self.cords

