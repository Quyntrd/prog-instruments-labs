"""
 @Author : TheKnight
 Date : 6/09/2020

 copyright  © TheKight All Right Reserved
"""

import pygame
import random
import math
import time

from pygame import mixer

pygame.init()

clock = pygame.time.Clock()

# bg sound
mixer.music.load("bg.wav")
mixer.music.play(-1)

score_value = 0

# setting the display
screen = pygame.display.set_mode((800, 600))

# background
bg = pygame.image.load("img2.png")

icon = pygame.image.load("icond.png")
pygame.display.set_caption("Space Bullet Shooter")
# display the icon
pygame.display.set_icon(icon)

# showing the bird image
player_img = pygame.image.load("pl4.png")
player_x = 370
player_y = 460

player_x_change = 0

def player(x, y):
    screen.blit(player_img, (x, y))

# for enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

number_of_enemies = 6
for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load("ens.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(30)

# bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 20
bullet_state = "ready"

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 53, y + 10))

# checking if collision
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) +
                         (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# showing score
font = pygame.font.Font("freesansbold.ttf", 35)
score_x = 10
score_y = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value),
                        True, (255, 255, 255))
    screen.blit(score, (x, y))

over_font = pygame.font.Font("freesansbold.ttf", 60)

# game over
def game_over():
    over = over_font.render("GAME OVER", True, (0, 0, 255))
    screen.blit(over, (250, 250))

final_font = pygame.font.Font("freesansbold.ttf", 50)

def final_score():
    finalscore = final_font.render("Total Score : " + str(score_value),
                                   True, (0, 255, 0))
    screen.blit(finalscore, (280, 350))

author_font = pygame.font.Font("freesansbold.ttf", 16)

# showing author name
def show_author():
    subject = author_font.render("Copyright ©2020 TheKnight All Right Reserved",
                                 True, (0, 255, 0))
    screen.blit(subject, (170, 580))

# game loop
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5

            if event.key == pygame.K_RIGHT:
                player_x_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    bullet_sound = mixer.Sound("bulletout.wav")
                    bullet_sound.play()

                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_LEFT:
                player_x_change = 0

    for i in range(number_of_enemies):
        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over()
            time.sleep(2)
            final_score()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_sound = mixer.Sound("bulletshoot.wav")
            bullet_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 730:
        player_x = 730

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(score_x, score_y)
    show_author()

    pygame.display.update()
