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
    bg_image = "backgrounds/background.jpg"
    bg = Object(all_sprites)
    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
    bg.rect = bg.image.get_rect()
    bg.set_rect(0, 0)
    # Растянутый задний фон в ч/б (границы ходьбы) преобразуем в PixelArray
    wb_bg_image = load_image("wb_backgrounds/wb_background.jpg")
    pixels = pygame.PixelArray(pygame.transform.scale(wb_bg_image, (screen_w, screen_h)))

    return screen, pixels, all_sprites, bg, bg_image, screen_w, screen_h


# Добавляем объекты
def objects_init(pygame, all_sprites, screen_w, screen_h):
    # Здесь добавляются разные герои

    '''
    apple = Entity(all_sprites, True)
    apple.image = pygame.transform.scale(load_image("grass.PNG"), (screen_w, screen_h))
    apple.rect = apple.image.get_rect()
    apple.set_rect(0, 0)
    '''

    # Второй объект !!!HERO всегда последний!!!
    hero = Hero(all_sprites)
    hero_image = load_image("hero.jpg")
    hero.image = pygame.transform.scale(hero_image, (dS, dS))
    hero.rect = hero.image.get_rect()
    # Первый объект

    # Начальные координаты левого верхнего угла прямоугольной области для персонажа
    hero.set_rect(screen_w * 0.75, screen_h * 0.75)

    # Возврат героя и списка всех objects
    return hero, []


# Добавляем все спрайты в группу спрайтов и инициализируем начальные переменные
def game_init(screen, all_sprites, screen_w, screen_h):
    all_sprites.draw(screen)

    # Главная музыка, ее воспроизведение
    pygame.mixer.music.load("core/data/musc/loc_sound.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    clock = pygame.time.Clock()

    # isStep = False - маркер приостаноки, т. е. требуется обход препятствия (текущая пиксела не валидная)
    isStep = True
    # isImpasse = True - маркер начала обхода препятствия (текущая пиксела не валидная)
    isImpasse = False
    # Новые требуемые координаты героя совпадают с собственными координатами героя
    cords = (screen_w * 0.75, screen_h * 0.75)
    running = True
    dx, dy = 0, 0

    color = 0

    # что то непонятное
    fps = 0

    # какие то счетчики
    count = 0
    ccount = 0
    cccount = 0
    speccou = 0

    # Спрайты для анимации
    spFOX = [load_image(f"movement/move{x}.PNG") for x in range(30)]
    spRiv = [load_image(f"river/background_river{y}.PNG") for y in range(3)]
    spCentralLoc = [load_image(f"centralloc/cloc{y}.PNG") for y in range(3)]
    spBluefor = [load_image(f"bluefor/blf{y}.PNG") for y in range(4)]
    spHome = [load_image(f"home/home{y}.PNG") for y in range(3)]

    return running, isStep, isImpasse, clock, cords, dx, dy, fps, count, ccount, cccount, speccou, spFOX, spRiv, spCentralLoc, color


# Обработка клика
def event_handling(events, hero, bg_image, objects, pixels, cords, color):
    for event in events:
        # Выход из программы при нажатии на крестик
        if event.type == pygame.QUIT:
            return False, cords, bg_image, pixels, color

        # Выход из программы по клавише Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, cords, bg_image, pixels, color

        # Проверка получения новых координат для героя
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Новые требуемые координаты героя
            hero.need_rotate(event.pos)
            # Проверяем, можно ли подобрать предмет, если да, то подбираем
            for i in objects:
                # Если объект видно, мышка наведена на объект и герой находится не далеко, объект пропадает с экрана
                i.pick_up(event.pos, hero.cords)
            color = pixels[event.pos]

            return True, event.pos, bg_image, pixels, color
    return True, cords, bg_image, pixels, color


# Меняем фон
def background(hero, bg, bg_image, pixels, screen_w, screen_h, count, color):
    # Если нажали на красный цвет, и персонаж находится недалеко от бортика, выбираем соответствующий фон
    if color == 66047:
        bg_image = f"river/background_river{count // 20}.PNG"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_background_river.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        # Устанавливаем место героя
        hero.change_rect(screen_w * 0.85, screen_h * 0.75)

        # Звук течения реки
        music_play('river')

        return bg_image, pixels

    if color == 254:
        bg_image = "backgrounds/background.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_background.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        hero.change_rect(screen_w * 0.01, screen_h * 0.75)

        # Звук главного меню
        music_play('main')

        return bg_image, pixels

    if color == 65515:
        bg_image = "backgrounds/forest.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_forest.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        hero.change_rect(screen_w * 0.01, screen_h * 0.75)

        # Звук главного меню
        music_play('main')

        return bg_image, pixels

    if color == 130816:
        bg_image = "backgrounds/home.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_home.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        hero.change_rect(screen_w * 0.5, screen_h * 0.75)

        # Звук главного меню
        music_play('main')

        return bg_image, pixels
    return bg_image, pixels


# Функция обхода препятствий
def step_handling(screen, bg, bg_image, pixels, cords, hero, all_sprites, barrier, isImpasse, dx, dy, count, ccount,
                  cccount, screen_w,
                  screen_h, color):
    # Смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем
    if pixels[cords] == 0 and hero.need_step(cords):

        ccount, cccount = update_anim_counters(screen, all_sprites, count, ccount, cccount)
        # Меняем корды героя, если хоть одна отличается от кордов клика

        # Обновляем счетчик на 60
        print(bg_image)
        count += 1
        if count == 60:
            count = 0

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
    elif not hero.need_step(cords) and color != 0:
        bg_image, pixels = background(hero, bg, bg_image, pixels, screen_w, screen_h, count, color)
        cords = hero.get_cords()

    # Если пиксель цветной, идем к верхнему черному пикселю по этому Y
    elif pixels[cords] != 0 and pixels[cords] != 16777215 and cords[1] < screen_h - 1:
        # Ищем верхний черный пиксель данного столбца
        for i in range(screen_h):
            if pixels[cords[0], i] == 0:
                # Задаем новые корды к которым пойдет персонаж
                cords = cords[0], i
                break

    return barrier, isImpasse, dx, dy, count, ccount, cccount, cords, bg_image, pixels


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
    running, barrier, isImpasse, clock, cords, dx, dy, fps, count, ccount, cccount, speccou, spFOX, spRiv, spCentralLoc, color = \
        game_init(screen, all_sprites, screen_w, screen_h)

    while running:
        fps = animation(hero, bg, fps, spFOX, spRiv, ccount, screen_w, screen_h, bg_image, spCentralLoc)

        running, cords, bg_image, pixels, color = event_handling(pygame.event.get(), hero, bg_image, objects, pixels,
                                                                 cords, color)
        barrier, isImpasse, dx, dy, count, ccount, cccount, cords, bg_image, pixels = step_handling(screen, bg,
                                                                                                    bg_image, pixels,
                                                                                                    cords,
                                                                                                    hero, all_sprites,
                                                                                                    barrier, isImpasse,
                                                                                                    dx, dy, count,
                                                                                                    ccount, cccount,
                                                                                                    screen_w, screen_h,
                                                                                                    color)

        game_update(pygame, screen, all_sprites, hero, cords, clock)


def update_anim_counters(screen, all_sprites, count, ccount, cccount):
    # Какие-то действия со счетчиками
    if count % 4 == 0 and count != 0:
        all_sprites.draw(screen)
        ccount += 1
        if ccount == 15 and cccount == 0:
            cccount = 1
            ccount = 0
    return ccount, cccount


def animation(hero, bg, fps, spFOX, spRiv, ccount, screen_w, screen_h, bg_image, spCentralLoc):
    fps += 1
    print(fps)
    if fps == 360:
        fps = 0
    if 'background_river' in bg_image and fps % 40 == 0:
        bg.image = pygame.transform.scale(spRiv[fps // 40], (screen_w, screen_h))
    if 'background' in bg_image and fps % 120 == 0:
        bg.image = pygame.transform.scale(spCentralLoc[fps // 120], (screen_w, screen_h))
    if hero.is_rotate():
        hero.image = pygame.transform.scale(spFOX[ccount % len(spFOX)], (dS, dS))
    else:
        hero.image = pygame.transform.scale(pygame.transform.flip(spFOX[ccount % len(spFOX)], True, False), (dS, dS))
    return fps


def music_play(key):
    riversound = pygame.mixer.Sound("core/data/musc/ivsound.wav")
    icesound = pygame.mixer.Sound("core/data/musc/ices.wav")
    if key == 'river':
        icesound.stop()
        riversound.play()
        riversound.set_volume(0.2)
    elif key == 'ice':
        riversound.stop()
    elif key == 'main':
        icesound.stop()
        riversound.stop()


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
