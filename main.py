import asyncio

from attributes import Derrick, Cloud, Tree, FlyingCat, RunningCat
import pygame
import sys
import random

pygame.init()

game_speed = 5
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

icon = pygame.image.load('favicon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Derrick's Snowboard Adventures")
game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 26)
game_small_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)


# Objects
tree_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
derrick_group = pygame.sprite.GroupSingle()

derrick = Derrick(200, 360)
derrick_group.add(derrick)

# Surfaces
ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 360))
ground_x = 0
ground_y = 400
ground_rect = ground.get_rect(center=(640, 400))

# Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.ogg")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.ogg")

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 700)


TREE_EVENT = pygame.USEREVENT
pygame.time.set_timer(TREE_EVENT, random.randint(
    500, 1300))  # Random interval


def reset_tree_timer():
    pygame.time.set_timer(TREE_EVENT, random.randint(
        500, 1300))   # Randomize next tree


def reset_obstacles():
    global obstacle_timer, obstacle_spawn, last_obstacle_x, obstacle_cooldown, max_gap
    last_obstacle_x = random.randint(700, 1000)
    max_gap = 100


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 100))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 140))
    restart_text = game_small_font.render(
        "Press any key to restart game", True, "gray")
    restart_text_rect = restart_text.get_rect(center=(640, 190))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_text_rect)

    game_speed = 5
    tree_group.empty()
    cloud_group.empty()
    obstacle_group.empty()
    reset_obstacles()


# Initial value to prevent early overlap
last_obstacle_x = random.randint(700, 1000)
min_gap = 30  # Minimum distance between obstacles
max_gap = 100  # Maximum spacing for variety


def spawn_obstacle():
    global obstacle_timer, obstacle_spawn, last_obstacle_x, obstacle_cooldown, max_gap

    if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
        obstacle_spawn = True

        # Reduce obstacle cooldown as the game progresses
        # Prevent it from getting too fast
        if obstacle_cooldown > 500:
            obstacle_cooldown -= 1
        if max_gap > min_gap + 5:
            max_gap -= 0.08

    if obstacle_spawn:
        # Calculate the next obstacle position based on the last obstacle
        spawn_x = last_obstacle_x + random.randint(min_gap, int(max_gap))

        obstacle_random = random.randint(1, 50)
        if obstacle_random in range(1, 8):
            # Running cat at ground level
            new_obstacle = RunningCat(spawn_x, 380)
            obstacle_group.add(new_obstacle)

            # Update last obstacle position
            last_obstacle_x = spawn_x
            obstacle_timer = pygame.time.get_ticks()
            obstacle_spawn = False
        elif obstacle_random in range(30, 34):
            # Flying cat at a random height
            new_obstacle = FlyingCat(spawn_x)
            obstacle_group.add(new_obstacle)

            # Update last obstacle position
            last_obstacle_x = spawn_x
            obstacle_timer = pygame.time.get_ticks()
            obstacle_spawn = False


async def main():
    global game_speed, player_score, game_over, obstacle_timer, obstacle_spawn, obstacle_cooldown, ground_x

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            derrick.duck()
        elif keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            derrick.jump()
        else:
            if derrick.ducking:
                derrick.unduck()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == CLOUD_EVENT:
                current_cloud_y = random.randint(50, 300)
                current_cloud = Cloud(1380, current_cloud_y)
                cloud_group.add(current_cloud)
            if event.type == TREE_EVENT:
                if random.random() < 0.6:  # 60% chance to spawn a tree
                    current_tree = Tree()
                    tree_group.add(current_tree)

                reset_tree_timer()  # Set the next random tree event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    derrick.jump()
                    if game_over:
                        game_over = False
                        game_speed = 5
                        player_score = 0

        # Collisions
        if pygame.sprite.spritecollide(derrick_group.sprite, obstacle_group, False):
            game_over = True
            death_sfx.play()
        if game_over:
            end_game()

        if not game_over:
            screen.fill("#EAF7FF")

            game_speed += 0.0005
            if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
                points_sfx.play()

            spawn_obstacle()

            screen.blit(ground, (ground_x, ground_y))
            screen.blit(ground, (ground_x + 1280, ground_y))

            if ground_x <= -1280:
                ground_x = 0

            cloud_group.update()
            cloud_group.draw(screen)

            tree_group.update()
            tree_group.draw(screen)

            derrick_group.update()
            derrick_group.draw(screen)

            obstacle_group.update()
            obstacle_group.draw(screen)

            player_score += 0.1
            player_score_surface = game_font.render(
                str(int(player_score)), True, ("black"))
            screen.blit(player_score_surface, (1150, 10))

            ground_x -= game_speed

        clock.tick(120)
        pygame.display.update()

        await asyncio.sleep(0)


# This is the program entry point:
asyncio.run(main())

# Do not add anything from here, especially sys.exit/pygame.quit
# asyncio.run is non-blocking on pygame-wasm and code would be executed
# right before program start main()
