import os

import pygame
from core.data.constant import hW, hH
from core.handlers.base import load_image


# класс всех объектов на экране
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cords = ()
        # начальные корды
        self.x = 0
        self.y = 0

    def get_cords(self):
        return self.cords

    def set_rect(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        self.cords = (self.rect.x, self.rect.y)

    def change_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y


# класс перса
class Hero(Object):
    def __init__(self):
        super().__init__()
        self.cords = ()
        # начальные корды
        self.x = 0
        self.y = 0
        # повернут ли герой
        self.f = False

    def __call__(self, screen, x, y):
        self.x += x
        self.y += y

        self.cords = (self.x, self.y)

    def need_rotate(self, cords):
        if self.centralX() > cords[0] and self.is_rotate():
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate()
        if self.centralX() < cords[0] and not self.is_rotate():
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate()

    def is_rotate(self):
        return self.f

    def rotate(self):
        if self.f:
            self.f = False
        else:
            self.f = True

    def need_step(self, cords):
        return cords[0] != self.centralX() or cords[1] != self.centralY()

    def set_diff(self, cords, pixels):
        sx, sy = 0, 0
        if cords[0] > self.centralX() and pixels[self.centralX() + 1, self.centralY()] == 0:
            sx = 1
        elif cords[0] < self.centralX() and pixels[self.centralX() - 1, self.centralY()] == 0:
            sx = -1
        if cords[1] > self.centralY() and pixels[self.centralX(), self.centralY() + 1] == 0:
            sy = 1
        elif cords[1] < self.centralY() and pixels[self.centralX(), self.centralY() - 1] == 0:
            sy = -1

        return sx, sy

    def next_step(self, cords, pixels):
        sx, sy = self.set_diff(cords, pixels)
        self.set_rect(sx, sy)
        return sx, sy

    # идем вниз или вверх до тех пор,
    # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне (0 - черный)
    # НЕ РАБОТАЕТ при обходе вверх!
    def overcome_step(self, pixels, dx, dy):
        if pixels[self.centralX() + dx, self.centralY()] != 0:
            self.rect.y += dy
            return False
        else:
            return True

    # координаты точки отсчета героя
    def centralX(self):
        return self.rect.x + hW

    def centralY(self):
        return self.rect.y + hH


# класс предметов
class Entity(Object):
    def __init__(self, x, y, visible):
        super().__init__()
        self.x = x
        self.y = y
        self.size = (100, 100)
        self.cords = (self.x, self.y)
        self.is_visible = visible


    def __call__(self, screen, x, y):
        self.x += x
        self.y += y

        self.cords = (self.x, self.y)


    def disappear(self):
        self.is_visible = False

    def visible(self):
        return self.is_visible

    def pick_up(self, mouse_cords, hero_cords):
        # проверка, находится ли курсор на энтити и как далеко находится герой
        if (self.x <= mouse_cords[0] <= self.x + self.size[0] and self.y <= mouse_cords[1] <= self.y + self.size[1])\
                and (0 <= self.x - hero_cords[0] <= 50 or 0 >= (self.x + self.size[0]) - hero_cords[0] >= -50):

            self.disappear()
            print('clicked')
