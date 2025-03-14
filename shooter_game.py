from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shoter Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
run = True
finish = False
shot = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
speed = 3
player = Player('rocket.png', 250, 400, 100, 100, speed)
enemy1 = Enemy('ufo.png', 0, 0, 90, 50, randint(1, 2))
enemy2 = Enemy('ufo.png', 100, 0, 90, 50, randint(1, 2))
enemy3 = Enemy('ufo.png', 200, 0, 90, 50, randint(1, 2))
enemy4 = Enemy('ufo.png', 300, 0, 90, 50, randint(1, 2))
enemy5 = Enemy('ufo.png', 400, 0, 90, 50, randint(1, 2))
asteroid1 = Asteroid('asteroid.png', 0, 0, 90, 50, randint(1, 3))
asteroid2 = Asteroid('asteroid.png', 305, 0, 90, 50, randint(1, 3))
asteroid3 = Asteroid('asteroid.png', 555, 0, 90, 50, randint(1, 3))
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
font.init()
font = font.SysFont('Arial', 36)
kills = 0
lives = 3
win = font.render('YOU WIN!', 1, (0, 255, 0))
game_over = font.render('GAME OVER!', 1, (255, 0, 0))

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               player.fire()
               shot.play()

    if finish != True:
        window.blit(background, (0, 0))
        text_lose = font.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_kills = font.render('Счёт: ' + str(kills), 1, (255, 255, 255))
        text_lives = font.render('Жизни: ' + str(lives), 1, (255, 255, 255))
        window.blit(text_lose, (10, 10))
        window.blit(text_kills, (10, 50))
        window.blit(text_lives, (10, 90))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprites = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites:
            enemy = Enemy('ufo.png', randint(80, win_width - 80), 0, 90, 50, 1)
            monsters.add(enemy)
            kills += 1

        sprites2 = sprite.spritecollide(player, asteroids, True)
        for i in sprites2:
            lives -= 1

        if kills >= 10:
            finish = True
            window.blit(win, (240, 220))

        if lost >= 3 or lives == 0:
            finish = True
            window.blit(game_over, (240, 220))

        display.update()
        clock.tick(FPS)