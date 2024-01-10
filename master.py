import pygame

from core.handlers.base import corners, screen_init, objects_init, game_init, event_handling, game_update, step_handling


def main():
    pygame.init()

    # получаем размер экрана
    # Конфигурация экрана
    screen, pixels, all_sprites, screen_w, screen_h = screen_init(pygame)

    # Получение всех героев в кортеже
    hero, bg, bg_image, objects = objects_init(pygame, screen_w, screen_h)

    # Задание значений игровых переменных
    running, barrier, isImpasse, clock, cords, dx, dy = \
        game_init(screen, hero, bg, all_sprites, objects, screen_w, screen_h)

    while running:
        running, cords, bg_image, pixels = event_handling(pygame.event.get(), hero, bg, bg_image, pixels, cords,
                                                          screen_w, screen_h)
        barrier, isImpasse, dx, dy = step_handling(pixels, cords, hero, barrier, isImpasse, dx, dy)

        game_update(pygame, screen, all_sprites, hero, cords, clock)

    pygame.quit()


if __name__ == '__main__':
    main()
