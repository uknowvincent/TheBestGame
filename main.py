import os
import pygame
import pygame_gui
import sys
import random

pygame.init()

FPS = 50
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
counter_catch = 0


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
    Кл
    """

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.speed = 5
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


def counter_catching():
    global counter_catch
    counter_catch += 1


def first_mini_game():
    font = pygame.font.SysFont('Arial', 24, True)
    text = font.render('ВЫ ПРОИГРАЛИ. ПЕРЕЗАПУСК ИГРЫ.', True, (255, 255, 255))

    class Monster(pygame.sprite.Sprite):
        image = load_image("mountains.png")

        def __init__(self):
            super().__init__(all_sprites)
            self.image = Monster.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.bottom = HEIGHT

    class Food(pygame.sprite.Sprite):
        image = load_image("pt.png")

        def __init__(self, position):
            super().__init__(all_sprites)
            self.counter_catching = 0
            self.image = Food.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = position[0]
            self.rect.y = position[1]

        def update(self):
            if pygame.sprite.collide_mask(self, mountain):
                self.kill()
                counter_catching()
                print(counter_catch)
            if self.rect.y == 560:
                pygame.time.delay(700)
                first_mini_game()
            else:
                self.rect = self.rect.move(0, 2)

    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption('Food Catcher')
        all_sprites = pygame.sprite.Group()
        mountain = Monster()
        fps = 60
        clock = pygame.time.Clock()
        flag = True
        running = True
        counter_spawn = 10
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                mountain.rect.x -= 8
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                mountain.rect.x += 8
            if counter_spawn != -990:
                Food((random.randrange(30, 740), counter_spawn))
                counter_spawn -= 100
            if counter_catch == 10:
                game()
            screen.fill((255, 255, 255))
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(fps)
            pygame.display.flip()
        game()


def run_minigame():
    class Enemy(pygame.sprite.Sprite):
        image = load_image("krovosisya.png")

        def __init__(self, position):
            super().__init__(all_sprites)
            self.counter_catching = 0
            self.image = Enemy.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = position[0]
            self.rect.y = position[1]

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                pygame.time.delay(700)
                run_minigame()
            else:
                self.rect = self.rect.move(3, 0)

    class Player(pygame.sprite.Sprite):
        image = load_image("lizard_dont_go.png")

        def __init__(self):
            super().__init__(all_sprites)
            self.image = Player.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.bottom = HEIGHT

    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption('Food Catcher')
        all_sprites = pygame.sprite.Group()
        player = Player()
        fps = 60
        clock = pygame.time.Clock()
        counter_spawn = -100
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if player.rect.x >= 773:
                    player.rect.x -= 2
                player.rect.x += 2
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if player.rect.x == 0:
                    player.rect.x += 2
                player.rect.x -= 2
            if pygame.key.get_pressed()[pygame.K_UP]:
                if player.rect.y <= 0:
                    player.rect.y += 2
                player.rect.y -= 2
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if player.rect.y == 541:
                    player.rect.y -= 2
                player.rect.y += 2
            print(counter_spawn)
            if counter_spawn >= -1000:
                Enemy((counter_spawn, random.randrange(50, 550, 50)))
                counter_spawn -= 100
            screen.fill((255, 255, 255))
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(fps)
            pygame.display.flip()
        game()


def game():
    class Camera:
        # зададим начальный сдвиг камеры
        def __init__(self):
            self.dx = 0

        # сдвинуть объект obj на смещение камеры
        def apply(self, obj, target):
            if 349 < (target.rect.x % 800) <= 725:
                obj.rect.x -= 2
                target.rect.x -= 2
            elif 348 > (target.rect.x % 800) <= 725:
                obj.rect.x += 2
                target.rect.x += 2

    """
    Основной игровой цикл
    """
    sound = pygame.mixer.Sound(os.path.join('data', 'go_sound.wav'))
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
            ship.rect.x -= ship.speed
            ship.cur_anim = 'left'
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            ship.rect.x += ship.speed
            ship.cur_anim = 'right'
        if -520 >= background.rect.x >= -720 and pygame.key.get_pressed()[pygame.K_SPACE]:
            first_mini_game()
        if -1200 >= background.rect.x >= -1360 and pygame.key.get_pressed()[pygame.K_SPACE]:
            run_minigame()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
        if background.rect.x == 152:
            background.rect.x = 150
        if background.rect.x == -2202:
            background.rect.x = -2200
        if 150 >= background.rect.x >= -2200:
            camera.apply(background, ship)
    pygame.quit()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
start_screen()
