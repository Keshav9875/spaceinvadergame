import pygame
import random
from math import *
from pygame import mixer

pygame.init()

# for creating screen in pygame
screen = pygame.display.set_mode((800, 600))

# for background image
background = pygame.image.load('background.png')

# for background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# for set caption
pygame.display.set_caption("space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
running = True

# player variables
playerimage = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0


# for enemy
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 12

for i in range(no_of_enemies):

    enemyimage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(60)

# for Bullet
Bulletimage = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 10
Bullet_state = "ready"

# score variable
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scorex = 10
scorey = 10

# for gameover
gameover_font = pygame.font.Font('freesansbold.ttf', 64)


def gameover_show():
    gameover = gameover_font.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(gameover, (200, 270))

# for score


def show_score(x, y):
    gamescore = font.render("score:- "+str(score), True, (123, 255, 255))
    screen.blit(gamescore, (x, y))

# for player


def player(x, y):
    screen.blit(playerimage, (x+16, y+10))

# for enemy


def enemy(x, y, i):
    screen.blit(enemyimage[i], (x, y))

# for Bullet


def bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(Bulletimage, (x+30, y-20))

# for collision


def iscollision(enemyX, enemyY, BulletX, BulletY):
    distance = sqrt(pow(enemyX-BulletX, 2)+pow(enemyY-BulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change += 5
            if event.key == pygame.K_SPACE:
                # we save the current x coordinate of spaceship
                # for playing the sound of bullet we use mixer.sound instead of mixer.music
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                BulletX = playerX
                bullet(BulletX, BulletY)
        # if key is not down then it will continously increasing the playerx value because playerxchange is in the loop.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # for player
    playerX += playerX_change

    # for setting the boundaries of the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 726:
        playerX = 726

    # for setting the boundaries and movement of the enemy
    for i in range(no_of_enemies):

        if enemyY[i] > 460:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            # you can also set the  value of all enemies to more larger in y axis(Important note ) rather than this.
            gameover_show()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] += 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] -= 4
            enemyY[i] += enemyY_change[i]
        # for collision code
        collision = iscollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            BulletY = 480
            Bullet_state = "ready"
            score += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

   # for the movement of bullet
    if BulletY <= 0:
        BulletY = 480
        # Bullet state ready means bullet is not on the screen.
        Bullet_state = "ready"

    if Bullet_state == "fire":  # Bullet state fire means bullet is on the screen.
        bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    show_score(scorex, scorey)
    player(playerX, playerY)

    pygame.display.update()
