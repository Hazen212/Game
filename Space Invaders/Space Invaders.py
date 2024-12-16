import pygame
import sys
import random
import math
from pygame import mixer

pygame.init()

# setup cái background
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BG_COLOR = "black"
WHITE = "White"
BLACK = "Black"
GREEN = "Green"

# giao diện vs cả tên game
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# hình nền background
BG = pygame.image.load("background2.jpg")


# phông chữ add
def get_font(size):
    return pygame.font.Font("font.ttf", size)


# các nút bấm
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# vận hành game
def play():
    # chơi game
    background = pygame.image.load('background.jpg')
    mixer.music.load('background.mp3')
    mixer.music.play(1)
#người chơi
    player_img = pygame.image.load('spaceship.png')
    player_x, player_y = 370, 480
    player_x_change = 0
#đối thủ
    enemy_img, enemy_x, enemy_y = [], [], []
    enemy_x_change, enemy_y_change = [], []
    num_enemies = 5
    for _ in range(num_enemies):
        enemy_img.append(pygame.image.load('enemies.png'))
        enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(2)
        enemy_y_change.append(30)
#bắn
    bullet_img = pygame.image.load('bullet.png')
    bullet_x, bullet_y = 0, 480
    bullet_y_change = 4.5
    bullet_state = "ready"

#setup cách ghi điểm
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    over_font = pygame.font.Font('freesansbold.ttf', 64)

#ghi điểm
    def show_score():
        score = font.render(f"Score : {score_value}", True, (0,0,0))
        SCREEN.blit(score, (10, 10))

    def game_over_text():
        over_text = over_font.render("GAME OVER!", True, BLACK)
        SCREEN.blit(over_text, (200, 250))

    def player(x, y):
        SCREEN.blit(player_img, (x, y))

    def enemy(x, y, i):
        SCREEN.blit(enemy_img[i], (x, y))
#bắn tia lửa điện
    def fire_bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        SCREEN.blit(bullet_img, (x + 16, y + 10))
#lúc đạn dính vô đối thủ
    def is_collision(ex, ey, bx, by):
        return math.sqrt((ex - bx) ** 2 + (ey - by) ** 2) < 27

    running = True
    clock = pygame.time.Clock()

#các nút bấm để chơi game
    while running:
        SCREEN.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -2.5
                if event.key == pygame.K_RIGHT:
                    player_x_change = 2.5
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
                    mixer.Sound('laser.wav').play()

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_x_change = 0

        player_x += player_x_change
        player_x = max(0, min(SCREEN_WIDTH - 64, player_x))

        for i in range(num_enemies):
            if enemy_y[i] > 230:
                for j in range(num_enemies):
                    enemy_y[j] = 2000
                game_over_text()
                break

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0 or enemy_x[i] >= SCREEN_WIDTH - 64:
                enemy_x_change[i] *= -1
                enemy_y[i] += enemy_y_change[i]

            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                mixer.Sound('explosion.wav').play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
                enemy_y[i] = random.randint(50, 150)

            enemy(enemy_x[i], enemy_y[i], i)
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score()
        pygame.display.update()
        clock.tick(FPS)


#setup giao diện game
def options():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                return

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=None, pos=(400, 250), text_input="PLAY", font=get_font(75), base_color=WHITE,
                             hovering_color=GREEN)
        QUIT_BUTTON = Button(image=None, pos=(400, 400), text_input="QUIT", font=get_font(75), base_color=WHITE,
                             hovering_color=GREEN)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
