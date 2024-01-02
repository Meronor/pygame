import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class sqr:
    def __init__(self):
        self.cords = ()
        self.x = 410
        self.y = 540

    def __call__(self, screen, *args, **kwargs):
        self.x += args[0]
        self.y += args[1]
        pygame.draw.rect(screen, 'red',(self.x, self.y, 100, 150), 8)
        self.cords = (self.x, self.y)

    def get_cords(self):
        return self.cords




def main():
    pygame.init()

    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Game')

    all_sprites = pygame.sprite.Group()

    image1 = load_image("backround.jpg")
    bg_image = pygame.transform.scale(image1, (screen_w, screen_h))
    hero = pygame.sprite.Sprite(all_sprites)
    hero.image = bg_image
    hero.rect = hero.image.get_rect()
    hero.rect.x, hero.rect.y = 0, 0

    image2 = load_image("wb_backround.jpg")
    wb_bg_image = pygame.transform.scale(image2, (screen_w, screen_h))
    pixels = pygame.PixelArray(wb_bg_image)

    all_sprites.draw(screen)

    clock = pygame.time.Clock()
    obj = sqr()
    obj(screen, 0, 0)
    cords = (460, 690)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and pixels[event.pos] == 0:
                cords = event.pos

        if cords[0] != obj.get_cords()[0] + 50 or cords[1] != obj.get_cords()[1] + 150:
            x = 0
            y = 0
            if cords[0] > obj.get_cords()[0] + 50:
                x = 1
            if cords[0] < obj.get_cords()[0] + 50:
                x = -1
            if cords[1] > obj.get_cords()[1] + 150:
                y = 1
            if cords[1] < obj.get_cords()[1] + 150:
                y = -1
            all_sprites.draw(screen)
            obj(screen, x, y)

        clock.tick(150)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
