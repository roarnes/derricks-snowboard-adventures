import pygame
import random

game_speed = 5


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1380

        original_image = pygame.image.load("assets/tree.png")
        original_width, original_height = original_image.get_size()

        fixed_height = random.randint(80, 200)  # Set fixed height
        aspect_ratio = original_width / original_height  # Calculate aspect ratio
        new_width = int(fixed_height * aspect_ratio)

        # Ensure the tree bottom is always at y = 360
        self.y_pos = 400 - (fixed_height // 2)

        self.image = pygame.transform.scale(
            original_image, (new_width, fixed_height))

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        # self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.sprites = []
        for i in range(1, 7):
            original_image = pygame.image.load(
                f"assets/clouds/cloud{i}.png")

            original_width, original_height = original_image.get_size()

            fixed_height = random.randint(20, 80)  # Set fixed height
            aspect_ratio = original_width / original_height  # Calculate aspect ratio
            # Scale width proportionally
            new_width = int(fixed_height * aspect_ratio)

            scaled_sprite = pygame.transform.scale(
                original_image, (new_width, fixed_height))
            self.sprites.append(scaled_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        # self.x_pos -= game_speed
        self.rect.x -= 1


class Derrick(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        self.ride_img = pygame.transform.scale(
            pygame.image.load("assets/Ride.png"), (80, 120))
        self.jump_img = pygame.transform.scale(
            pygame.image.load(f"assets/Jump.png"), (80, 120))
        self.duck_img = pygame.transform.scale(
            pygame.image.load(f"assets/Duck.png"), (95, 95))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = 0
        self.image = self.ride_img
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 20
        # self.gravity = 3
        self.ducking = False
        self.jumping = False

    def jump(self):
        if not self.jumping and self.rect.centery == 360:  # Allow jump only if on ground
            self.jumping = True
            # Start with an initial negative velocity (jump impulse)
            self.velocity = -8
            jump_sfx = pygame.mixer.Sound("assets/sfx/jump.ogg")
            jump_sfx.play()

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360

    def apply_gravity(self):

        if self.jumping:
            self.rect.centery += self.velocity  # Move up or down
            self.velocity += 0.3  # Simulate gravity

            if self.rect.centery >= 360:  # If Derrick lands back
                self.rect.centery = 360
                self.jumping = False  # Reset jumping state
                self.velocity = 0  # Reset velocity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        if self.ducking:
            self.image = self.duck_img
        elif self.jumping:
            self.image = self.jump_img
        else:
            self.image = self.ride_img


class RunningCat(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()

        # Load sprite animations
        self.buttface_sprites = [
            pygame.transform.scale(pygame.image.load(f"assets/Buttface{i}.png"), (55, 55)) for i in range(1, 3)
        ]
        self.dumdum_sprites = [
            pygame.transform.scale(pygame.image.load(f"assets/Dumdum{i}.png"), (55, 55)) for i in range(1, 3)
        ]

        # Store animations separately
        self.sprites = [self.dumdum_sprites, self.buttface_sprites]
        self.current_sprite_index = random.randint(0, 1)
        self.current_image_index = 0  # Current frame in animation

        self.x_pos = x_pos
        self.y_pos = y_pos

        # Set initial image
        self.image = self.sprites[self.current_sprite_index][self.current_image_index]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        # Animation timers
        self.animation_speed = 0.05  # Adjust speed of animation
        self.frame_timer = 0  # Timer for frame animation

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect.center = (self.x_pos, self.y_pos)

    def animate(self):
        # Animate the selected sprite set
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:  # Adjust for smooth animation
            self.frame_timer = 0
            self.current_image_index = (
                self.current_image_index + 1) % len(self.sprites[self.current_sprite_index])

        # Update sprite image
        self.image = self.sprites[self.current_sprite_index][self.current_image_index]


class FlyingCat(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = random.choice([265, 275, 290])

        # Load sprite animations
        self.buttface_sprites = [
            pygame.transform.scale(pygame.image.load(f"assets/ButtfaceFly{i}.png"), (55, 55)) for i in range(1, 3)
        ]
        self.dumdum_sprites = [
            pygame.transform.scale(pygame.image.load(f"assets/DumdumFly{i}.png"), (55, 55)) for i in range(1, 3)
        ]

        # Store animations separately
        self.sprites = [self.dumdum_sprites, self.buttface_sprites]
        self.current_sprite_index = random.randint(0, 1)
        self.current_image_index = 0  # Current frame in animation

        # Set initial image
        self.image = self.sprites[self.current_sprite_index][self.current_image_index]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.animation_speed = 0.05  # Adjust speed of animation
        self.frame_timer = 0  # Timer for frame animation

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect.center = (self.x_pos, self.y_pos)

    def animate(self):
        # Animate the selected sprite set
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:  # Adjust for smooth animation
            self.frame_timer = 0
            self.current_image_index = (
                self.current_image_index + 1) % len(self.sprites[self.current_sprite_index])

        # Update sprite image
        self.image = self.sprites[self.current_sprite_index][self.current_image_index]
