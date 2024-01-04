import pygame

from core.handlers.base import corners, load_image
from core.handlers.items import Hero, Object, Entity
from core.data.constant import tk, hX, hY, dS


def main():
    pygame.init()

    # получаем размер экрана
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    # растягиваем окно во весь экран
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()

    # получаем и растягиваем картинку на весь экран
    bg = Object()
    bg.image = pygame.transform.scale(load_image("backround.jpg"), (screen_w, screen_h))
    bg.rect = bg.image.get_rect()
    bg.set_rect(hX, hY)

    # растянутый задний фон в ч/б (границы ходьбы)
    wb_bg_image = pygame.transform.scale(load_image("wb_backround.jpg"), (screen_w, screen_h))
    pixels = pygame.PixelArray(wb_bg_image)

    clock = pygame.time.Clock()

    hero = Hero()
    hero.rect = hero.image.get_rect()
    hero.image = pygame.transform.scale(load_image("hero.jpg"), (dS, dS))
    hero.rect.x, hero.rect.y = screen_w * 0.75, screen_h * 0.75

    items = Entity()
    item_image = load_image("i.jpg")
    items.image = item_image
    items.rect = items.image.get_rect()
    items.image = pygame.transform.scale(item_image, (100, 100))
    items.rect.x, items.rect.y = 250, 250

    all_sprites.add(bg)
    all_sprites.add(hero)
    all_sprites.add(items)

    all_sprites.draw(screen)
    # fd = False - маркер того, что требуется обход препятствия (текущая пиксела не валидная)
    fd = True
    # задаем "первый клик"
    cords = (hX, hY)
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

                # проверка необходимости перевернуть героя
                if hero.centralX() < cords[0] and hero.is_rotate():
                    hero.image = pygame.transform.flip(hero.image, True, False)
                    hero.rotate()
                if hero.centralX() > cords[0] and not hero.is_rotate():
                    hero.image = pygame.transform.flip(hero.image, True, False)
                    hero.rotate()

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
