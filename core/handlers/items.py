import pygame
from core.data.constant import hX, hY, hW, hH


# класс всех объектов на экране
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cords = ()
        # начальные корды
        self.x = hX
        self.y = hY

    def get_cords(self):
        return self.cords

    def set_rect(self, sx, sy):
        self.rect.x += sx
        self.rect.y += sy


# класс перса
class Hero(Object):
    def __init__(self):
        super().__init__()
        self.cords = ()
        # начальные корды
        self.x = hX
        self.y = hY
        # повернут ли герой
        self.f = False

    def __call__(self, screen, *args):
        # перерисовываем героя на новые корды (в args передеём х и у)
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

    def need_step(self, cords):
        return cords[0] != self.centralX() or cords[1] != self.centralY()

    def set_diff(self, cords, pixels):
        sx, sy = 0, 0
        print(cords, (self.centralX(), self.centralY()))
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
    # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне (0 - черный).
    # ПРОВЕРИТЬ! судя по всему этот код только для сглаженной функции!
    # НЕ РАБОТАЕТ при обходе вверх!
    def overcomeStep(self, pixels, dx, dy):
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
class Item:
    def __init__(self):
        self.cords = ()
        # его начальные корды
        self.x = 410
        self.y = 540

    def __call__(self, screen, *args):
        # перерисовываем на новые корды (в args передеём х и у)
        self.x += args[0]
        self.y += args[1]
        pygame.draw.rect(screen, 'red', (self.x, self.y, 100, 150), 8)
        self.cords = (self.x, self.y)

    def get_cords(self):
        return self.cords


# класс картинок
class Image(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.cords = ()
        # начальные корды
        self.x = hX
        self.y = hY

    def get_cords(self):
        return self.cords
