import pygame

from core.handlers.base import game


def main():
    # Конфигурация игрового движка
    pygame.init()
    # Игровой цикл
    game(pygame)
    # Выход из приложения
    pygame.quit()


if __name__ == '__main__':
    main()
