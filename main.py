import pygame
from settings import *
from random import randint
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#створення вікна гри
W, H = 1000, 800
FPS = 60
BLOCK_SIZE = 50
YELLOW = (255, 225, 117)
window = pygame.display.set_mode((W, H))
background = pygame.image.load('images\\menu_back.png')
background = pygame.transform.scale(background, (W, H))
pygame.display.set_caption('Лабиринт')

def game(MAP):
    #аналіз карти
    walls = []
    acids = []
    spikes = []
    for block_y, row in enumerate(MAP):
        for block_x, element in enumerate(row):
            if element == 'x':
                wall = Wall(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, 'images\\wall.png')
                walls.append(wall)
            elif element == 'o':
                acid = Acid(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, 'images\\acid_frames\\')
                acids.append(acid)
            elif element == '1':
                player = Player(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, 2, 'images\\player')
            elif element == 's':
                spike = Spike(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, 'images\\spike_frames')
                spikes.append(spike)
            elif element == 'f':
                flag = Flag(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, 'images\\flag_frames\\')

    #звукові ефекти
    pygame.mixer.music.load('sounds\\back.ogg')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    snd_run = pygame.mixer.Sound('sounds\\run.wav')
    snd_damage = pygame.mixer.Sound('sounds\\damage.ogg')
    pygame.mixer.set_num_channels(1)
    clock = pygame.time.Clock()

    #ігровий цикл
    game = True
    while game:
        window.fill(YELLOW)
        player.status = 'still'
        player.speed = 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()

        for acid in acids:
            window.blit(acid.image, acid.rect)
            acid.update(0.1)
            if player.collideobject(acid):
                player.speed = 1
                if pygame.time.get_ticks() - player.last_damage > 500:
                    pygame.mixer.stop()
                    snd_damage.play()
                    player.health -= 1
                    player.last_damage = pygame.time.get_ticks()

        #обробка натискань по клавіатурі  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.rect.y -= player.speed
            player.direction = 'up'
            player.status = 'run'
        elif keys[pygame.K_s]:
            player.rect.y += player.speed
            player.direction = 'down'
            player.status = 'run' 
        elif keys[pygame.K_a]:
            player.rect.x -= player.speed
            player.direction = 'left'
            player.status = 'run'   
        elif keys[pygame.K_d]:
            player.rect.x += player.speed
            player.direction = 'right'
            player.status = 'run'
        elif keys[pygame.K_ESCAPE]:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            game = False

        for wall in walls:
            window.blit(wall.image, wall.rect)
            if player.collideobject(wall):
                player.step_back()
                player.status = 'still'

        for spike in spikes:
            window.blit(spike.image, spike.rect)
            spike.update()
            if spike.is_up():
                if player.collideobject(spike):
                    player.step_back()
                    player.status = 'still'
                    if pygame.time.get_ticks() - player.last_damage > 500:
                        pygame.mixer.stop()
                        snd_damage.play()
                        player.health -= 1
                        player.last_damage = pygame.time.get_ticks()

        player.update_frame()
        player.update_image()

        if player.status == 'run':
            snd_run.play()
        else:
            snd_run.stop()

        if player.health <= 0:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            return 'lose'

        if player.collideobject(flag):
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            return 'win'

        flag.update(window, 0.1)
        window.blit(player.image, player.rect)
        player.draw_hp(window)
        clock.tick(FPS)
        pygame.display.update()

def manage_screen(text):
    btns = []
    if text == 'Ви перемогли!':
        btn_action = Button(150, 300, 700, 100, (255, 255, 255), (170, 170, 170), (0,0,0), 80, 'Наступна карта')
        btns.append(btn_action)
        font = pygame.font.SysFont('arial', 50, 1)
        txt = font.render(text, True, (23, 255, 108))
    elif text == 'Ви пройшли гру!':
        btn_action = Button(100, 300, 800, 100, (255, 255, 255), (170, 170, 170), (0,0,0), 80, 'Карт більше немає')
        btns.append(btn_action)
        font = pygame.font.SysFont('arial', 50, 1)
        txt = font.render(text, True, (23, 255, 108))
    else:
        btn_action = Button(100, 300, 800, 100, (255, 255, 255), (170, 170, 170), (0,0,0), 80, 'Спробувати знову')
        btns.append(btn_action)
        font = pygame.font.SysFont('arial', 50, 1)
        txt = font.render(text, True, (255, 91, 91))

    btn_exit = Button(150, 600, 700, 100, (255, 255, 255), (170, 170, 170), (200, 10, 10), 80, 'Вийти в меню')
    btns.append(btn_exit)

    clock = pygame.time.Clock()
    run = True
    while run:
        window.fill((0,0,0))
        mouse_pos = pygame.mouse.get_pos()
        for btn in btns:
            btn.draw(window)
            if btn.rect.collidepoint(mouse_pos):
                btn.choose(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_action.rect.collidepoint(mouse_pos):
                        snd_btn_click.play()
                        return True

                    elif btn_exit.rect.collidepoint(mouse_pos):
                        snd_btn_click.play()
                        run = False

        window.blit(txt, (350, 100))
        pygame.display.update()
        clock.tick(60)
    return False

#кнопки
btns = []
btn_game = Button(200, 300, 600, 100, (255, 255, 255), (170, 170, 170), (0,0,0), 80, 'Почати гру')
btn_exit = Button(300, 600, 400, 100, (255, 255, 255), (170, 170, 170), (200, 10, 10), 80, 'Вийти')
btns.append(btn_game)
btns.append(btn_exit)

#звукові ефекти
snd_btn_click = pygame.mixer.Sound('sounds\\btn_click.ogg')
snd_lose = pygame.mixer.Sound('sounds\\lose.ogg')
snd_win = pygame.mixer.Sound('sounds\\win.ogg')
snd_back = pygame.mixer.Sound('sounds\\menu_back.ogg')
snd_back.set_volume(0.1)

start_game = False
cur_maps = MAPS[:]
MAP = cur_maps[0]
clock = pygame.time.Clock()
run = True
while run:
    if start_game:
        start_game = False
        pygame.mouse.set_visible(False)
        game_result = game(MAP)
        pygame.mouse.set_visible(True)
        pygame.mixer.set_num_channels(2)
        if game_result == 'win':
            snd_win.play()
            cur_maps.pop(0)
            if not cur_maps:
                manage_screen('Ви пройшли гру!')
                run = False
            else:
                if manage_screen('Ви перемогли!'):
                    MAP = cur_maps[0]
                    start_game = True
        elif game_result == 'lose':
            snd_lose.play()
            if manage_screen('Ви програли!'):
                MAP = cur_maps[0]
                start_game = True
    else:
        pygame.mixer.set_num_channels(1)
        snd_back.play()
        window.blit(background, (0,0))
        mouse_pos = pygame.mouse.get_pos()
        for btn in btns:
            btn.draw(window)
            if btn.rect.collidepoint(mouse_pos):
                btn.choose(window)
        #обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_game.rect.collidepoint(mouse_pos):
                        pygame.mixer.stop()
                        snd_btn_click.play()
                        start_game = True

                    elif btn_exit.rect.collidepoint(mouse_pos):
                        pygame.mixer.stop()
                        snd_btn_click.play()
                        run = False

    pygame.display.update()
    clock.tick(60)
