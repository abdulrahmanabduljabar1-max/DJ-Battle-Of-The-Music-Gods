import pygame
import random
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DJ: Battle Of The Music Gods")

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
NEON = (0, 255, 200)
RED = (255, 60, 60)
PURPLE = (180, 0, 255)
BLUE = (0, 150, 255)

# Player
player = pygame.Rect(100, 300, 50, 50)
player_speed = 5
player_health = 100

# Beats (bullets)
beats = []

# Enemies
enemies = []

for i in range(6):
    enemy = pygame.Rect(random.randint(400, 850), random.randint(50, 600), 50, 50)
    enemies.append(enemy)

# Zone (battle royale circle)
zone_radius = 400
zone_center = (WIDTH // 2, HEIGHT // 2)

# Weapon system
weapon_type = "BASS"
cooldown = 0

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

def draw_window():
    screen.fill(BLACK)

    # Zone circle
    pygame.draw.circle(screen, PURPLE, zone_center, zone_radius, 3)

    # Player
    pygame.draw.rect(screen, NEON, player)

    # Beats
    for beat in beats:
        pygame.draw.circle(screen, beat["color"], (beat["x"], beat["y"]), 6)

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # UI
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    weapon_text = font.render(f"Weapon: {weapon_type}", True, WHITE)

    screen.blit(health_text, (10, 10))
    screen.blit(weapon_text, (10, 40))

    pygame.display.update()

running = True

while running:
    clock.tick(60)
    cooldown -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Switch weapons
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                weapon_type = "BASS"
            if event.key == pygame.K_2:
                weapon_type = "TRAP"
            if event.key == pygame.K_3:
                weapon_type = "LASER"

            # Shoot
            if event.key == pygame.K_SPACE and cooldown <= 0:
                if weapon_type == "BASS":
                    beats.append({"x": player.x + 25, "y": player.y + 25, "dx": 8, "dy": 0, "damage": 15, "color": NEON})
                    cooldown = 15

                elif weapon_type == "TRAP":
                    for angle in [-0.2, 0, 0.2]:
                        beats.append({
                            "x": player.x + 25,
                            "y": player.y + 25,
                            "dx": 7,
                            "dy": angle * 10,
                            "damage": 10,
                            "color": BLUE
                        })
                    cooldown = 25

                elif weapon_type == "LASER":
                    beats.append({"x": player.x + 25, "y": player.y + 25, "dx": 15, "dy": 0, "damage": 25, "color": PURPLE})
                    cooldown = 35

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.y -= player_speed
    if keys[pygame.K_s]: player.y += player_speed
    if keys[pygame.K_a]: player.x -= player_speed
    if keys[pygame.K_d]: player.x += player_speed

    # Keep player in screen
    player.clamp_ip(screen.get_rect())

    # Move beats
    for beat in beats[:]:
        beat["x"] += beat["dx"]
        beat["y"] += beat["dy"]

        if beat["x"] > WIDTH or beat["y"] > HEIGHT or beat["y"] < 0:
            beats.remove(beat)

    # Enemy AI (chasing player)
    for enemy in enemies:
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        dist = math.hypot(dx, dy)

        if dist != 0:
            enemy.x += int(dx / dist * 2)
            enemy.y += int(dy / dist * 2)

        # Collision damage
        if player.colliderect(enemy):
            player_health -= 0.3

    # Beat hits enemy
    for beat in beats[:]:
        for enemy in enemies[:]:
            if pygame.Rect(beat["x"], beat["y"], 5, 5).colliderect(enemy):
                if beat in beats:
                    beats.remove(beat)
                enemies.remove(enemy)

                # Respawn stronger enemy
                new_enemy = pygame.Rect(random.randint(400, 850), random.randint(50, 600), 50, 50)
                enemies.append(new_enemy)
                break

    # Zone shrinking
    zone_radius -= 0.02
    player_dist = math.hypot(player.x - zone_center[0], player.y - zone_center[1])

    if player_dist > zone_radius:
        player_health -= 0.2

    # Game Over
    if player_health <= 0:
        print("💀 GAME OVER - The Music Gods Defeated You")
        running = False

    draw_window()

pygame.quit()
