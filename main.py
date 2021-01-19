import os
import pygame
import pygame_gui
import sys
import random

pygame.mixer.pre_init()
pygame.init()
FPS = 50
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
counter_catch = 0
counter_krovo_kill = 0


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
        relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 3 + 55), (150, 50)),
        text='Начать игру',
        manager=manager
    )
    exit_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 100), (150, 50)),
        text='Выход',
        manager=manager
    )
    back = load_image('legend_start.png')
    screen.blit(back, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_btn:
                        end_game()
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


def counter_krovosisya():
    global counter_krovo_kill
    counter_krovo_kill += 1


def first_mini_game():
    class Monster(pygame.sprite.Sprite):

        image = load_image("monster.png")

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
            self.image = Food.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = position[0]
            self.rect.y = position[1]

        def update(self):
            if pygame.sprite.collide_mask(self, monster):
                self.kill()
                counter_catching()
            if self.rect.y == 560:
                pygame.time.delay(500)
                pygame.time.delay(700)
                first_mini_game()
            else:
                self.rect = self.rect.move(0, 2)

    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption('Food Catcher')
        legend_start = pygame.sprite.Sprite(first_minigame_sprites)
        legend_start.image = load_image('first_minigame.png')
        legend_start.rect = legend_start.image.get_rect()
        all_sprites = pygame.sprite.Group()
        monster = Monster()
        fps = 60
        clock = pygame.time.Clock()
        running = True
        counter_spawn = 10
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                monster.rect.x -= 8
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                monster.rect.x += 8
            if counter_spawn != -990:
                Food((random.randrange(30, 740), counter_spawn))
                counter_spawn -= 100
            if counter_catch == 10:
                continue_game()
            screen.fill((255, 255, 255))
            first_minigame_sprites.draw(screen)
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(fps)
            pygame.display.flip()
        continue_game()


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
            elif self.rect.x >= 850:
                self.kill()
                counter_krovosisya()
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
                player.rect.x += 4
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if player.rect.x <= 0:
                    player.rect.x += 2
                player.rect.x -= 4
            if pygame.key.get_pressed()[pygame.K_UP]:
                if player.rect.y <= 0:
                    player.rect.y += 2
                player.rect.y -= 4
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if player.rect.y >= 541:
                    player.rect.y -= 2
                player.rect.y += 4
            if counter_spawn >= -1000:
                Enemy((counter_spawn, random.randrange(50, 550, 50)))
                counter_spawn -= 50
            if counter_krovo_kill == 19:
                game()
            screen.fill((255, 255, 255))
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(fps)
            pygame.display.flip()
        game()


def print_text(text, coords=(20, 517), color=(0, 100, 50), size=30):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    screen.blit(text, coords)
    pygame.display.update()


def clear_sf_from_text():
    s = pygame.Surface((800, 90), pygame.SRCALPHA)
    s.set_alpha(255)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 510))


def elder_dialogue():
    clear_sf_from_text()
    print_text('- Так ты попал сюда, сынок...')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('Это говорил лизард, чьи глаза были завешаны вековыми морщинами.')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Мы все надеемся на тебя и твою доблесть')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Будь смел и неси своё бремя с честью')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Смотри только гордо вперёд и не останавливайся')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Предание гласит о роще, где пасутся опасные звери.')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Их называют красношмыги...')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Оседлав его ты сможешь догнать духа - АЮ')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('Достав из мантии пожелтевшую от времени бумажку,')
    print_text('он начал водить по ней костлявым пальцем', (20, 537))
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- На этом болоте несколько сотен лет назад')
    print_text('был похоронен великий лизард Святошкур,', (20, 537))
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Отправляйся в те болота на борьбу с комариной ордой')
    print_text('Получив этот меч, ты обретёшь силу,', (20, 537))
    print_text('необходимую для победы над духом', (20, 560))
    pygame.time.delay(4500)
    clear_sf_from_text()


def forest_owner_dialogue():
    clear_sf_from_text()
    print_text('- О, заходи быстрее ко мне, а то так и пришкваришся к дороге.')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Попей холодного морса, и расскажи быстрее,')
    print_text('как тот самый жёлтый лизард попал в эти края...', (20, 537))
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Ты искал ту загадочную рощу?')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Красношмыг?')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Моя бабка рассказывала в детстве о них сказки.')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Будто на деревьях там жирееют личинки огромных размеров...')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('-  А красношмыги их пожирают')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('-  Возможно тебе удастся его приручить, накормив его...')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Пойдем скорее в дом.')
    pygame.time.delay(3500)
    clear_sf_from_text()
    print_text('- Я отведу тебя к красношмыгу через задние ворота.')
    pygame.time.delay(3500)


def legend_telling():
    # если не хотите при проверке смотреть легенду, измените переменную
    # legend_telling_flag в игровом цикле на False
    start_legend_sprites.draw(screen)
    print_text('На протяжении сотен лет народ лизардов жил в мире и гармонии,', (50, 100))
    pygame.time.delay(3500)
    print_text('вкушая лучшие плоды с их земель, танцуя по вечерам,', (50, 150))
    pygame.time.delay(3500)
    print_text('не зная горя и печали.', (50, 200))
    pygame.time.delay(3500)
    print_text('Но в один  ужасный день...', (50, 250))
    pygame.time.delay(3500)
    print_text('Пробудился злой дух - "АЮ", и стал сеять хаос на земле лизардов,', (50, 300))
    pygame.time.delay(3500)
    print_text('сжигая их посевы и разрушая дома.', (50, 350))
    pygame.time.delay(3500)
    start_legend_sprites.draw(screen)
    print_text('Народ лизардов решил созвать Великое собрание старейшин,', (50, 100))
    pygame.time.delay(3500)
    print_text('чтобы справиться с напастью духа - "АЮ".', (50, 150))
    pygame.time.delay(3500)
    print_text('Со всех поселений лизардов собирались мудрецы.', (50, 200))
    pygame.time.delay(3500)
    print_text('Они приходили к дому главного старейшины, дабы найти спасение.', (50, 250))
    pygame.time.delay(3500)
    print_text('Закопавшись в свитки древних пророчеств, они кое-что узнали.', (50, 300))
    pygame.time.delay(3500)
    print_text('Узнали о знаменосном жёлтом лизарде...', (50, 350))
    pygame.time.delay(3500)
    print_text('способном принести мир в их земли вновь.', (50, 400))
    pygame.time.delay(3500)
    start_legend_sprites.draw(screen)
    print_text('ВЫ - Наша последняя надежда', (40, 300), (0, 200, 0), 60)
    pygame.time.delay(3500)


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
    legend_start = pygame.sprite.Sprite(start_legend_sprites)
    legend_start.image = load_image('legend_start.png')
    legend_start.rect = legend_start.image.get_rect()
    background = pygame.sprite.Sprite(all_sprites)
    background.image = load_image('background.png')
    background.rect = background.image.get_rect()
    ship = Ship(load_image("lizard_go.png"), 13, 1, 350, 442)
    legend_telling_flag = False
    lesnik_event = True
    krovosisya_event = True
    krasnoshmig_event = True
    elder_event = True
    running = True
    flag_go = False
    while running:
        if legend_telling_flag:
            legend_telling()
            legend_telling_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        ship.cur_anim = 'straight'
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            flag_go = True
            ship.rect.x -= ship.speed
            ship.cur_anim = 'left'
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            flag_go = True
            ship.rect.x += ship.speed
            ship.cur_anim = 'right'
        if flag_go:
            flag_go = False
            sound.play()
        else:
            sound.stop()
        all_sprites.draw(screen)
        all_sprites.update()
        if -36 >= background.rect.x >= -82 and not pygame.key.get_pressed()[pygame.K_e]:
            clear_sf_from_text()
            print_text('Нажмите Е, чтобы заговорить со старейшиной.')
        if -444 >= background.rect.x >= -496 and not pygame.key.get_pressed()[pygame.K_e] and not elder_event:
            clear_sf_from_text()
            print_text('Нажмите Е, чтобы заговорить с лесником.')
        if pygame.key.get_pressed()[pygame.K_e] and -36 >= background.rect.x >= -82:
            elder_dialogue()
            elder_event = False
        if -444 >= background.rect.x >= -496 and pygame.key.get_pressed()[pygame.K_e] and not elder_event:
            forest_owner_dialogue()
            lesnik_event = False
        if -520 >= background.rect.x >= -720 and not pygame.key.get_pressed()[pygame.K_SPACE] and not lesnik_event:
            clear_sf_from_text()
            print_text('Нажмите пробел, чтобы пойти с лесником к красношмыгу')
        if -520 >= background.rect.x >= -720 and pygame.key.get_pressed()[pygame.K_SPACE]:
            first_mini_game()
            krasnoshmig_event = False
        #print(krovosisya_event)
        if not krovosisya_event and 50 >= background.rect.x >= -200:
            clear_sf_from_text()
            print_text('Отправляйтесь на битву с АЮ')
        pygame.display.flip()
        clock.tick(FPS)
        #print(background.rect.x)
        if background.rect.x == 152:
            background.rect.x = 150
        if background.rect.x == -2202:
            background.rect.x = -2200
        if 150 >= background.rect.x >= -2200:
            camera.apply(background, ship)
    pygame.quit()


def continue_game():
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
    Игровой цикл после первого испытания
    """

    sound = pygame.mixer.Sound(os.path.join('data', 'go_sound.wav'))
    camera = Camera()
    background = pygame.sprite.Sprite(all_sprites)
    background.image = load_image('background.png')
    background.rect = background.image.get_rect()
    ship = Ship(load_image("lizard_go.png"), 13, 1, 350, 442)
    krovosisya_event = True
    running = True
    flag_go = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        ship.cur_anim = 'straight'
        print(background.rect.x)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            flag_go = True
            ship.rect.x -= ship.speed
            ship.cur_anim = 'left'
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            flag_go = True
            ship.rect.x += ship.speed
            ship.cur_anim = 'right'
        if flag_go:
            flag_go = False
            sound.play(-1)
        else:
            sound.stop()
        if -1200 >= background.rect.x >= -1350 and pygame.key.get_pressed()[pygame.K_SPACE]:
            run_minigame()
            krovosisya_event = False
        all_sprites.draw(screen)
        all_sprites.update()
        if -36 >= background.rect.x >= -82 and not pygame.key.get_pressed()[pygame.K_e]:
            clear_sf_from_text()
            print_text('Нажмите Е, чтобы заговорить со старейшиной.')
        if -1200 >= background.rect.x >= -1350 and not pygame.key.get_pressed()[pygame.K_SPACE]:
            clear_sf_from_text()
            print_text('Нажмите пробел, чтобы пойти на комариные топи.')
        if -444 >= background.rect.x >= -496 and not pygame.key.get_pressed()[pygame.K_e]:
            clear_sf_from_text()
            print_text('Лесник уже вам помог')
        if pygame.key.get_pressed()[pygame.K_e] and -36 >= background.rect.x >= -82:
            elder_dialogue()
            elder_event = False
        if -520 >= background.rect.x >= -720 and not pygame.key.get_pressed()[pygame.K_SPACE]:
            clear_sf_from_text()
            print_text('Вы уже оседлали красношмыга')
        print(krovosisya_event)
        if not krovosisya_event and 50 >= background.rect.x >= -200:
            clear_sf_from_text()
            print_text('Отправляйтесь на битву с АЮ')
        pygame.display.flip()
        clock.tick(FPS)
        print(background.rect.x)
        if background.rect.x == 152:
            background.rect.x = 150
        if background.rect.x == -2202:
            background.rect.x = -2200
        if 150 >= background.rect.x >= -2200:
            camera.apply(background, ship)
    pygame.quit()


def end_game():
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
    Игровой цикл после первого испытания
    """

    sound = pygame.mixer.Sound(os.path.join('data', 'go_sound.wav'))
    camera = Camera()
    background = pygame.sprite.Sprite(all_sprites)
    background.image = load_image('background.png')
    background.rect = background.image.get_rect()
    ship = Ship(load_image("lizard_go.png"), 13, 1, 350, 442)
    krovosisya_event = True
    running = True
    flag_go = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
        ship.cur_anim = 'straight'
        print(background.rect.x)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            flag_go = True
            ship.rect.x -= ship.speed
            ship.cur_anim = 'left'
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            flag_go = True
            ship.rect.x += ship.speed
            ship.cur_anim = 'right'
        if flag_go:
            flag_go = False
            sound.play(-1)
        else:
            sound.stop()
        if -1944 >= background.rect.x >= -2200 and not pygame.key.get_pressed()[pygame.K_SPACE]:
            background = pygame.sprite.Sprite(end_game_sprites)
            background.image = load_image('final_background.png')
            background.rect = background.image.get_rect()
            end_game_sprites.draw(screen)
            end_game_sprites.update()
        all_sprites.draw(screen)
        all_sprites.update()
        if -1944 >= background.rect.x >= -2200 and not pygame.key.get_pressed()[pygame.K_e]:
            clear_sf_from_text()
            print_text('Нажмите Е, чтобы войти в пещеру.')
        print(krovosisya_event)
        if  50 >= background.rect.x >= -200:
            clear_sf_from_text()
            print_text('Отправляйтесь на битву с АЮ')
        pygame.display.flip()
        clock.tick(FPS)
        print(background.rect.x)
        if background.rect.x == 152:
            background.rect.x = 150
        if background.rect.x == -2202:
            background.rect.x = -2200
        if 150 >= background.rect.x >= -2200:
            camera.apply(background, ship)
    pygame.quit()

# clear_sf_from_text()
#             print_text('Вы уже оседлали красношмыга')
all_sprites = pygame.sprite.Group()
start_legend_sprites = pygame.sprite.Group()
first_minigame_sprites = pygame.sprite.Group()
end_game_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
start_screen()
