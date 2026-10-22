import sys
import random
import pygame
import os


# ==========================================
# 1. INITIALIZATION
# ==========================================
pygame.init()

try:
    pygame.mixer.init()
    pygame.mixer.music.load("effect.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    hit_sound = pygame.mixer.Sound("lough.mp3")
    hit_sound.set_volume(1.0)
    sound_available = True
except pygame.error:
    sound_available = False
    hit_sound = None

WIDTH, HEIGHT = 600, 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Shooter")

clock = pygame.time.Clock()

# ==========================================
# 2. COLORS AND FONTS
# ==========================================
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
GRAY = (120, 120, 130)
DARK = (25, 25, 45)

font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 52)
small_font = pygame.font.Font(None, 22)

# ==========================================
# 3. LOAD IMAGES
# ==========================================
background = pygame.image.load("back.jpg").convert()
background = pygame.transform.scale(
    background, (WIDTH, HEIGHT)
)

player_size = 50

player_image = pygame.image.load(
    "hr2.jpg"
).convert_alpha()

player_image = pygame.transform.scale(
    player_image, (player_size, player_size)
)

monster_image = pygame.image.load(
    "images.jpeg"
).convert_alpha()

monster_image = pygame.transform.scale(
    monster_image, (50, 50)
)

# ==========================================
# 4. GAME SETTINGS
# ==========================================
MAX_ROUNDS = 5
MAX_HEARTS = 3

player_speed = 5
bullet_speed = 7
target_speed = 1.5

player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 65

bullets = []

target = pygame.Rect(100, 60, 50, 50)

score = 0
hearts = MAX_HEARTS

music_on = sound_available
sound_on = sound_available

# Game states:
# menu, options, game, pause, win, gameover
game_state = "menu"

# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================

def draw_text(text, font_used, color, x, y, center=True):
    image = font_used.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_button(text, rect, color, mouse_pos):
    # Hover effect
    button_color = color

    if rect.collidepoint(mouse_pos):
        button_color = tuple(
            min(c + 30, 255) for c in color
        )

    pygame.draw.rect(
        screen, button_color, rect, border_radius=10
    )

    pygame.draw.rect(
        screen, WHITE, rect, 2, border_radius=10
    )

    draw_text(
        text,
        font,
        WHITE,
        rect.centerx,
        rect.centery
    )


def draw_heart(x, y, size=22, color=RED):
    # Two circles and a triangle form a heart
    radius = size // 4

    pygame.draw.circle(
        screen, color,
        (x - radius, y - radius // 2),
        radius
    )

    pygame.draw.circle(
        screen, color,
        (x + radius, y - radius // 2),
        radius
    )

    pygame.draw.polygon(
        screen,
        color,
        [
            (x - size // 2, y - radius // 2),
            (x + size // 2, y - radius // 2),
            (x, y + size // 2)
        ]
    )


def draw_hearts():
    for i in range(hearts):
        draw_heart(25 + i * 30, 30)


def reset_target():
    target.x = random.randint(
        0, WIDTH - target.width
    )
    target.y = random.randint(40, 100)


def start_new_game():
    global player_x, player_y
    global bullets, score, hearts, game_state

    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - 65

    bullets = []
    score = 0
    hearts = MAX_HEARTS

    reset_target()
    game_state = "game"


def play_hit_sound():
    if sound_on and hit_sound is not None:
        hit_sound.play()


def toggle_music():
    global music_on

    if not sound_available:
        return

    music_on = not music_on

    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def toggle_sound():
    global sound_on

    if sound_available:
        sound_on = not sound_on


def draw_game():
    screen.blit(background, (0, 0))

    # Draw monster
    screen.blit(monster_image, target.topleft)

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(bullet[0]), int(bullet[1])),
            5
        )

    # Score and hearts
    draw_text(
        f"Round: {score + 1}/{MAX_ROUNDS}",
        font,
        WHITE,
        WIDTH - 100,
        25
    )

    draw_hearts()

    # Pause button
    pause_rect = pygame.Rect(WIDTH - 95, 45, 80, 30)

    draw_button(
        "PAUSE",
        pause_rect,
        BLUE,
        pygame.mouse.get_pos()
    )

    return pause_rect


# ==========================================
# 6. MAIN LOOP
# ==========================================
while True:

    mouse_pos = pygame.mouse.get_pos()

    # --------------------------------------
    # MAIN MENU
    # --------------------------------------
    if game_state == "menu":

        screen.blit(background, (0, 0))

        # Dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(
            "MONSTER SHOOTER",
            big_font,
            YELLOW,
            WIDTH // 2,
            75
        )

        new_game_rect = pygame.Rect(
            WIDTH // 2 - 100, 135, 200, 45
        )

        options_rect = pygame.Rect(
            WIDTH // 2 - 100, 195, 200, 45
        )

        exit_rect = pygame.Rect(
            WIDTH // 2 - 100, 255, 200, 45
        )

        draw_button(
            "NEW GAME",
            new_game_rect,
            GREEN,
            mouse_pos
        )

        draw_button(
            "OPTIONS",
            options_rect,
            BLUE,
            mouse_pos
        )

        draw_button(
            "EXIT",
            exit_rect,
            RED,
            mouse_pos
        )

        draw_text(
            "Hit the monster 5 times to win!",
            small_font,
            WHITE,
            WIDTH // 2,
            335
        )

    # --------------------------------------
    # OPTIONS MENU
    # --------------------------------------
    elif game_state == "options":

        screen.blit(background, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(
            "OPTIONS",
            big_font,
            YELLOW,
            WIDTH // 2,
            65
        )

        music_text = (
            "Music: ON" if music_on else "Music: OFF"
        )

        sound_text = (
            "Sound Effects: ON"
            if sound_on else "Sound Effects: OFF"
        )

        music_rect = pygame.Rect(
            WIDTH // 2 - 125, 120, 250, 45
        )

        sound_rect = pygame.Rect(
            WIDTH // 2 - 125, 180, 250, 45
        )

        back_rect = pygame.Rect(
            WIDTH // 2 - 100, 255, 200, 45
        )

        draw_button(
            music_text,
            music_rect,
            BLUE,
            mouse_pos
        )

        draw_button(
            sound_text,
            sound_rect,
            BLUE,
            mouse_pos
        )

        draw_button(
            "BACK",
            back_rect,
            RED,
            mouse_pos
        )

        if not sound_available:
            draw_text(
                "Audio could not be initialized",
                small_font,
                WHITE,
                WIDTH // 2,
                325
            )

    # --------------------------------------
    # GAME
    # --------------------------------------
    elif game_state == "game":

        pause_rect = draw_game()

        # Move player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

        # Keep player inside the window
        player_x = max(
            0, min(player_x, WIDTH - player_size)
        )

        player_y = max(
            0, min(player_y, HEIGHT - player_size)
        )

        # Move target down
        target.y += target_speed

        # Monster escapes if it reaches the bottom
        if target.top >= HEIGHT:
            hearts -= 1
            reset_target()

            if hearts <= 0:
                game_state = "gameover"

        # Update bullets and check collisions
        player_rect = pygame.Rect(
            player_x, player_y,
            player_size, player_size
        )

        for bullet in bullets[:]:

            bullet[1] -= bullet_speed

            bullet_rect = pygame.Rect(
                int(bullet[0]) - 3,
                int(bullet[1]) - 3,
                6, 6
            )

            # Bullet hits monster
            if bullet_rect.colliderect(target):

                bullets.remove(bullet)
                score += 1

                play_hit_sound()

                if score >= MAX_ROUNDS:
                    game_state = "win"
                else:
                    reset_target()

                continue

            # Remove bullets outside the screen
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Keyboard shortcut to pause
        if keys[pygame.K_ESCAPE]:
            game_state = "pause"

    # --------------------------------------
    # PAUSE MENU
    # --------------------------------------
    elif game_state == "pause":

        draw_game()

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(
            "PAUSED",
            big_font,
            YELLOW,
            WIDTH // 2,
            100
        )

        resume_rect = pygame.Rect(
            WIDTH // 2 - 100, 150, 200, 40
        )

        menu_rect = pygame.Rect(
            WIDTH // 2 - 100, 205, 200, 40
        )

        exit_rect = pygame.Rect(
            WIDTH // 2 - 100, 260, 200, 40
        )

        draw_button(
            "RESUME",
            resume_rect,
            GREEN,
            mouse_pos
        )

        draw_button(
            "MAIN MENU",
            menu_rect,
            BLUE,
            mouse_pos
        )

        draw_button(
            "EXIT",
            exit_rect,
            RED,
            mouse_pos
        )

    # --------------------------------------
    # WIN SCREEN
    # --------------------------------------
    elif game_state == "win":

        screen.blit(background, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(
            "YOU WIN!",
            big_font,
            GREEN,
            WIDTH // 2,
            100
        )

        draw_text(
            f"Final Score: {score}/{MAX_ROUNDS}",
            font,
            WHITE,
            WIDTH // 2,
            155
        )

        for i in range(hearts):
            draw_heart(
                WIDTH // 2 - (hearts - 1) * 15 + i * 30,
                195,
                25
            )

        again_rect = pygame.Rect(
            WIDTH // 2 - 100, 230, 200, 40
        )

        menu_rect = pygame.Rect(
            WIDTH // 2 - 100, 280, 200, 40
        )

        draw_button(
            "PLAY AGAIN",
            again_rect,
            GREEN,
            mouse_pos
        )

        draw_button(
            "MAIN MENU",
            menu_rect,
            BLUE,
            mouse_pos
        )

    # --------------------------------------
    # GAME OVER SCREEN
    # --------------------------------------
    elif game_state == "gameover":

        screen.blit(background, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(190)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        draw_text(
            "GAME OVER",
            big_font,
            RED,
            WIDTH // 2,
            100
        )

        draw_text(
            f"Final Score: {score}/{MAX_ROUNDS}",
            font,
            WHITE,
            WIDTH // 2,
            155
        )

        again_rect = pygame.Rect(
            WIDTH // 2 - 100, 210, 200, 40
        )

        menu_rect = pygame.Rect(
            WIDTH // 2 - 100, 265, 200, 40
        )

        draw_button(
            "TRY AGAIN",
            again_rect,
            GREEN,
            mouse_pos
        )

        draw_button(
            "MAIN MENU",
            menu_rect,
            BLUE,
            mouse_pos
        )

    # ======================================
    # 7. EVENT HANDLING
    # ======================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if game_state == "game":
                    game_state = "pause"

                elif game_state == "pause":
                    game_state = "game"

                elif game_state == "options":
                    game_state = "menu"

            # Shoot using SPACE
            if (
                event.key == pygame.K_SPACE
                and game_state == "game"
            ):
                bullets.append([
                    player_x + player_size // 2,
                    player_y
                ])

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                continue

            mx, my = event.pos

            # Main menu buttons
            if game_state == "menu":

                if new_game_rect.collidepoint(mx, my):
                    start_new_game()

                elif options_rect.collidepoint(mx, my):
                    game_state = "options"

                elif exit_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

            # Options buttons
            elif game_state == "options":

                if music_rect.collidepoint(mx, my):
                    toggle_music()

                elif sound_rect.collidepoint(mx, my):
                    toggle_sound()

                elif back_rect.collidepoint(mx, my):
                    game_state = "menu"

            # Game controls
            elif game_state == "game":

                if pause_rect.collidepoint(mx, my):
                    game_state = "pause"

                else:
                    # Shoot with mouse
                    bullets.append([
                        player_x + player_size // 2,
                        player_y
                    ])

            # Pause buttons
            elif game_state == "pause":

                if resume_rect.collidepoint(mx, my):
                    game_state = "game"

                elif menu_rect.collidepoint(mx, my):
                    game_state = "menu"

                elif exit_rect.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

            # Win buttons
            elif game_state == "win":

                if again_rect.collidepoint(mx, my):
                    start_new_game()

                elif menu_rect.collidepoint(mx, my):
                    game_state = "menu"

            # Game over buttons
            elif game_state == "gameover":

                if again_rect.collidepoint(mx, my):
                    start_new_game()

                elif menu_rect.collidepoint(mx, my):
                    game_state = "menu"

    pygame.display.flip()
    clock.tick(60)