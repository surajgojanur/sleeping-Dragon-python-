import math
import pygame

WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
CENTER = (CENTER_X, CENTER_Y)
FONT_COLOR = (0, 0, 0)
EGG_TARGET = 20
HERO_START = (200, 300)
ATTACK_DISTANCE = 200
DRAGON_WAKE_TIME = 2
EGG_HIDE_TIME = 2
MOVE_DISTANCE = 5
lives = 3
eggs_collected = 0
game_over = False
game_complete = False
reset_required = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load your images here. Replace 'image_file.png' with actual file paths.
hero_image = pygame.image.load("C:/Users/suraj/OneDrive/Desktop/Dragons/images/hero.jpg")
dragon_asleep_image = pygame.image.load('dragon-asleep.png')
one_egg_image = pygame.image.load('one-egg.png')
two_eggs_image = pygame.image.load("C:\\Users\\suraj\\OneDrive\\Desktop\\Dragons\\images\\two-eggs.jpg")
three_eggs_image = pygame.image.load('three-eggs.png')

easy_lair = {
    "dragon": {"image": dragon_asleep_image, "rect": pygame.Rect(600, 100, 100, 100)},
    "eggs": {"image": one_egg_image, "rect": pygame.Rect(400, 100, 100, 100)},
    "egg_count": 1,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 10,
    "sleep_counter": 0,
    "wake_counter": 0
}

medium_lair = {
    "dragon": {"image": dragon_asleep_image, "rect": pygame.Rect(600, 300, 100, 100)},
    "eggs": {"image": two_eggs_image, "rect": pygame.Rect(400, 300, 100, 100)},
    "egg_count": 2,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 7,
    "sleep_counter": 0,
    "wake_counter": 0
}

hard_lair = {
    "dragon": {"image": dragon_asleep_image, "rect": pygame.Rect(600, 500, 100, 100)},
    "eggs": {"image": three_eggs_image, "rect": pygame.Rect(400, 500, 100, 100)},
    "egg_count": 3,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 4,
    "sleep_counter": 0,
    "wake_counter": 0
}

lairs = [easy_lair, medium_lair, hard_lair]

hero_rect = pygame.Rect(HERO_START[0], HERO_START[1], 100, 100)

def draw_lairs(lairs_to_draw):
    for lair in lairs_to_draw:
        screen.blit(lair["dragon"]["image"], lair["dragon"]["rect"])
        if not lair["egg_hidden"]:
            screen.blit(lair["eggs"]["image"], lair["eggs"]["rect"])

def draw_counters(eggs_collected, lives):
    font = pygame.font.Font(None, 36)
    egg_count_text = font.render(f'Eggs: {eggs_collected}', True, FONT_COLOR)
    life_count_text = font.render(f'Lives: {lives}', True, FONT_COLOR)
    screen.blit(egg_count_text, (10, 10))
    screen.blit(life_count_text, (10, 40))

def update():
    global hero_rect, game_over, game_complete
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        hero_rect.move_ip(MOVE_DISTANCE, 0)
    if keys[pygame.K_LEFT]:
        hero_rect.move_ip(-MOVE_DISTANCE, 0)
    if keys[pygame.K_DOWN]:
        hero_rect.move_ip(0, MOVE_DISTANCE)
    if keys[pygame.K_UP]:
        hero_rect.move_ip(0, -MOVE_DISTANCE)
    
    check_for_collisions()

def update_lairs():
    global lairs, lives
    for lair in lairs:
        if lair["dragon"]["image"] == dragon_asleep_image:
            update_sleeping_dragon(lair)
        elif lair["dragon"]["image"] == dragon_awake_image:
            update_waking_dragon(lair)
        update_egg(lair)

def update_sleeping_dragon(lair):
    if lair["sleep_counter"] >= lair["sleep_length"]:
        lair["dragon"]["image"] = dragon_awake_image
        lair["sleep_counter"] = 0
    else:
        lair["sleep_counter"] += 1

def update_waking_dragon(lair):
    if lair["wake_counter"] >= DRAGON_WAKE_TIME:
        lair["dragon"]["image"] = dragon_asleep_image
        lair["wake_counter"] = 0
    else:
        lair["wake_counter"] += 1

def update_egg(lair):
    if lair["egg_hidden"]:
        if lair["egg_hide_counter"] >= EGG_HIDE_TIME:
            lair["egg_hidden"] = False
        lair["egg_hide_counter"] = 0
    else:
        lair["egg_hide_counter"] += 1

def check_for_collisions():
    global lairs, eggs_collected, lives, reset_required, game_complete
    for lair in lairs:
        if not lair["egg_hidden"]:
            check_for_egg_collision(lair)
        if lair["dragon"]["image"] == dragon_awake_image and not reset_required:
            check_for_dragon_collision(lair)

def check_for_dragon_collision(lair):
    x_distance = hero_rect.x - lair["dragon"]["rect"].x
    y_distance = hero_rect.y - lair["dragon"]["rect"].y
    distance = math.hypot(x_distance, y_distance)
    if distance < ATTACK_DISTANCE:
        handle_dragon_collision()

def handle_dragon_collision():
    global reset_required
    reset_required = True
    hero_rect.topleft = HERO_START
    subtract_life()

def check_for_egg_collision(lair):
    global eggs_collected, game_complete
    if hero_rect.colliderect(lair["eggs"]["rect"]):
        lair["egg_hidden"] = True
        eggs_collected += lair["egg_count"]
        if eggs_collected >= EGG_TARGET:
            game_complete = True

def subtract_life():
    global lives, reset_required, game_over
    lives -= 1
    if lives == 0:
        game_over = True
        reset_required = False

running = True
