import pygame
import sys
import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game: Combined Fuzzy Logic Features")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

player = pygame.Rect(100, 100, 50, 50)
enemy = pygame.Rect(400, 300, 50, 50)
player_speed = 5
player_health = 100

TIMER_START = 60
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# fuzzy variables
time_remaining = ctrl.Antecedent(np.arange(0, 61, 1), 'time_remaining')
player_level = ctrl.Antecedent(np.arange(0, 101, 1), 'player_level')
tracking_speed = ctrl.Consequent(np.arange(1, 6, 0.1), 'tracking_speed')
enemy_damage = ctrl.Consequent(np.arange(0, 101, 1), 'enemy_damage')

# Membership functions
time_remaining['long'] = fuzz.trimf(time_remaining.universe, [30, 60, 60])
time_remaining['medium'] = fuzz.trimf(time_remaining.universe, [10, 30, 50])
time_remaining['short'] = fuzz.trimf(time_remaining.universe, [0, 0, 30])

player_level['beginner'] = fuzz.trimf(player_level.universe, [0, 0, 50])
player_level['intermediate'] = fuzz.trimf(player_level.universe, [30, 50, 70])
player_level['expert'] = fuzz.trimf(player_level.universe, [50, 100, 100])

tracking_speed['slow'] = fuzz.trimf(tracking_speed.universe, [1, 1, 3])
tracking_speed['moderate'] = fuzz.trimf(tracking_speed.universe, [2, 3, 4])
tracking_speed['fast'] = fuzz.trimf(tracking_speed.universe, [3, 5, 5])

enemy_damage['low'] = fuzz.trimf(enemy_damage.universe, [0, 0, 40])
enemy_damage['medium'] = fuzz.trimf(enemy_damage.universe, [30, 50, 70])
enemy_damage['high'] = fuzz.trimf(enemy_damage.universe, [60, 100, 100])

# fuzzy rules
rule1 = ctrl.Rule(time_remaining['long'], tracking_speed['slow'])
rule2 = ctrl.Rule(time_remaining['medium'], tracking_speed['moderate'])
rule3 = ctrl.Rule(time_remaining['short'], tracking_speed['fast'])

rule4 = ctrl.Rule(player_level['beginner'], enemy_damage['high'])
rule5 = ctrl.Rule(player_level['intermediate'], enemy_damage['medium'])
rule6 = ctrl.Rule(player_level['expert'], enemy_damage['low'])

# control systems
tracking_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
damage_ctrl = ctrl.ControlSystem([rule4, rule5, rule6])

# simulations
tracking_sim = ctrl.ControlSystemSimulation(tracking_ctrl)
damage_sim = ctrl.ControlSystemSimulation(damage_ctrl)

font = pygame.font.Font(None, 36)

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += player_speed
    if keys[pygame.K_a] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH:
        player.x += player_speed

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    remaining_time = max(0, TIMER_START - int(seconds_passed))
    player_level_value = max(0, (60 - remaining_time) / 60 * 100)

    # fuzzy logic to calculate enemy tracking speed
    tracking_sim.input['time_remaining'] = remaining_time
    tracking_sim.compute()
    enemy_speed = tracking_sim.output['tracking_speed']

    # fuzzy logic to calculate enemy damage dynamically
    damage_sim.input['player_level'] = player_level_value
    damage_sim.compute()
    damage_output = damage_sim.output['enemy_damage']

    if enemy.x < player.x:
        enemy.x += enemy_speed
    if enemy.x > player.x:
        enemy.x -= enemy_speed
    if enemy.y < player.y:
        enemy.y += enemy_speed
    if enemy.y > player.y:
        enemy.y -= enemy_speed

    enemy.x = max(0, min(WIDTH - enemy.width, enemy.x))
    enemy.y = max(0, min(HEIGHT - enemy.height, enemy.y))

    if player.colliderect(enemy):
        player_health -= damage_output / 30
        if player_health < 0:
            player_health = 0

    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, enemy)

    health_text = font.render(f"Health: {int(player_health)}", True, BLACK)
    timer_text = font.render(f"Time Left: {remaining_time}s", True, BLACK)
    speed_text = font.render(f"Enemy Speed: {enemy_speed:.2f}", True, BLACK)
    level_text = font.render(f"Player Level: {int(player_level_value)}", True, BLACK)
    screen.blit(health_text, (10, 10))
    screen.blit(timer_text, (WIDTH - 200, 10))
    screen.blit(speed_text, (10, 50))
    screen.blit(level_text, (10, 100))

    if player_health <= 0:
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    if remaining_time == 0:
        win_text = font.render("You Survived!", True, BLUE)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()

    clock.tick(30)
