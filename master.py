import os
import sys
import pygame

from core.handlers.base import corners


def load_image(name):
    fullname = os.path.join('core/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# класс перса
class Hero:
    def __init__(self):
        self.cords = ()
        # его начальные корды
        self.x = 410
        self.y = 540

    def __call__(self, screen, *args):
        # перерисовываем на новые корды (в args передеём х и у)
        self.x += args[0]
        self.y += args[1]
        pygame.draw.rect(screen, 'red', (self.x, self.y, 100, 150), 8)
        self.cords = (self.x, self.y)

    def get_cords(self):
        return self.cords


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

    all_sprites.draw(screen)

    clock = pygame.time.Clock()
    hero = Hero()
    hero(screen, 0, 0)
    cords = (460, 690)
    x = 1
    y = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                cords = event.pos
        # меняем корды героя если хоть 1 отличается от кордов клика,
        # смотрим, является ли пиксель по цвету в ч\б фоне черным
        if (cords[0] != hero.get_cords()[0] + 50 or cords[1] != hero.get_cords()[1] + 150) and pixels[cords] == 0:
            # ВАЖНО! если после тика корды не поменялись, а мы всё равно прошли через верхнее условие,
            # то наш перс стоит в тупке, ниже код обхода этого тупика
            if x == 0 and y == 0:
                # в corners проверяем различные ситуации, когда ободить надо по разному
                dx, dy = corners(hero.get_cords(), cords)
                hero(screen, 0, dy)
                # идем вниз или вверх до тех пор,
                # пока левый или правый пиксель (в зависимости от dx) не будет черный в ч\б фоне
                while pixels[hero.get_cords()[0] + 50 + dx, hero.get_cords()[1] + 150] != 0:
                    hero(screen, 0, dy)
                hero(screen, dx, 0)

            x = 0
            y = 0
            # узнаем в каком направлении идти по x и y
            if cords[0] > hero.get_cords()[0] + 50 and pixels[hero.get_cords()[0] + 51, hero.get_cords()[1] + 150] == 0:
                x = 1
            if cords[0] < hero.get_cords()[0] + 50 and pixels[hero.get_cords()[0] - 49, hero.get_cords()[1] + 150] == 0:
                x = -1
            if cords[1] > hero.get_cords()[1] + 150 and pixels[
                hero.get_cords()[0] + 50, hero.get_cords()[1] + 151] == 0:
                y = 1
            if cords[1] < hero.get_cords()[1] + 150 and pixels[
                hero.get_cords()[0] + 50, hero.get_cords()[1] + 149] == 0:
                y = -1

            all_sprites.draw(screen)
            hero(screen, x, y)

        clock.tick(150)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
