import pygame
from random import uniform

class Button:
    def __init__(self, x, y, w, h, btn_color, btn_ch_color, txt_color, txt_size, txt):
        self.rect = pygame.Rect(x, y, w, h)
        self.txt = txt
        self.btn_color = btn_color
        self.btn_ch_color = btn_ch_color
        self.txt_color = txt_color
        self.txt_size = txt_size
    
    def draw(self, window):
        pygame.draw.rect(window, self.btn_color, self.rect)
        font = pygame.font.SysFont('arial', self.txt_size, bold=1)
        text = font.render(self.txt, True, self.txt_color)
        txt_rect = text.get_rect(center=self.rect.center)
        window.blit(text, txt_rect)

    def choose(self, window):
        pygame.draw.rect(window, self.btn_ch_color, self.rect)
        font = pygame.font.SysFont('arial', self.txt_size, bold=1)
        text = font.render(self.txt, True, self.txt_color)
        txt_rect = text.get_rect(center=self.rect.center)
        window.blit(text, txt_rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size, image_path):
        self.rect = pygame.Rect(x, y, size, size)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (size, size)).convert()
        
class Acid(pygame.sprite.Sprite):
    def __init__(self, x, y, size, images_path):
        self.rect = pygame.Rect(x, y, size, size)
        self.frame = 0
        self.images_path = images_path
        self.image = pygame.image.load(self.images_path + str(self.frame) + '.png')

    def update(self, framerate):
        self.frame += framerate
        if self.frame >= 8:
            self.frame = 0
        self.image = pygame.image.load(self.images_path + str(int(self.frame)) + '.png')
        

class Flag(Acid):
    def update(self, window, framerate):
        self.frame += framerate
        if self.frame >= 7:
            self.frame = 0
        self.image = pygame.image.load(self.images_path + str(int(self.frame)) + '.png')
        window.blit(self.image, self.rect)
        
class Spike:
    def __init__(self, x, y, size, images_path):
        self.rect = pygame.Rect(x, y, size, size)
        self.frame = 0
        self.framerate = 0.05
        self.up_framerate = round(uniform(0.01, 0.04), 2)
        self.images_path = images_path
        self.image = pygame.image.load(f'{self.images_path}\\{self.frame}.png')

    def update(self):
        self.frame += self.framerate
        if int(self.frame) == 0:
            self.framerate = self.up_framerate
        elif 1 <= int(self.frame) <= 3:
            self.framerate = 0.2
        elif int(self.frame) == 4:
            self.framerate = 0.01
        elif int(self.frame) == 5:
            self.framerate == 0.05
        else:
            self.frame = 0
        self.image = pygame.image.load(f'{self.images_path}\\{int(self.frame)}.png')
    
    def is_up(self):
        if int(self.frame) in range(0, 4):
            return True
        return False

class Player:
    def __init__(self, x, y, speed, images_path):
        self.speed = speed
        self.direction = 'down'
        self.status = 'still'
        self.health = 3
        self.frame = 0
        self.last_damage = 0
        self.still_framerate = 0.25
        self.images_path = images_path
        self.image = pygame.image.load(f'{images_path}\\{self.direction}\\{self.status}-{self.frame}.png')
        self.rect = self.image.get_rect(x=x, y=y)

    def collideobject(self, obj):
        diff_x = self.rect.x - obj.rect.x
        diff_y = self.rect.y - obj.rect.y
        if -40 <= diff_x <= 38:
            if -49 <= diff_y <= 15:
                return True
        return False
        
    def step_back(self):
        if self.direction == 'up':
            self.rect.y += self.speed
        elif self.direction == 'down':
            self.rect.y -= self.speed
        elif self.direction == 'left':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def update_image(self):
        self.image = pygame.image.load(f'{self.images_path}\\{self.direction}\\{self.status}-{int(self.frame)}.png')
        
    def update_frame(self):
        if self.status == 'run':
            framerate = self.speed / 8
            self.frame += framerate
            if self.frame >= 10:
                self.frame = 0
        else:
            if self.frame < 1:
                self.still_framerate = 0.01
            elif 1 <= self.frame < 2:
                self.still_framerate = 0.25
            else:
                self.still_framerate = 0.4
            
            self.frame += self.still_framerate
            if self.direction == 'up':
                self.frame = 0
            else:
                if self.frame >= 3:
                    self.frame = 0
    
    def draw_hp(self, window):
        img = pygame.image.load('images\\heart.png')
        for i in range(int(self.health)):
            window.blit(img, (5 + i*30, 15))

MAPS = [
    [
        'xxxxxxxxxxxxxxxxxxxx',
        'x1 x   s   x       x',
        'x  x xx xx x xx x ox',
        'x     x x     x xssx',
        'xoo xsx osxoo x xo x',
        'xoo x x xsx   x x  x',
        'x         xsx       ',
        'x xxxoo  xxsxxxx   f',
        'x    ooo      o     ',
        'xx x  o  xxxx xxxx x',
        'x  xx       x    xsx',
        'ox   x xxoxsx xx xsx',
        'oox  x    x    x   x',
        'ooox    xxx     oxxx',
        'ooox  x      xxxxxxx',
        'xxxxxxxxxxxxxxxxxxxx',
    ],
    [
        'xxxxxxxxxxxxxxxxxxxx',
        'x  xxxoooooxxxxx   x',
        'x  x           x   x',
        'x  o xxxsoooxx x   x',
        'x  o x       x o   x',
        'x  o x xxxso x o   x',
        'x  o x x   o x     x',
        'x  o o x 1 x x o   x',
        '   o o o   x o o   x',
        'f  o x oxoxx s xs  x',
        '   o x       x x   x',
        'x  s xxxxxooxx x ssx',
        'x  x      ss   xss x',
        'x  xxxxxo ooxxxx   x',
        'x        s         x',
        'xxxxxxxxxxxxxxxxxxxx',
    ],
    [
        'xxxxxxxxxxxxxxxxxxxx',
        'x              sss x',
        'x xxxxxxxxxxxxxxxx x',
        'x x       sss    x x',
        'x x xxxxxxxxxxxx x x',
        'x x x          x x x',
        'x x x xoooooox x x x',
        'x x x o     fo x x x',
        'x x x o xoooox x x x',
        'x x x o o   o  x x x',
        'x x x o   o   ox x x',
        'xsx x xoooooooox x x',
        'xsosx            x x',
        'xsosxxxxxxxxxxxxxx x',
        'x1os           sss x',
        'xxxxxxxxxxxxxxxxxxxx',
    ]
]
