import pygame
import sys
import numpy as np
from stable_baselines3 import PPO
import skfuzzy as fuzz
from skfuzzy import control as ctrl

model = PPO.load("enemy_ai_ppo")
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game: PPO-Controlled Enemy")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

player = pygame.Rect(100, 100, 50, 50)  # Player: x, y, width, height
enemy = pygame.Rect(400, 300, 50, 50)  # Enemy: x, y, width, height
player_speed = 5
player_health = 100

TIMER_START = 60  # Seconds to survive
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()  # Start timer

font = pygame.font.Font(None, 36)

# ====== Fuzzy Logic Setup ======
# Define fuzzy variables
player_level = ctrl.Antecedent(np.arange(0, 101, 1), 'player_level')  # 0 to 100
enemy_damage = ctrl.Consequent(np.arange(0, 101, 1), 'enemy_damage')  # 0 to 100

player_level['beginner'] = fuzz.trimf(player_level.universe, [0, 0, 50])
player_level['intermediate'] = fuzz.trimf(player_level.universe, [30, 50, 70])
player_level['expert'] = fuzz.trimf(player_level.universe, [50, 100, 100])

enemy_damage['low'] = fuzz.trimf(enemy_damage.universe, [0, 0, 40])
enemy_damage['medium'] = fuzz.trimf(enemy_damage.universe, [30, 50, 70])
enemy_damage['high'] = fuzz.trimf(enemy_damage.universe, [60, 100, 100])

rule1 = ctrl.Rule(player_level['beginner'], enemy_damage['low'])
rule2 = ctrl.Rule(player_level['intermediate'], enemy_damage['medium'])
rule3 = ctrl.Rule(player_level['expert'], enemy_damage['high'])

damage_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
damage_sim = ctrl.ControlSystemSimulation(damage_ctrl)

while True:
    screen.fill(WHITE)  # Background color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:  # Move up
        player.y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT:  # Move down
        player.y += player_speed
    if keys[pygame.K_a] and player.left > 0:  # Move left
        player.x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH:  # Move right
        player.x += player_speed

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000  # Elapsed time
    remaining_time = max(0, TIMER_START - int(seconds_passed))
    player_level_value = max(0, (60 - remaining_time) / 60 * 100)  # Scale level 0-100

    observation = np.array([player.x - enemy.x, player.y - enemy.y, 0, 0], dtype=np.float32)

    action, _states = model.predict(observation, deterministic=True)

    enemy_speed = 3  # Base speed for enemy movement
    if action == 0:  # Move up
        enemy.y -= enemy_speed
    elif action == 1:  # Move down
        enemy.y += enemy_speed
    elif action == 2:  # Move left
        enemy.x -= enemy_speed
    elif action == 3:  # Move right
        enemy.x += enemy_speed

    # ====== Updated Damage Calculation ======
    damage_sim.input['player_level'] = player_level_value
    damage_sim.compute()
    fuzzy_damage = damage_sim.output['enemy_damage']  # Base damage from fuzzy logic

    distance = np.linalg.norm(np.array([enemy.x, enemy.y]) - np.array([player.x, player.y]))
    distance_factor = 1 / (1 + distance)  # Scale between 0 and 1

    if player.colliderect(enemy):
        # Final damage calculation
        final_damage = fuzzy_damage * distance_factor
        player_health -= final_damage  # Reduce health accordingly


    # Ensure player health doesn't go negative
    player_health = max(0, player_health)

    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, enemy)
    health_text = font.render(f"Health: {int(player_health)}", True, BLACK)
    timer_text = font.render(f"Time Left: {remaining_time}s", True, BLACK)
    screen.blit(health_text, (10, 10))
    screen.blit(timer_text, (WIDTH - 200, 10))

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
