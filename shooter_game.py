#Create your own shooter

from pygame import *
from random import randint
from time import time as timer

img_back = 'galaxy.jpg'
img_player = 'rocket.png'
img_ufo = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = 'asteroid.png'

font.init()
font1 = font.SysFont('arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont('arial', 36)


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self): 
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



rocket = player(img_player, 5, win_height - 100, 80, 100, 10)

ufos = sprite.Group()

bullets = sprite.Group()

for i in range(1, 6):
    ufo = enemy(img_ufo, randint(80, win_width - 80), - 40, 80, 50, randint(1,5))
    ufos.add(ufo)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

score = 0
lost = 0
max_lost = 3
goal = 100
life = 3

real_time = False

num_fire = 0

finish = False

run = True
while run:
    for e in event.get():
        if e.type == QUIT: 
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    rocket.fire()

                if num_fire >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True

    if not finish:
        window.blit(background, (0,0))

        text = font2.render('Score: ' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lost = font2.render('Missed: ' + str(lost), 1, (255,255,255))
        window.blit(text_lost, (10,50))

        if life == 3:
            life_color = (1,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        rocket.update()
        ufos.update()
        bullets.update()
        asteroids.update()

        rocket.reset()
        ufos.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if real_time == True:
            cur_time = timer()

            if cur_time - last_time < 3:
                reload = font2.render('Wait, reload... ', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_time = False

        collides = sprite.groupcollide(ufos, bullets, True, True)
        for collide in collides:
            score = score + 1
            ufo = enemy(img_ufo, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            ufos.add(ufo)

            if sprite.spritecollide(rocket, ufos, False) or sprite.spritecollide(rocket, asteroids, False):
                sprite.spritecollide(rocket, ufos, True)
                sprite.spritecollide(rocket, asteroids, True)
                life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))    
        display.update()
    
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0

        for b in bullets:
            b.kill()
        for u in ufos:
            u.kill()

        time.delay(3000)
        for i in range(1,6):
            ufo = enemy(img_ufo, randint(80, win_width - 80), 40, 80, 50, randint(1,5))
            ufos.add(ufo)

        for i in range(1, 3):
            asteroid = enemy(img_ast, randint(80, win_width - 30, -40, 80, 50, randint(1,7)))
            asteroids.add(asteroid)

    time.delay(50)