
import pygame
import random
import math
import os

# =========================
# 1. Initialisation
# =========================
pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooting Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 60)

# =========================
# 2. Colors
# =========================
BLACK = (20, 20, 30)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 50)
GREEN = (50, 220, 100)
RED = (230, 60, 60)

# =========================
# 3. Load images
# =========================

# Background image (optional)
if os.path.exists("back.jpg"):
    background = pygame.image.load(
        "back.jpg"
    ).convert()

    background = pygame.transform.scale(
        background, (WIDTH, HEIGHT)
    )
else:
    background = None

# Hero image
if os.path.exists("hero.jpg"):
    hero_image = pygame.image.load(
        "hero.jpg"
    ).convert_alpha()

    hero_image = pygame.transform.smoothscale(
        hero_image, (50, 50)
    )
else:
    hero_image = None
    print("Warning: hero.jpg not found!")

# Enemy image
if os.path.exists("images.jpeg"):
    enemy_image = pygame.image.load(
        "images.jpeg"
    ).convert_alpha()

    enemy_image = pygame.transform.smoothscale(
        enemy_image, (50, 50)
    )
else:
    enemy_image = None
    print("Warning: images.jpeg not found!")

# =========================
# 4. Reset game
# =========================
def reset_game():
    player = pygame.Rect(380, 500, 40, 40)

    monster = pygame.Rect(
        random.randint(0, WIDTH - 40),
        50,
        40,
        40
    )

    bullets = []
    score = 0
    health = 3
    game_over = False

    return player, monster, bullets, score, health, game_over


player, monster, bullets, score, health, game_over = reset_game()

# =========================
# 5. Game settings
# =========================
player_speed = 5
bullet_speed = 8
monster_speed = 2

running = True

# =========================
# 6. Main game loop
# =========================
while running:

    clock.tick(60)

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            # Shoot with SPACE
            if not game_over and event.key == pygame.K_SPACE:
                bullet = pygame.Rect(
                    player.centerx - 4,
                    player.top - 12,
                    8,
                    16
                )
                bullets.append(bullet)

            # Restart with R
            if game_over and event.key == pygame.K_r:
                (
                    player,
                    monster,
                    bullets,
                    score,
                    health,
                    game_over
                ) = reset_game()

    # =========================
    # Update game
    # =========================
    if not game_over:

        keys = pygame.key.get_pressed()

        # Player movement
        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
            or keys[pygame.K_q]
        ):
            player.x -= player_speed

        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        ):
            player.x += player_speed

        if (
            keys[pygame.K_UP]
            or keys[pygame.K_w]
            or keys[pygame.K_z]
        ):
            player.y -= player_speed

        if (
            keys[pygame.K_DOWN]
            or keys[pygame.K_s]
        ):
            player.y += player_speed

        # Keep player inside the window
        player.clamp_ip(screen.get_rect())

        # Move bullets
        for bullet in bullets[:]:

            bullet.y -= bullet_speed

            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Monster follows player
        dx = player.centerx - monster.centerx
        dy = player.centery - monster.centery

        distance = math.hypot(dx, dy)

        if distance > 0:
            monster.x += round(
                dx / distance * monster_speed
            )
            monster.y += round(
                dy / distance * monster_speed
            )

        # Bullet-monster collision
        for bullet in bullets[:]:

            if bullet.colliderect(monster):

                bullets.remove(bullet)
                score += 1

                # Create a new monster
                monster.x = random.randint(
                    0, WIDTH - monster.width
                )
                monster.y = random.randint(
                    0, HEIGHT // 3
                )

                break

        # Monster-player collision
        if player.colliderect(monster):

            health -= 1

            # Move monster to a new position
            monster.x = random.randint(
                0, WIDTH - monster.width
            )
            monster.y = random.randint(
                0, HEIGHT // 3
            )

            if health <= 0:
                game_over = True

    # =========================
    # 7. Drawing
    # =========================

    # Draw background
    if background is not None:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLACK)

    # Draw hero
    if hero_image is not None:
        screen.blit(hero_image, player)
    else:
        pygame.draw.rect(
            screen, (50, 150, 255), player
        )

    # Draw enemy
    if enemy_image is not None:
        screen.blit(enemy_image, monster)
    else:
        pygame.draw.rect(
            screen, RED, monster
        )

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(
            screen, YELLOW, bullet
        )

    # =========================
    # 8. Score and health
    # =========================
    score_text = font.render(
        f"Score: {score}", True, WHITE
    )

    health_text = font.render(
        f"Health: {health}", True, GREEN
    )

    screen.blit(score_text, (20, 20))
    screen.blit(health_text, (20, 55))

    # =========================
    # 9. Game over
    # =========================
    if game_over:

        title = big_font.render(
            "GAME OVER", True, RED
        )

        restart = font.render(
            "Press R to restart", True, WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 30)
            )
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 25)
            )
        )

    # Update display
    pygame.display.flip()

# =========================
# 10. Quit pygame
# =========================
pygame.quit()
