import os
import sys
import pygame

# Импорт объектов-героев
from core.handlers.items import Hero, Entity, Object
# Получение констант из конфигурации
from core.data.constant import dS, tk


def load_image(name):
    fullname = os.path.join('core/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# сложно, главное, что работает
def corners(pos1, pos2):
    if pos2[0] - pos1[0] <= 0 > pos2[1] - pos1[1]:
        return -1, 1
    elif pos2[0] - pos1[0] <= 0 < pos2[1] - pos1[1]:
        return -1, 1
    elif pos2[0] - pos1[0] >= 0 > pos2[1] - pos1[1]:
        return 1, 1
    elif pos2[0] - pos1[0] >= 0 < pos2[1] - pos1[1]:
        return 1, 1
    elif pos2[0] - pos1[0] < 0 == pos2[1] - pos1[1]:
        return -1, 1
    elif pos2[0] - pos1[0] > 0 == pos2[1] - pos1[1]:
        return 1, 1
    else:
        return 0, 0


def event_handling(events, hero, bg, bg_image, pixels, cords, screen_w, screen_h):
    for event in events:
        # выход из программы при нажатии на крестик
        if event.type == pygame.QUIT:
            return False, cords, bg_image, pixels

        # выход из программы по клавише Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, cords, bg_image, pixels

        # проверка получения новых координат для героя
        if event.type == pygame.MOUSEBUTTONDOWN:
            # новые требуемые координаты героя
            bg_image, pixels = background(hero, bg, bg_image, pixels, event.pos, screen_w, screen_h)
            hero.need_rotate(event.pos)
            return True, event.pos, bg_image, pixels
    return True, cords, bg_image, pixels


def background(hero, bg, bg_image, pixels, cords, screen_w, screen_h):
    if (pixels[cords] == 254 and hero.get_cords()[0] < screen_w * 0.2 and
            bg_image != "background_river.jpg"):
        bg_image = "background_river.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
        wb_bg_image = pygame.transform.scale(load_image("wb_background_river.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)
        hero.change_rect(screen_w * 0.85, screen_h * 0.75)
        return bg_image, pixels
    if (pixels[cords] == 254 and hero.get_cords()[0] > screen_w * 0.7 and
            bg_image != "backround.jpg"):
        bg_image = "backround.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
        wb_bg_image = pygame.transform.scale(load_image("wb_backround.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)
        hero.change_rect(screen_w * 0.01, screen_h * 0.75)
        return bg_image, pixels
    return bg_image, pixels


def screen_init(pygame):
    # получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h
    # растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)

    # устанавливаем название окна
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()

    # растянутый задний фон в ч/б (границы ходьбы) преобразуем в PixelArray
    wb_bg_image = load_image("wb_backround.jpg")
    pixels = pygame.PixelArray(pygame.transform.scale(wb_bg_image, (screen_w, screen_h)))
    return screen, pixels, all_sprites, screen_w, screen_h


def objects_init(pygame, screen_w, screen_h):
    # получаем и растягиваем фон
    bg_image = "backround.jpg"
    bg = Object()
    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
    bg.rect = bg.image.get_rect()
    bg.set_rect(0, 0)

    # Здесь добавляются разные герои

    # Первый объект Hero
    hero = Hero()
    hero_image = load_image("hero.jpg")
    hero.image = pygame.transform.scale(hero_image, (dS, dS))
    hero.rect = hero.image.get_rect()
    # засовываем картинку героя в квадрат dSxdS (175х175)
    # начальные координаты левого верхнего угла прямоугольной области для персонажа
    hero.set_rect(screen_w * 0.75, screen_h * 0.75)

    # Второй объект
    apple = Entity()
    apple.image = pygame.transform.scale(load_image("apple.jpg"), (100, 100))
    apple.rect = apple.image.get_rect()
    apple.set_rect(250, 250)

    # Возврат героя и списка всех objects
    return hero, bg, bg_image, [apple]


def game_init(screen, hero, bg, all_sprites, objects, screen_w, screen_h):
    all_sprites.add(bg)
    for i in objects:
        all_sprites.add(i)
    all_sprites.add(hero)
    all_sprites.draw(screen)

    clock = pygame.time.Clock()

    # isStep = False - маркер приостаноки, т. е. требуется обход препятствия (текущая пиксела не валидная)
    isStep = True
    # новые требуемые координаты героя совпадают с собственными координатами героя
    cords = (screen_w * 0.75, screen_h * 0.75)
    running = True
    return running, isStep, clock, cords


def game_update(pygame, screen, all_sprites, hero, cords, clock):
    # проверка необходимости перевернуть героя
    hero.need_rotate(cords)

    all_sprites.draw(screen)

    clock.tick(tk)

    # Отображение новых изменений (перерисовка)
    pygame.display.flip()
