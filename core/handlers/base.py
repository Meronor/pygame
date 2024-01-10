import os
import sys
import pygame

# Импорт объектов-героев
from core.handlers.items import Hero, Entity, Object
# Получение констант из конфигурации
from core.data.constant import dS, tk


# Первоначальная загрузка окна
def screen_init(pygame):
    # Получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    # Растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)

    # Устанавливаем название окна
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()

    # Получаем и растягиваем фон
    bg_image = "backround.jpg"
    bg = Object(all_sprites)
    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
    bg.rect = bg.image.get_rect()
    bg.set_rect(0, 0)

    # Растянутый задний фон в ч/б (границы ходьбы) преобразуем в PixelArray
    wb_bg_image = load_image("wb_backround.jpg")
    pixels = pygame.PixelArray(pygame.transform.scale(wb_bg_image, (screen_w, screen_h)))
    return screen, pixels, all_sprites, bg, bg_image, screen_w, screen_h


# Добавляем объекты
def objects_init(pygame, all_sprites, screen_w, screen_h):
    # Здесь добавляются разные герои

    # Первый объект
    apple = Entity(all_sprites, True)
    apple.image = pygame.transform.scale(load_image("apple.jpg"), (100, 100))
    apple.rect = apple.image.get_rect()
    apple.set_rect(250, 800)

    # Второй объект !!!HERO всегда последний!!!
    hero = Hero(all_sprites)
    hero_image = load_image("hero.jpg")
    hero.image = pygame.transform.scale(hero_image, (dS, dS))
    hero.rect = hero.image.get_rect()

    # Начальные координаты левого верхнего угла прямоугольной области для персонажа
    hero.set_rect(screen_w * 0.75, screen_h * 0.75)

    # Возврат героя и списка всех objects
    return hero, [apple]


# Добавляем все спрайты в группу спрайтов и инициализируем начальные переменные
def game_init(screen, all_sprites, screen_w, screen_h):
    all_sprites.draw(screen)

    clock = pygame.time.Clock()

    # isStep = False - маркер приостаноки, т. е. требуется обход препятствия (текущая пиксела не валидная)
    isStep = True
    # isImpasse = True - маркер начала обхода препятствия (текущая пиксела не валидная)
    isImpasse = False
    # Новые требуемые координаты героя совпадают с собственными координатами героя
    cords = (screen_w * 0.75, screen_h * 0.75)
    running = True
    dx, dy = 0, 0
    return running, isStep, isImpasse, clock, cords, dx, dy


# Обработка клика
def event_handling(events, hero, bg, bg_image, objects, pixels, cords, screen_w, screen_h):
    for event in events:
        # Выход из программы при нажатии на крестик
        if event.type == pygame.QUIT:
            return False, cords, bg_image, pixels

        # Выход из программы по клавише Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, cords, bg_image, pixels

        # Проверка получения новых координат для героя
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Новые требуемые координаты героя
            bg_image, pixels = background(hero, bg, bg_image, pixels, event.pos, screen_w, screen_h)
            hero.need_rotate(event.pos)
            # Проверяем, можно ли подобрать предмет, если да, то подбираем
            for i in objects:
                # Если объект видно, мышка наведена на объект и герой находится не далеко, объект пропадает с экрана
                i.pick_up(event.pos, hero.cords)
            return True, event.pos, bg_image, pixels
    return True, cords, bg_image, pixels


# Меняем фон
def background(hero, bg, bg_image, pixels, cords, screen_w, screen_h):
    # Если нажали на красный цвет, и персонаж находится недалеко от бортика, выбираем соответствующий фон
    if (pixels[cords] == 254 and hero.get_cords()[0] < screen_w * 0.2 and
            bg_image != "background_river.jpg"):
        bg_image = "background_river.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_background_river.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        # Устанавливаем место героя
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


# Функция обхода препятствий
def step_handling(pixels, cords, hero, barrier, isImpasse, dx, dy):
    # Смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем
    if pixels[cords] == 0 and hero.need_step(cords):
        # Меняем корды героя, если хоть одна отличается от кордов клика

        # Проверяем, обходит ли герой в данный момент препятствие
        if barrier:
            # Делаем шаг
            isImpasse = hero.next_step(cords, pixels)

        # ВАЖНО! Если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
        # То наш перс стоит в тупике, ниже код обхода этого тупика
        if isImpasse:
            # Если barrier = False, наш герой уже обходит препятствие
            if barrier:
                # В corners проверяем различные ситуации, когда обходить надо по разному
                dx, dy = corners((hero.centralX(), hero.centralY()), cords)

            # Меняем корды героя на dx, dy, если возвращается True, мы обошли препятствие,
            # Иначе повторяем код со следующим тиком
            barrier = hero.overcome_step(pixels, dx, dy)
    return barrier, isImpasse, dx, dy


# Переход на новый тик
def game_update(pygame, screen, all_sprites, hero, cords, clock):
    # Проверка необходимости перевернуть героя
    hero.need_rotate(cords)

    # Перерисовываем экран
    all_sprites.draw(screen)

    clock.tick(tk)

    # Отображение новых изменений (перерисовка)
    pygame.display.flip()


def game(pygame):
    # Конфигурация экрана
    screen, pixels, all_sprites, bg, bg_image, screen_w, screen_h = screen_init(pygame)

    # Получение героя, фон, картинку фона, остальные объекты в списке
    hero, objects = objects_init(pygame, all_sprites, screen_w, screen_h)

    # Задание значений игровых переменных
    running, barrier, isImpasse, clock, cords, dx, dy = \
        game_init(screen, all_sprites, screen_w, screen_h)

    while running:
        running, cords, bg_image, pixels = event_handling(pygame.event.get(), hero, bg, bg_image, objects, pixels,
                                                          cords, screen_w, screen_h)
        barrier, isImpasse, dx, dy = step_handling(pixels, cords, hero, barrier, isImpasse, dx, dy)

        game_update(pygame, screen, all_sprites, hero, cords, clock)


def load_image(name):
    fullname = os.path.join('core/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# Сложно, главное, что работает
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
