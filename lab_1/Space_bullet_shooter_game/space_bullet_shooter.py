"""
Author : TheKnight
Date : 6/09/2020

This is a Space Bullet Shooter game using Pygame.
Copyright © TheKnight. All Rights Reserved.
"""

import math
import random
import time

import pygame
from pygame import mixer


pygame.init()

clock = pygame.time.Clock()

# Background music
mixer.music.load("bg.wav")
mixer.music.play(-1)

# Initialize score
score_value = 0

# Set up display
screen = pygame.display.set_mode((800, 600))

# Load background image
bg = pygame.image.load("img2.png")

# Set window icon and caption
icon = pygame.image.load("icond.png")
pygame.display.set_caption("Space Bullet Shooter")
pygame.display.set_icon(icon)

# Player settings
player_img = pygame.image.load("pl4.png")
player_x = 370
player_y = 460
player_x_change = 0

def player(x, y):
    """Draw the player on the screen at the given coordinates."""
    screen.blit(player_img, (x, y))

# Enemy settings
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

# Bullet settings
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_change = 20
bullet_state = "ready"  # "ready" means bullet is not visible

def enemy(x, y, i):
    """Draw the enemy on the screen at the given coordinates."""
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y, bullet_state):
    """Move the bullet upwards and change its state to 'fire'."""
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 53, y + 10))
    return bullet_state

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    """Check if a collision occurred between an enemy and the bullet."""
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) +
                         (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

# Score settings
font = pygame.font.Font("freesansbold.ttf", 35)
score_x = 10
score_y = 10

def show_score(x, y, score_value):
    """Display the current score on the screen."""
    score = font.render("Score : " + str(score_value),
                        True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game over screen settings
over_font = pygame.font.Font("freesansbold.ttf", 60)

def game_over():
    """Display the 'Game Over' screen."""
    over = over_font.render("GAME OVER", True, (0, 0, 255))
    screen.blit(over, (250, 250))

# Final score display settings
final_font = pygame.font.Font("freesansbold.ttf", 50)

def final_score(score_value):
    """Display the final score when the game ends."""
    finalscore = final_font.render("Total Score : " + str(score_value),
                                   True, (0, 255, 0))
    screen.blit(finalscore, (280, 350))

# Author information display
author_font = pygame.font.Font("freesansbold.ttf", 16)

def show_author():
    """Display the author's copyright information on the screen."""
    subject = author_font.render("Copyright ©2020 TheKnight All Right Reserved",
                                 True, (0, 255, 0))
    screen.blit(subject, (170, 580))

# Main game loop
running = True

while running:
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(bg, (0, 0))  # Display background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Control the player movement
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

                    bullet_state = fire_bullet(bullet_x, bullet_y, bullet_state)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Move the enemies and check for game over
    for i in range(number_of_enemies):
        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over()
            time.sleep(2)
            final_score(score_value)
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # Check for collision
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

    # Player movement boundaries
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 730:
        player_x = 730

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y, bullet_state)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(score_x, score_y, score_value)
    show_author()

    pygame.display.update()
