from pygame import *
from random import *
import time as tm

global rel_time
rel_time = False
global num_fire
num_fire = 0
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("shooter_game")
background = transform.scale(image.load("less.jpg"), (win_width, win_height))
mixer.init()
mixer.music.load('Music_default_ui_startup_01.mp3')
mixer.music.play()
kick = mixer.Sound('a1.mp3')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, x_size, y_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x_size, y_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 595:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE]:
            global num_fire, rel_time, k 
            if num_fire < 5:
                self.fire()
                num_fire += 1
            if num_fire >= 5 and not rel_time:
                rel_time = True
                k = tm.time()
           
                
            

    def fire(self):
        bullet = Bullet('screen-2.png', self.rect.centerx, self.rect.top, 5, 15, 20 )
        bullets.add(bullet)
pudge = player('pudge.png', 350, 400 , 5, 65, 65)
lost = 0
class enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.x = randint(70, 630)
            self.rect.y = 0    
            lost += 1
            kick.play()
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

crip = enemy('crip.png', 100, 0, 3, 65, 65)
crip1 = enemy('crip.png', 200, 0, 2, 65, 65)
crip2 = enemy('crip.png', 300, 0, 4, 65, 65)
crip3 = enemy('crip.png', 400, 0, 1, 65, 65)
crip4 = enemy('crip.png', 500, 0, 3, 65, 65)
monsters = sprite.Group()
monsters.add(crip)
monsters.add(crip1)
monsters.add(crip2)
monsters.add(crip3)
monsters.add(crip4)
font.init()
font1 = font.Font(None, 36)  
font2 = font.Font(None, 50)
font3 = font.Font(None, 50)
bullets = sprite.Group()
tower = enemy('tower(2).png', 600, 0, 2, 40, 40)
tower1 = enemy('tower(2).png', 700, 0, 2, 40, 40)
tower2 = enemy('tower(2).png', 150, 0, 2, 40, 40)
towers = sprite.Group()
towers.add(tower)
towers.add(tower1)
towers.add(tower2)
p = 0
global c 
c = 3
global v
v = 0
finish = False
game = True
clock = time.Clock()
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
           game = False
    if finish != True:
        window.blit(background,(0, 0))
        pudge.update()
        monsters.update()
        bullets.update()
        towers.update()
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (25, 50))
        sprites_list = sprite.spritecollide(pudge, monsters, True)
        if rel_time == True:
            b = tm.time()
            if b - k >= 3:
                num_fire = 0
                rel_time = False
            else:
                text_reload = font1.render("Хук кд бро(", 1, (255, 255, 255))
                window.blit(text_reload, (300, 400 ))
        for i in sprites_list:
            c -= 1
            crip = enemy('crip.png', randint(70, 630), 0, 3, 65, 65)
            monsters.add(crip)
        if c <= 0 or lost >= 10:
            textL = font2.render('YOU LOSE', 1, (250, 0, 0))
            window.blit(textL, (300, 300))
        sprites_list1 = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list2 = sprite.groupcollide(towers, bullets, False, True)
        sprites_list3 = sprite.spritecollide(pudge, towers, True)
        for i in sprites_list:
            c -= 1
            crip = enemy('crip.png', randint(70, 630), 0, 3, 65, 65)
            monsters.add(crip)
        for i in sprites_list3:
            c -= 1
            tower = enemy('tower(2).png', randint(0, 630), 0, 2, 40, 40)
            towers.add(tower)
        text_win = font1.render("Убито: " + str(p), 1, (255, 255, 255))
        window.blit(text_win, (25, 80))
        text_helth = font1.render("Количество здоровья: " + str(c), 1, (255, 255, 255))
        window.blit(text_helth, (350, 70))
        if p >= 10:           
            finish = True
            textW = font3.render('YOU WIN', 1, (0, 250, 0))
            window.blit(textW, (300, 300))

    pudge.reset()
    monsters.draw(window)
    towers.draw(window)
    bullets.draw(window)
    display.update()
    clock.tick(30)
