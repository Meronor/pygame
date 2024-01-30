import pygame
from core.data.constant import hW, hH
import core.handlers.base as base
import os


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

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def checkForNear(self, hero_cords):
        if (0 <= self.get_cords()[0] - hero_cords[0] <= 50
                or 0 >= (self.get_cords()[0] + self.size[0]) - hero_cords[0] >= -50):
            return True
        return False


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
    def __init__(self, all_sprites, visible, picable, size, bg, item_image, active_color):
        super().__init__(all_sprites)
        self.all_sprites = all_sprites
        all_sprites.add(self)
        # задаем карткинку
        self.item_image = item_image
        self.size = size
        self.const_size = size
        self.is_visible = visible
        self.is_picable = picable
        # На каком фоне показывается Object
        try:
            self.bg = os.listdir(bg)
        except Exception:
            self.bg = bg

        self.picked_up = False
        self.image = pygame.transform.scale(base.load_image(item_image), self.size)
        self.rect = self.image.get_rect()
        # Цвет на которое будет триггериться действие
        self.active_color = active_color
        self.action = False

    def set_rect(self, dx, dy, color):
        self.rect.x += dx
        self.rect.y += dy

        self.cords = (self.rect.x, self.rect.y)

        if self.active_color == color:
            self.action = True

    def visible(self):
        return self.is_visible

    def pick_up(self, mouse_cords, hero_cords, inventory):
        # Проверка, находится ли курсор на энтити и как далеко находится герой
        if self.is_picable and self.is_visible and self.checkForInput(mouse_cords) and self.checkForNear(
                hero_cords) and self not in inventory:
            self.all_sprites.remove(self)
            self.is_visible = False
            self.picked_up = True

            inventory.append(self)
            return True
        return False

    def bg_check(self, cur_bg):
        try:
            cur_bg = cur_bg.split('/')[1]
        except Exception:
            pass
        if self.bg not in cur_bg:
            self.is_visible = False
        elif self.bg in cur_bg and self.picked_up:
            self.is_visible = False
        elif self.bg in cur_bg and not self.picked_up:
            self.is_visible = True

    def place(self, bg, cords):
        self.change_rect(cords)
        self.picked_up = False
        self.visible = True
        self.size = self.const_size
        self.bg = bg


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Image:
    def __init__(self, image, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.image = base.load_image(image)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False
