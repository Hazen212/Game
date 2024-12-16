import pygame
import random
import math
from pygame import mixer

pygame.init()

#tao cai man hinh game
screen = pygame.display.set_mode((800, 600))

#tạo cái background
background = pygame.image.load('background.jpg')

#am thanh cua background
mixer.music.load('background.mp3')
mixer.music.play(-1)

#Ten game vs Logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#giao dien nguoi choi
playerimg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#giao dien UFO
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
so_luong_ufo = 6

for i in range(so_luong_ufo):
    enemyimg.append(pygame.image.load('enemies.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.15)
    enemyY_change.append(40)


#vien dan
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

#ghi diem
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#thua game
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value),True,(255, 0, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(0, 0, 0))
    screen.blit(over_text, (200,250))


def player(x,y):
    screen.blit(playerimg,(x, y))

def enemy(x,y,i):
    screen.blit(enemyimg[i],(x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x, y))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
    if distance < 27:
        return True
    else:
        return False




#vong lap game
running = True
while running:
    # RGB = Do - Xanh La - Xanh Lam
    screen.fill((0, 0, 0))
    #hinh anh Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#bam phim trai hay phai
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.25
            if event.key == pygame.K_RIGHT:
                playerX_change = +0.25
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

#duong di cua ng choi
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

#duong di cua con UFO
    for i in range(so_luong_ufo):

        #luc thua game
        if enemyY[i] > 200:
            for j in range(so_luong_ufo):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.15
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.15
            enemyY[i] += enemyY_change[i]

        # vien dan ban zo con ufo
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)


#duong di cua vien dan
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
