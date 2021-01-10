import os
import pygame
import pygame_gui
import sys

pygame.init()

FPS = 50
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Ship(pygame.sprite.Sprite):
    """
    Класс корабля
    """
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.speed = 2
        self.tick = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_anim = 'straight'
        self.cur_frame = 1
        self.image = self.frames[4]
        self.animations = {'straight': 6, 'left': [5, 4, 3, 2, 1, 0], 'right': [7, 8, 9, 10, 11, 12]}
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.rotate(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size)), 0))

    def update(self):
        if self.cur_anim == 'straight':
            self.cur_frame = self.animations['straight']
            self.tick = 0
        if self.cur_anim == 'left':
            if self.tick > 1 and self.cur_frame < 7:
                self.cur_frame -= 1
                self.tick = 0
                if self.cur_frame == 0:
                    self.cur_frame = 5
        if self.cur_anim == 'right':
            if self.tick > 1 and self.cur_frame > 1:
                self.cur_frame += 1
                self.tick = 0
                if self.cur_frame == 12:
                    self.cur_frame = 7
        self.image = self.frames[self.cur_frame]
        self.tick = self.tick + 1


def terminate():
    """
    Прерывание игры
    """
    pygame.quit()
    sys.exit()


def start_screen():
    """
    Начальная заставка с кнопками
    """
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), os.path.join('data', 'menu_theme.json'))
    # Кнопки
    start_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 3 - 25), (150, 50)),
        text='Начать игру',
        manager=manager
    )
    savings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 - 25), (150, 50)),
        text='Сохранения',
        manager=manager
    )
    exit_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 125), (150, 50)),
        text='Выход',
        manager=manager
    )
    back = load_image('start_fon.jpg')
    screen.blit(back, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_btn:
                        game()
                    if event.ui_element == exit_btn:
                        terminate()
            manager.process_events(event)
        manager.update(FPS / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def game():
    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 0

        # сдвинуть объект obj на смещение камеры
        def apply(self, obj, target):
            if 800 - (target.rect.x % 800) < 75 and 75 < target.rect.x - 75 < 3000:
                    obj.rect.x -= 5
                    target.rect.x -= 3
            if 800 - (target.rect.x % 800) < 75 and 75 < target.rect.x < 3000:
                    obj.rect.x += 5
                    target.rect.x += 3
            print(target.rect.x, obj.rect.x)


    """
    Основной игровой цикл
    """
    camera = Camera()
    background = pygame.sprite.Sprite(all_sprites)
    background.image = load_image('background.png')
    background.rect = background.image.get_rect()
    ship = Ship(load_image("lizard_go.png"), 13, 1, 350, 442)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        ship.cur_anim = 'straight'
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if -2470 < background.rect.x <= 0:
                ship.rect.x -= ship.speed
                ship.cur_anim = 'left'
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if -2475 <= background.rect.x <= 0:
                ship.rect.x += ship.speed
                ship.cur_anim = 'right'
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
        camera.apply(background, ship)
    pygame.quit()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
start_screen()
