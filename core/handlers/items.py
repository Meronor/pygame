import pygame
from core.data.constant import hW, hH


# Класс всех объектов на экране
class Object(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__()
        self.all_sprites = all_sprites
        all_sprites.add(self)
        self.cords = ()
        # Начальные корды
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

        self.cords = (self.rect.x, self.rect.y)


# Класс перса
class Hero(Object):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        all_sprites.add(self)
        self.cords = ()
        # Начальные корды
        self.x = 0
        self.y = 0
        # Повернут ли герой
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
        return (sx, sy) == (0, 0)

    # Идем вниз или вверх до тех пор,
    # Пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне (0 - черный)
    # НЕ РАБОТАЕТ при обходе вверх!
    def overcome_step(self, pixels, dx, dy):
        if pixels[self.centralX() + dx, self.centralY()] != 0:
            self.rect.y += dy
            return False
        else:
            return True

    # Координаты точки отсчета героя
    def centralX(self):
        return self.rect.x + hW

    def centralY(self):
        return self.rect.y + hH


# Класс предметов
class Entity(Object):
    def __init__(self, all_sprites, visible, size, bg, item_image):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        all_sprites.add(self)
        # задаем карткинку
        self.item_image = item_image
        self.size = size
        self.const_size = size
        self.is_visible = visible
        # На каком фоне показывается Object
        # self.bg = bg
        self.picked_up = False
        self.image = pygame.transform.scale(core.handlers.base.load_image(item_image), self.size)
        self.rect = self.image.get_rect()

    def visible(self):
        return self.is_visible

    def pick_up(self, mouse_cords, hero_cords, inventory):
        # Проверка, находится ли курсор на энтити и как далеко находится герой
        if self.is_visible and (self.get_cords()[0] <= mouse_cords[0] <= self.get_cords()[0] + self.size[0]
                                  and self.get_cords()[1] <= mouse_cords[1] <= self.get_cords()[1] + self.size[1]) \
                and (0 <= self.get_cords()[0] - hero_cords[0] <= 50
                     or 0 >= (self.get_cords()[0] + self.size[0]) - hero_cords[0] >= -50):
            self.is_visible = False
            self.picked_up = True

            inventory.append(self)

    def bg_check(self, cur_bg):
        if self.bg != cur_bg:
            self.is_visible = False
        elif self.bg == cur_bg and self.picked_up == False:
            self.is_visible = True
        elif self.bg == cur_bg and self.picked_up == True:
            self.is_visible = False

    def place(self, bg, cords):
        self.change_rect(cords)
        self.picked_up = False
        self.visible = True
        self.size = self.const_size
        self.bg = bg