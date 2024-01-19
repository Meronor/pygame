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
    bg_image = "backgrounds/start_menu.jpg"
    bg = Object(all_sprites)
    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
    bg.rect = bg.image.get_rect()
    bg.set_rect(0, 0)

    # Растянутый задний фон в ч/б (границы ходьбы) преобразуем в PixelArray
    wb_bg_image = load_image("wb_backgrounds/wb_start_menu.jpg")
    pixels = pygame.PixelArray(pygame.transform.scale(wb_bg_image, (screen_w, screen_h)))

    # скрываем системный курсор
    pygame.mouse.set_visible(False)

    return screen, pixels, all_sprites, bg, bg_image, screen_w, screen_h


# Добавляем объекты
def objects_init(pygame, all_sprites, screen_w, screen_h):
    # Здесь добавляются разные герои

    # Первый объект
    apple = Entity(all_sprites, True, (100, 100), 'backg_main.jpg', "snejinka.PNG")
    apple.set_rect(500, 800)
    # Второй объект
    snowball = Entity(all_sprites, True, (100, 100), 'core/data/river', "snowball.png")
    snowball.set_rect(1000, 800)

    #frog = Entity(all_sprites, True)
    #frog.image = pygame.transform.scale(load_image("frog/frog0.PNG"), (600, 400))
    #frog.rect = apple.image.get_rect()
    #frog.set_rect(190, 560)

    # !!!HERO всегда предпоследний!!!
    hero = Hero(all_sprites)
    hero_image = load_image("hero.jpg")
    hero.image = pygame.transform.scale(hero_image, (dS, dS))
    hero.rect = hero.image.get_rect()

    # !!!Курсор всегда последний!!!
    cursor_image = "cursor.jpg"
    cursor = pygame.sprite.Sprite(all_sprites)

    cursor.image = pygame.transform.scale(load_image(cursor_image), (screen_w * 0.05, screen_h * 0.05))
    cursor.rect = cursor.image.get_rect()

    # objects
    objects = [apple, snowball]

    # Начальные координаты левого верхнего угла прямоугольной области для персонажа
    hero.set_rect(screen_w * 0.75, screen_h * 0.75)

    # Возврат героя и списка всех objects
    return cursor, hero, objects


# Добавляем все спрайты в группу спрайтов и инициализируем начальные переменные
def game_init(screen, all_sprites, screen_w, screen_h, objects):
    for i in objects:
        # Если объект видно, мышка наведена на объект и герой находится не далеко, объект пропадает с экрана
        i.bg_check('backround.jpg')
        if i.visible() == False and i in all_sprites:
            all_sprites.remove(i)
        elif i.visible() == True and i not in all_sprites:
            # Добавление спрайта на предпоследнее место в группе
            sprites = list(all_sprites.sprites())  # Преобразование группы в список
            sprites.insert(-2, i)  # Вставка нового спрайта на предпоследнее место
            all_sprites.empty()  # Очистка группы
            for sprite in sprites:
                all_sprites.add(sprite)  # Добавление спрайтов обратно в группу
        elif i.visible() and i in all_sprites:
            # Добавление спрайта на предпоследнее место в группе
            sprites = list(all_sprites.sprites())  # Преобразование группы в список
            sprites.insert(-2, i)  # Вставка нового спрайта на предпоследнее место
            all_sprites.empty()  # Очистка группы
            for sprite in sprites:
                all_sprites.add(sprite)  # Добавление спрайтов обратно в группу
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
    inventory = []
    running = True
    dx, dy = 0, 0

    color = 0

    # Что то непонятное
    fps = 0

    # Какие-то счетчики
    count, ccount, cccount, speccou = 0, 0, 0, 0

    savecords = (0, 0)

    # Заморожена ли речка
    freeze = False

    # Спрайты для анимации
    spFOX, spRiv, spCentralLoc, spBluefor, spHome = [], [], [], [], []
    for x in range(30):
        spFOX.append(pygame.transform.scale(load_image(f"movement/move{x}.PNG"), (dS, dS)))
    for x in range(3):
        spRiv.append(pygame.transform.scale(load_image(f"river/background_river{x}.PNG"), (screen_w, screen_h)))
    for x in range(3):
        spCentralLoc.append(pygame.transform.scale(load_image(f"centralloc/cloc{x}.PNG"), (screen_w, screen_h)))
    for x in range(4):
        spBluefor.append(pygame.transform.scale(load_image(f"bluefor/blf{x}.jpg"), (screen_w, screen_h)))
    for x in range(3):
        spHome.append(pygame.transform.scale(load_image(f"home/home{x}.jpg"), (screen_w, screen_h)))

    return running, isStep, isImpasse, clock, cords, dx, dy, fps, count, ccount, cccount, speccou, spFOX, spRiv, \
           spCentralLoc, spBluefor, spHome, color, freeze, inventory, savecords


# Обработка клика
def event_handling(events, hero, bg_image, objects, pixels, cords, color, cursor, screen_w, screen_h, freeze,
                   all_sprites, inventory, savecords):
    for event in events:
        # Выход из программы при нажатии на крестик
        if event.type == pygame.QUIT:
            return False, cords, bg_image, pixels, color, freeze, inventory, savecords

        # Выход из программы по клавише Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, cords, bg_image, pixels, color, freeze

        if event.type == pygame.MOUSEMOTION:
            if pixels[event.pos] != 0 and pixels[event.pos] != 16777215:
                cursor.image = pygame.transform.scale(load_image('hand.png'), (screen_w * 0.05, screen_h * 0.05))
            else:
                cursor.image = pygame.transform.scale(load_image('cursor.jpg'), (screen_w * 0.05, screen_h * 0.05))
            # изменяем положение спрайта-стрелки
            cursor.rect.topleft = event.pos[0] - 20, event.pos[1] - 10
            for i, item in enumerate(inventory):
                if event.buttons[0] and item.get_cords()[0] <= event.pos[0] <= item.get_cords()[0] + \
                        item.image.get_width() and item.get_cords()[1] <= event.pos[1] <= item.get_cords()[1] + \
                        item.image.get_height():
                    delta = (event.pos[0] - savecords[0], event.pos[1] - savecords[1])
                    item.set_rect(delta[0], delta[1])
                    savecords = event.pos

        # Проверка получения новых координат для героя
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Новые требуемые координаты героя
            hero.need_rotate(event.pos)
            color = pixels[event.pos]
            # Проверяем, можно ли подобрать предмет, если да, то подбираем
            for i in objects:
                # Если объект видно, мышка наведена на объект и герой находится не далеко, объект пропадает с экрана
                if i.pick_up(event.pos, hero.cords, inventory):
                    freeze = True
                i.pick_up(event.pos, hero.cords, inventory)
                i.bg_check(bg_image)
                if i.visible() == False and i in all_sprites:
                    all_sprites.remove(i)
                elif i.visible() == True and i not in all_sprites:
                    # Добавление спрайта на предпоследнее место в группе
                    sprites = list(all_sprites.sprites())  # Преобразование группы в список
                    sprites.insert(-2, i)  # Вставка нового спрайта на предпоследнее место
                    all_sprites.empty()  # Очистка группы
                    for sprite in sprites:
                        all_sprites.add(sprite)  # Добавление спрайтов обратно в группу
                elif i.visible() and i in all_sprites:
                    # Добавление спрайта на предпоследнее место в группе
                    sprites = list(all_sprites.sprites())  # Преобразование группы в список
                    sprites.insert(-2, i)  # Вставка нового спрайта на предпоследнее место
                    all_sprites.empty()  # Очистка группы
                    for sprite in sprites:
                        all_sprites.add(sprite)  # Добавление спрайтов обратно в группу

            if inventory:
                for i, item in enumerate(inventory):
                    item.image = pygame.transform.scale(load_image(item.item_image), (50, 50))
                    item.change_rect((i + 1) * 10 + 50 * i, 10)
                    # Добавление спрайта на предпоследнее место в группе
                    sprites = list(all_sprites.sprites())  # Преобразование группы в список
                    sprites.insert(-2, item)  # Вставка нового спрайта на предпоследнее место
                    all_sprites.empty()  # Очистка группы
                    for sprite in sprites:
                        all_sprites.add(sprite)  # Добавление спрайтов обратно в группу

            return True, event.pos, bg_image, pixels, color, freeze, inventory, savecords
    return True, cords, bg_image, pixels, color, freeze, inventory, savecords


# Меняем фон
def background(hero, bg, bg_image, pixels, screen_w, screen_h, color, freeze, cords):
    # Если нажали на соответствующий цвет выбираем фон
    if color == 66047:
        if freeze:
            bg_image = f"river/background_riverF.PNG"
            bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

            wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_background_river_fr.jpg"),
                                                 (screen_w, screen_h))
            pixels = pygame.PixelArray(wb_bg_image)
        else:
            bg_image = f"river/background_river0.PNG"
            bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

            wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_background_river.jpg"),
                                                 (screen_w, screen_h))
            pixels = pygame.PixelArray(wb_bg_image)

        # Устанавливаем место героя
        hero.change_rect(screen_w * 0.9, screen_h * 0.8)
        cords = screen_w * 0.9, screen_h * 0.8
        # Звук течения реки
        music_play('river')
        pygame.mixer.music.set_volume(0.0)

        return bg_image, pixels, cords

    if color == 254:
        pygame.mixer.music.set_volume(0.1)
        bg_image_past = bg_image
        bg_image = "backgrounds/backg_main.jpg"
        bg.image = pygame.transform.scale(load_image('centralloc/cloc0.PNG'), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_background.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)
        if bg_image_past == 'backgrounds/forest.jpg':
            hero.change_rect(screen_w * 0.4, screen_h * 0.7)
            cords = screen_w * 0.4, screen_h * 0.7
        elif bg_image_past == 'river/background_river0.PNG':
            hero.change_rect(screen_w * 0.05, screen_h * 0.75)
            cords = screen_w * 0.05, screen_h * 0.75
        else:
            hero.change_rect(screen_w * 0.75, screen_h * 0.75)
            cords = screen_w * 0.75, screen_h * 0.75
        # Звук главного меню
        music_play('main')
        pygame.mixer.music.set_volume(0.0)

        return bg_image, pixels, cords

    if color == 65515:
        bg_image = "backgrounds/forest.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_forest.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        hero.change_rect(screen_w * 0.01, screen_h * 0.75)
        cords = screen_w * 0.01, screen_h * 0.75

        # Звук главного меню
        music_play('main')
        pygame.mixer.music.set_volume(0.0)

        return bg_image, pixels, cords

    if color == 130816:
        bg_image = "backgrounds/home.jpg"
        bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))

        wb_bg_image = pygame.transform.scale(load_image("wb_backgrounds/wb_home.jpg"), (screen_w, screen_h))
        pixels = pygame.PixelArray(wb_bg_image)

        hero.change_rect(screen_w * 0.15, screen_h * 0.75)
        cords = screen_w * 0.15, screen_h * 0.75

        # Звук главного меню
        pygame.mixer.music.set_volume(0.0)
        music_play('home')

        return bg_image, pixels, cords
    return bg_image, pixels, cords


# Функция обхода препятствий
def step_handling(screen, bg, bg_image, pixels, cords, hero, all_sprites, barrier, isImpasse, dx, dy, count, ccount,
                  cccount, screen_w, screen_h, color, freeze):
    # Смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем
    if pixels[cords] == 0 and hero.need_step(cords):

        ccount, cccount = update_anim_counters(screen, all_sprites, count, ccount, cccount)
        # Меняем корды героя, если хоть одна отличается от кордов клика

        # Обновляем счетчик на 60
        count += 1
        if 'forest' in bg_image or 'home' in bg_image:
            count += 1
        else:
            count += 1
        if count == 120:
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
    # Если герой пришел к кордам курсора, но изначальный цвет был не 0, меняем фон
    elif not hero.need_step(cords) and color != 0 or (bg_image == "backgrounds/start_menu.jpg" and color == 254):
        bg_image, pixels, cords = background(hero, bg, bg_image, pixels, screen_w, screen_h, color, freeze, cords)
        color = 16777215

    # Если пиксель цветной, идем к верхнему черному пикселю по этому Y
    elif pixels[cords] != 0 and pixels[cords] != 16777215 and cords[1] < screen_h - 1:
        # Ищем верхний черный пиксель данного столбца
        for i in range(screen_h):
            if pixels[cords[0], i] == 0:
                # Задаем новые корды к которым пойдет персонаж
                cords = cords[0], i
                break

    return barrier, isImpasse, dx, dy, count, ccount, cccount, cords, bg_image, pixels, color, freeze


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
    cursor, hero, objects = objects_init(pygame, all_sprites, screen_w, screen_h)

    # Задание значений игровых переменных
    running, barrier, isImpasse, clock, cords, dx, dy, fps, count, ccount, cccount, speccou, spFOX, spRiv, \
    spCentralLoc, spBluefor, spHome, color, freeze, inventory, savecords = game_init(screen, all_sprites, screen_w,
                                                                                     screen_h, objects)

    while running:

        fps = animation(hero, bg, fps, spFOX, spRiv, ccount, bg_image, spCentralLoc, spBluefor,
                        spHome, freeze)

        running, cords, bg_image, pixels, color, freeze, inventory, savecords = event_handling(pygame.event.get(), hero, bg_image, objects,
                                                                         pixels, cords, color, cursor, screen_w,
                                                                         screen_h, freeze,all_sprites, inventory,
                                                                                       savecords)
        barrier, isImpasse, dx, dy, count, ccount, cccount, cords, bg_image, pixels, color, freeze \
            = step_handling(screen, bg, bg_image, pixels, cords, hero, all_sprites, barrier, isImpasse, dx, dy, count,
                            ccount, cccount, screen_w, screen_h, color, freeze)
        game_update(pygame, screen, all_sprites, hero, cords, clock)


def update_anim_counters(screen, all_sprites, count, ccount, cccount):
    # Какие-то действия со счетчиками
    if count % 8 == 0 and count != 0:
        all_sprites.draw(screen)
        ccount += 1
        if ccount == 15 and cccount == 0:
            cccount = 1
            ccount = 0
    return ccount, cccount


def animation(hero, bg, fps, spFOX, spRiv, ccount, bg_image, spCentralLoc, spBluefor, spHome, freeze):
    fps += 1
    if 'background_river' in bg_image and fps % 40 == 0 and not freeze:
        if fps >= 120:
            fps = 0
        bg.image = spRiv[fps // 40]
    if 'forest' in bg_image and fps % 90 == 0:
        if fps >= 270:
            fps = 0
        bg.image = spBluefor[fps // 90]
    if 'home' in bg_image and fps % 100 == 0:
        if fps >= 300:
            fps = 0
        bg.image = spHome[fps // 100]
    if 'backg_main' in bg_image and fps % 120 == 0:
        if fps >= 360:
            fps = 0
        bg.image = spCentralLoc[fps // 120]
    if hero.is_rotate() and 'forest' '''not in bg_image and 'home' not in bg_image''':
        hero.image = spFOX[ccount % len(spFOX)]
    else:
        hero.image = pygame.transform.flip(spFOX[ccount % len(spFOX)], True, False)
    return fps


def music_play(key):
    riversound = pygame.mixer.Sound("core/data/musc/ivsound.wav")
    icesound = pygame.mixer.Sound("core/data/musc/ices.wav")
    homesound = pygame.mixer.Sound("core/data/musc/home.wav")
    if key == 'river':
        homesound.stop()
        icesound.stop()
        riversound.play()
        riversound.set_volume(0.1)
    if key == 'stop':
        homesound.stop()
        homesound.set_volume(0.0)
    if key == 'ice':
        riversound.stop()
        homesound.stop()
        homesound.set_volume(0.0)
    if key == 'main':
        homesound.set_volume(0)
        icesound.stop()
        riversound.stop()
        homesound.set_volume(0.0)
    if key == 'home':
        homesound.play()
        homesound.set_volume(0.15)


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
