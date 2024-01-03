import pygame

from core.handlers.base import corners, load_image
from core.handlers.items import Hero, Entity


def main():
    pygame.init()

    # получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    # растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()

    # получаем и растягиваем картинку на весь экран
    image1 = load_image("backround.jpg")
    bg_image = pygame.transform.scale(image1, (screen_w, screen_h))
    bg = pygame.sprite.Sprite(all_sprites)
    bg.image = bg_image
    bg.rect = bg.image.get_rect()
    bg.rect.x, bg.rect.y = 0, 0

    # растянутый задний фон в ч/б (границы ходьбы)
    image2 = load_image("wb_backround.jpg")
    wb_bg_image = pygame.transform.scale(image2, (screen_w, screen_h))
    pixels = pygame.PixelArray(wb_bg_image)

    clock = pygame.time.Clock()

    hero = Hero()
    hero_image = load_image("hero.jpg")
    hero.image = hero_image
    hero.rect = hero.image.get_rect()
    hero.image = pygame.transform.scale(hero_image, (175, 175))
    hero.rect.x, hero.rect.y = screen_w * 0.75, screen_h * 0.75
    all_sprites.add(hero)

    items = Entity()
    item_image = load_image("i.jpg")
    items.image = item_image
    items.rect = items.image.get_rect()
    items.image = pygame.transform.scale(item_image, (100, 100))
    items.rect.x, items.rect.y = 250, 250
    all_sprites.add(items)

    all_sprites.draw(screen)
    fd = True
    cords = (460, 490)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
                if hero.rect.x + 75 < cords[0] and hero.is_rotate():
                    hero.image = pygame.transform.flip(hero.image, True, False)
                    hero.rotate()
                if hero.rect.x + 75 > cords[0] and not hero.is_rotate():
                    hero.image = pygame.transform.flip(hero.image, True, False)
                    hero.rotate()


        # меняем корды героя если хоть 1 отличается от кордов клика,
        # смотрим, является ли пиксель по цвету в ч\б фоне черным
        if (cords[0] != hero.rect.x + 75 or cords[1] != hero.rect.y + 165) and pixels[cords] == 0:
            x = 0
            y = 0
            # узнаем в каком направлении идти по x и y
            if cords[0] > hero.rect.x + 75 and pixels[hero.rect.x + 75 + 1, hero.rect.y + 165] == 0 and fd:
                x = 1
            elif cords[0] < hero.rect.x + 75 and pixels[hero.rect.x + 75 - 1, hero.rect.y + 165] == 0 and fd:
                x = -1
            if cords[1] > hero.rect.y + 165 and pixels[hero.rect.x + 75, hero.rect.y + 166] == 0 and fd:
                y = 1
            elif cords[1] < hero.rect.y + 165 and pixels[hero.rect.x + 75, hero.rect.y + 165 - 1] == 0 and fd:
                print(cords, (hero.rect.x + 75, hero.rect.y + 165))
                y = -1

        if (cords[0] != hero.rect.x + 75 or cords[1] != hero.rect.y + 165) and pixels[(cords[0], cords[1] - 30)] == 0:
            x = 0
            y = 0
            # узнаем в каком направлении идти по x и y
            if cords[0] > hero.rect.x + 75 and pixels[hero.rect.x + 75 + 1, hero.rect.y + 165] == 0 and fd:
                x = 1
            elif cords[0] < hero.rect.x + 75 and pixels[hero.rect.x + 75 - 1, hero.rect.y + 165] == 0 and fd:
                x = -1
            if cords[1] > hero.rect.y + 165 and pixels[hero.rect.x + 75, hero.rect.y + 166] == 0 and fd:
                y = 1
            elif cords[1] < hero.rect.y + 165 and pixels[hero.rect.x + 75, hero.rect.y + 165 - 1] == 0 and fd:
                print(cords, (hero.rect.x + 75, hero.rect.y + 165))
                y = -1


            hero.rect.x += x
            hero.rect.y += y

            # ВАЖНО! если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
            # то наш перс стоит в тупике, ниже код обхода этого тупика

            if x == 0 and y == 0:
                print(cords, (hero.rect.x + 75, hero.rect.y + 165))
                # в corners проверяем различные ситуации, когда ободить надо по разному
                if fd:
                    dx, dy = corners((hero.rect.x + 75, hero.rect.y + 165), cords)
                # идем вниз или вверх до тех пор,
                # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне
                if pixels[hero.rect.x + 75 + dx, hero.rect.y + 165] != 0:
                    hero.rect.y += 1
                    fd = False
                else:
                    fd = True
        all_sprites.draw(screen)

        clock.tick(150)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
