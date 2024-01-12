import pygame

from core.handlers.base import corners, load_image
from core.handlers.items import Hero, Object, Entity
from core.data.constant import tk, dS


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
    bg = Object()
    bg_image = "backround.jpg"
    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
    bg.rect = bg.image.get_rect()
    bg.set_rect(0, 0)

    # растянутый задний фон в ч/б (границы ходьбы)
    wb_bg_image = pygame.transform.scale(load_image("wb_backround.jpg"), (screen_w, screen_h))
    pixels = pygame.PixelArray(wb_bg_image)

    clock = pygame.time.Clock()

    hero = Hero()
    hero.image = pygame.transform.scale(load_image("hero.jpg"), (dS, dS))
    hero.rect = hero.image.get_rect()
    hero.set_rect(screen_w * 0.75, screen_h * 0.75)

    items = Entity(250, 750, True, 'backround.jpg')
    items.image = pygame.transform.scale(load_image("i.jpg"), (100, 100))
    items.rect = items.image.get_rect()
    items.set_rect(250, 750)

    all_sprites.add(bg)
    all_sprites.add(hero)
    all_sprites.add(items)

    all_sprites.draw(screen)
    # fd = False - маркер того, что требуется обход препятствия (текущая пиксела не валидная)
    fd = True
    # задаем "первый клик"
    cords = (screen_w * 0.75, screen_h * 0.75)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # выход из программы по клавише Esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # задаем корды, к который пойдет герой
                cords = event.pos
                if (pixels[cords] == 254 and hero.get_cords()[0] < screen_w * 0.2 and
                        bg_image != "background_river.jpg"):
                    bg_image = "background_river.jpg"
                    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
                    wb_bg_image = pygame.transform.scale(load_image("wb_background_river.jpg"), (screen_w, screen_h))
                    pixels = pygame.PixelArray(wb_bg_image)
                    hero.change_rect(screen_w * 0.85, screen_h * 0.75)
                if (pixels[cords] == 254 and hero.get_cords()[0] > screen_w * 0.7 and
                        bg_image != "backround.jpg"):
                    bg_image = "backround.jpg"
                    bg.image = pygame.transform.scale(load_image(bg_image), (screen_w, screen_h))
                    wb_bg_image = pygame.transform.scale(load_image("wb_backround.jpg"), (screen_w, screen_h))
                    pixels = pygame.PixelArray(wb_bg_image)
                    hero.change_rect(screen_w * 0.01, screen_h * 0.75)
                # при необходимости переворачиваем героя
                hero.need_rotate(cords)

                # проверяем, можно ли подобрать предмет, если да, то подбираем
                items.pick_up(pygame.mouse.get_pos(), hero.get_cords())
                items.bg_check(bg_image)
                if items.visible() == False and items in all_sprites:
                    all_sprites.remove(items)
                elif items.visible() == True and items not in all_sprites:
                    all_sprites.add(items)
                elif items.visible() and items in all_sprites:
                    all_sprites.add(items)

        # смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем
        if pixels[cords] == 0:
            # меняем корды героя, если хоть одна отличается от кордов клика
            if hero.need_step(cords):
                x, y = 0, 0

                # проверяем, обходит ли герой в данный момент препятствие
                if fd:
                    # делаем шаг
                    x, y = hero.next_step(cords, pixels)

                # ВАЖНО! если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
                # то наш перс стоит в тупике, ниже код обхода этого тупика
                if x == 0 and y == 0:
                    # если fd = False, наш герой уже обходит препятствие
                    if fd:
                        # в corners проверяем различные ситуации, когда обходить надо по разному
                        dx, dy = corners((hero.centralX(), hero.centralY()), cords)

                    # меняем корды героя на dx, dy, если возвращается True, мы обошли прпятствие,
                    # иначе повторяем код со следующим тиком
                    fd = hero.overcome_step(pixels, dx, dy)

        all_sprites.draw(screen)

        clock.tick(tk)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
