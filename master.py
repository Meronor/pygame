import pygame

from core.handlers.base import corners, screen_init, objects_init, game_init, event_handling, game_update
from core.handlers.items import Hero, Object, Entity
from core.data.constant import tk, dS


def main():
    pygame.init()

    # получаем размер экрана
    # Конфигурация экрана
    screen, pixels, all_sprites, screen_w, screen_h = screen_init(pygame)

    # Получение всех героев в кортеже
    hero, bg, bg_image, objects = objects_init(pygame, screen_w, screen_h)

    # Задание значений игровых переменных
    running, barrier, clock, cords = game_init(screen, hero, bg, all_sprites, objects, screen_w, screen_h)

    while running:
        running, cords, bg_image, pixels = event_handling(pygame.event.get(), hero, bg, bg_image, pixels, cords,
                                                          screen_w, screen_h)

        # смотрим, является ли пиксель по цвету в ч\б фоне черным (равен 0), иначе ничего не делаем
        if pixels[cords] == 0 and hero.need_step(cords):
            # меняем корды героя, если хоть одна отличается от кордов клика

            # проверяем, обходит ли герой в данный момент препятствие
            if barrier:
                # делаем шаг
                isImpasse = hero.next_step(cords, pixels)

            # ВАЖНО! если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
            # то наш перс стоит в тупике, ниже код обхода этого тупика
            if isImpasse:
                # если barrier = False, наш герой уже обходит препятствие
                if barrier:
                    # в corners проверяем различные ситуации, когда обходить надо по разному
                    dx, dy = corners((hero.centralX(), hero.centralY()), cords)

                # меняем корды героя на dx, dy, если возвращается True, мы обошли прпятствие,
                # иначе повторяем код со следующим тиком
                barrier = hero.overcome_step(pixels, dx, dy)

        game_update(pygame, screen,all_sprites, hero, cords, clock)

    pygame.quit()


if __name__ == '__main__':
    main()
