import pygame
from board import boards
import math
import copy
pygame.init()

# Scale factor to fit smaller screens
SCALE_FACTOR = 0.65

# Original dimensions
ORIGINAL_WIDTH = 900
ORIGINAL_HEIGHT = 950

# New scaled dimensions
WIDTH = int(ORIGINAL_WIDTH * SCALE_FACTOR)
HEIGHT = int(ORIGINAL_HEIGHT * SCALE_FACTOR)

PI = math.pi
# Color variable for the color of walls
color = 'blue'
# Screen display
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Speed at which game runs
timer = pygame.time.Clock()

# Max speed 
fps = 60

# Font for score game over etc - scale font size
font = pygame.font.Font('freesansbold.ttf', int(20 * SCALE_FACTOR))

# Later on will alter this to list and make different levels boards[activelevels]
level = copy.deepcopy(boards)
player_images = []
# Because 4 players animation of pacman
for i in range(1, 5):
    # Load and scale the image with our scale factor
    image_size = int(45 * SCALE_FACTOR)
    player_images.append(pygame.transform.scale(pygame.image.load(f'images/player_images/{i}.png'), (image_size, image_size)))

# Ghost images - scaled
ghost_size = int(45 * SCALE_FACTOR)
# Red one
blinky_img = pygame.transform.scale(pygame.image.load(f'images/ghost_images/red.png'), (ghost_size, ghost_size))
# Pink one
pinky_img = pygame.transform.scale(pygame.image.load(f'images/ghost_images/pink.png'), (ghost_size, ghost_size))
# Blue one
inky_img = pygame.transform.scale(pygame.image.load(f'images/ghost_images/blue.png'), (ghost_size, ghost_size))
# Orange one
clyde_img = pygame.transform.scale(pygame.image.load(f'images/ghost_images/orange.png'), (ghost_size, ghost_size))
# Powerup Frightened to be eaten
spooked_img = pygame.transform.scale(pygame.image.load(f'images/ghost_images/powerup.png'), (ghost_size, ghost_size))
# Eaten and returning to box
dead_img = pygame.transform.scale(pygame.image.load(f'images/ghost_images/dead.png'), (ghost_size, ghost_size))

"""
Ghost Classification
Red---------->Blinky
Pink--------->Pinky
Blue--------->Inky
Orange------->Clyde
Blue Fright-->Spooked
Eyes--------->Dead
"""

# Scale initial positions
# Starting position initially for pacman
player_x = int(450 * SCALE_FACTOR)
player_y = int(663 * SCALE_FACTOR)

# Starting positions for ghosts (scaled)
blinky_x = int(56 * SCALE_FACTOR)
blinky_y = int(58 * SCALE_FACTOR)
blinky_direction = 0
inky_x = int(440 * SCALE_FACTOR)
inky_y = int(388 * SCALE_FACTOR)
inky_direction = 2
pinky_x = int(440 * SCALE_FACTOR)
pinky_y = int(438 * SCALE_FACTOR)
pinky_direction = 2
clyde_x = int(440 * SCALE_FACTOR)
clyde_y = int(438 * SCALE_FACTOR)
clyde_direction = 2

# Only blinky starts outside of the box rest inside the box and move up
# Simple Directions
direction = 0
# Pac-Man Animation Variable
counter = 0
# Flicker For the power ups feel Lively
flicker = False
# Valid turns R L U D By Default
turns_allowed = [False, False, False, False]
# For more of classic joystick functionality
direction_command = 0
# Pac Man speed (scaled)
player_speed = 2
# Ofcourse Score
score = 0
# Powerup, Timer, Ghosts Eaten
powerup = False
power_counter = 0
eaten_ghosts = [False, False, False, False]
# Targets for the ghosts may change like to scatter, catch etc
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
# If ghosts dead variable
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
# Inside Box or not variable
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
# Speed Of the ghost (scaled)
ghost_speeds = [int(2 * SCALE_FACTOR) if int(2 * SCALE_FACTOR) > 0 else 1] * 4
startup_counter = 0
lives = 3
game_over = False
game_won = False

#Delay At start and if moving
startup_counter=0
moving=False
#Lives
lives=3

# Add a revival counter for each ghost at the top with other variables
blinky_revival_counter = 0
inky_revival_counter = 0
pinky_revival_counter = 0
clyde_revival_counter = 0

# Class for ghosts
class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        # Basic Attributes Coordinates, target, speed, image, direction, dead, box id(0-3)
        self.x_pos = x_coord
        self.y_pos = y_coord
        # Update center calculation to prevent index errors
        self.center_x = self.x_pos + int(22 * SCALE_FACTOR)
        self.center_y = self.y_pos + int(22 * SCALE_FACTOR)
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        # By position on the board to see some stuff
        self.turns, self.in_box = self.check_collisions()
        # For player colliding with pacman with the circle of the pacman and rectangle of the ghost
        self.rect = self.draw()
   
    def draw(self):
        # Lots Of conditions to take into consideration
        # Drawing Normal Ghost Base Image
        """
        1----No powerup Not dead
        2----Eaten (id) powerup On Not dead
        (Means did not comeback to the box)
        """
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        # Spooked Image
        elif (powerup and not self.dead and not eaten_ghosts[self.id]):
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        # Dead / Eaten
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        # Hitbox - scaled
        ghost_rect_size = int(36 * SCALE_FACTOR)
        ghost_rect_offset = int(18 * SCALE_FACTOR)
        ghost_rect = pygame.rect.Rect((self.center_x - ghost_rect_offset, self.center_y - ghost_rect_offset), (ghost_rect_size, ghost_rect_size))
        return ghost_rect

    def check_collisions(self):
        num1 = ((HEIGHT - int(50 * SCALE_FACTOR)) // 32)
        num2 = (WIDTH // 30)
        num3 = int(12 * SCALE_FACTOR)
        self.turns = [False, False, False, False]

        if 0 < self.center_x // num2 < 29:
            # Check all four directions for normal movement OR gate
            # Right
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or level[self.center_y // num1][(self.center_x + num3) // num2] == 9:
                self.turns[0] = True
            # Left
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or level[self.center_y // num1][(self.center_x - num3) // num2] == 9:
                self.turns[1] = True
            # Up
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            # Down
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or level[(self.center_y + num3) // num1][self.center_x // num2] == 9:
                self.turns[3] = True

            # Check for turns at intersections
            if self.direction == 2 or self.direction == 3:
                if 8 <= self.center_x % num2 <= 22:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or level[(self.center_y + num3) // num1][self.center_x // num2] == 9:
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 22:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3:
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3:
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 8 <= self.center_x % num2 <= 22:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or level[(self.center_y + num3) // num1][self.center_x // num2] == 9:
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                        self.turns[2] = True
                if 8 <= self.center_y % num1 <= 22:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3:
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3:
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        # Check if inside box
        box_left = int(350 * SCALE_FACTOR)
        box_right = int(550 * SCALE_FACTOR)
        box_top = int(370 * SCALE_FACTOR)
        box_bottom = int(480 * SCALE_FACTOR)

        if box_left < self.x_pos < box_right and box_top < self.y_pos < box_bottom:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    # The ghost movement logic remains the same, only the scaled variables are different
    def move_clyde(self):
        # clyde is going to turn whenever advantageous for pursuit
        # Moving Right and target is x and y coordinate pair
        if self.direction == 0:
            # If moving right then keep going right
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            # Going right but there was a collision 
            elif not self.turns[0]:
                # Logical Turns
                # Move Down if target down
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                # Move up if target up
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                # Move left if target behind
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                # Creator Preference again preference D-->U-->L
                # No Logical turns
                # For example target=right or above and cant move there so we have to give it direction
                # Move Down
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                # Move Up
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                # Move Left
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            # Going right but target not there
            elif self.turns[0]:
                # Going right but target not there but constant check up and down for better position
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                # Else moving right like he did
                else:
                    self.x_pos += self.speed
        # Same thing of left direction
        elif self.direction == 1:
            # Going left move down to proceed to target
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            # Going left then go left if beneficial
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            # If going left but collision on left
            elif not self.turns[1]:
                # Target below 
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                # Then go upwards
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                # Lastly we would go left 
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                # Non logical More of priority on user 
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        # Going Upwards
        elif self.direction == 2:
            # Go left if going upwards
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            # Going up if target above you
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        # Again same stuff if going x the go x/y
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            # The preference thing again if going down our choice
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        # Going outside - scale boundary checks
        if self.x_pos < -int(30 * SCALE_FACTOR):
            self.x_pos = int(900 * SCALE_FACTOR)
        elif self.x_pos > int(900 * SCALE_FACTOR):
            self.x_pos = -int(30 * SCALE_FACTOR)

        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        # Scale boundary checks
        if self.x_pos < -int(30 * SCALE_FACTOR):
            self.x_pos = int(900 * SCALE_FACTOR)
        elif self.x_pos > int(900 * SCALE_FACTOR):
            self.x_pos = -int(30 * SCALE_FACTOR)

        return self.x_pos, self.y_pos, self.direction
    
    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
                
        # Scale boundary checks
        screen_width = int(900 * SCALE_FACTOR)
        screen_edge = int(15 * SCALE_FACTOR)
        if self.x_pos < -int(30 * SCALE_FACTOR):
            self.x_pos = int(900 * SCALE_FACTOR)
        elif self.x_pos > int(900 * SCALE_FACTOR):
            self.x_pos = -int(30 * SCALE_FACTOR)
        
        return self.x_pos, self.y_pos, self.direction
    
    def move_pinky(self):
        # r, l, u, d
        # pinky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
                
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
                
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
                    
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
                    
        # Scale boundary checks
        if self.x_pos < -int(30 * SCALE_FACTOR):
            self.x_pos = int(900 * SCALE_FACTOR)
        elif self.x_pos > int(900 * SCALE_FACTOR):
            self.x_pos = -int(30 * SCALE_FACTOR)
            
        return self.x_pos, self.y_pos, self.direction
    

def draw_misc():
    score_text = font.render(f'Score:{score}', True, 'white')
    screen.blit(score_text, (int(10 * SCALE_FACTOR), int(920 * SCALE_FACTOR)))

    if powerup:
        # White circle indicator
        pygame.draw.circle(screen, 'white', (int(140 * SCALE_FACTOR), int(930 * SCALE_FACTOR)), int(15 * SCALE_FACTOR))

        # Power-up timer bar
        timer_width = int(200 * SCALE_FACTOR)
        timer_height = int(10 * SCALE_FACTOR)
        timer_x = int(170 * SCALE_FACTOR)  # Positioned after the circle
        timer_y = int(925 * SCALE_FACTOR)  # Centered vertically with the circle

        # Background of timer (grey)
        pygame.draw.rect(screen, 'grey', (timer_x, timer_y, timer_width, timer_height))

        # Remaining time (white)
        remaining = (600 - power_counter) / 600  # Percentage remaining
        pygame.draw.rect(screen, 'white', (timer_x, timer_y, int(timer_width * remaining), timer_height))

    
    for i in range(lives):
        life_img_size = int(30 * SCALE_FACTOR)
        screen.blit(pygame.transform.scale(player_images[0], (life_img_size, life_img_size)), 
                   (int((650 + i * 40) * SCALE_FACTOR), int(915 * SCALE_FACTOR)))
    
    if game_over:
        pygame.draw.rect(screen, 'white', [int(50 * SCALE_FACTOR), int(200 * SCALE_FACTOR), 
                                          int(800 * SCALE_FACTOR), int(300 * SCALE_FACTOR)], 0, int(10 * SCALE_FACTOR))
        pygame.draw.rect(screen, 'dark gray', [int(70 * SCALE_FACTOR), int(220 * SCALE_FACTOR), 
                                              int(760 * SCALE_FACTOR), int(260 * SCALE_FACTOR)], 0, int(10 * SCALE_FACTOR))
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (int(100 * SCALE_FACTOR), int(300 * SCALE_FACTOR)))
    
    if game_won:
        pygame.draw.rect(screen, 'white', [int(50 * SCALE_FACTOR), int(200 * SCALE_FACTOR), 
                                          int(800 * SCALE_FACTOR), int(300 * SCALE_FACTOR)], 0, int(10 * SCALE_FACTOR))
        pygame.draw.rect(screen, 'dark gray', [int(70 * SCALE_FACTOR), int(220 * SCALE_FACTOR), 
                                              int(760 * SCALE_FACTOR), int(260 * SCALE_FACTOR)], 0, int(10 * SCALE_FACTOR))
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (int(100 * SCALE_FACTOR), int(300 * SCALE_FACTOR)))


def check_collisions(s, power, power_count, eaten_ghosts):
    # Out Of Bounds
    num1 = (HEIGHT - int(50 * SCALE_FACTOR)) // 32
    num2 = (WIDTH // 30)

    # Prevent out of bounds errors
    if 0 < player_x < int(900 * SCALE_FACTOR):
        # Check if cell indices are valid before accessing
        cell_y = center_y // num1
        cell_x = center_x // num2

        # Ensure indices are within bounds
        if 0 <= cell_y < len(level) and 0 <= cell_x < len(level[0]):
            # Food
            if level[cell_y][cell_x] == 1:
                level[cell_y][cell_x] = 0
                s = s + 10
            # PowerUp
            if level[cell_y][cell_x] == 2:
                level[cell_y][cell_x] = 0
                s = s + 50
                power = True
                # Resetting the powerup counter for the new powerup timer
                power_count = 0
                eaten_ghosts = [False, False, False, False]

    return s, power, power_count, eaten_ghosts

def draw_board(lvl):
    # 50 Pixel Padding for the score etc actual board 900x900 
    # 32 vertical numbers (Items)
    # 30 horizontal numbers (Items)
    num1 = ((HEIGHT - int(50 * SCALE_FACTOR)) // 32)
    num2 = (WIDTH // 30)
    
    # Using floor division so int number returned
    for i in range(len(lvl)):
        # Row Loop
        for j in range(len(lvl[i])):
            # by default 0 then black space
            if lvl[i][j] == 1:
                # X Y center coordinate j*num2=x coordinate +(0.5+num2) to center it
                # Line thickness last argument  
                pygame.draw.circle(screen, 'white', 
                                  (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 
                                  int(4 * SCALE_FACTOR))
                
            if lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', 
                                  (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 
                                  int(10 * SCALE_FACTOR))
                
            if lvl[i][j] == 3:
                # For line we will give starting position and ending position(via coordinates)
                pygame.draw.line(screen, color, 
                                (j * num2 + (0.5 * num2), i * num1), 
                                (j * num2 + (0.5 * num2), i * num1 + num1), 
                                int(3 * SCALE_FACTOR))
                
            if lvl[i][j] == 4:
                pygame.draw.line(screen, color, 
                                (j * num2, i * num1 + (0.5 * num1)), 
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 
                                int(3 * SCALE_FACTOR))                     
                
            if lvl[i][j] == 5:
                # Why arc because they are occupying 1/4 th of a circle
                # Start and end position in terms of PI sin curve
                pygame.draw.arc(screen, color, 
                               [(j * num2 - (num2 * 0.4)) - int(2 * SCALE_FACTOR), 
                                (i * num1 + (0.5 * num1)), num2, num1], 
                               0, PI / 2, 
                               int(3 * SCALE_FACTOR))
                
            if lvl[i][j] == 6:  
                pygame.draw.arc(screen, color, 
                               [(j * num2 + (num2 * 0.5)), 
                                (i * num1 + (0.5 * num1)), num2, num1], 
                               PI / 2, PI, 
                               int(3 * SCALE_FACTOR))
                
            if lvl[i][j] == 7:  
                pygame.draw.arc(screen, color, 
                               [(j * num2 + (num2 * 0.5)), 
                                (i * num1 - (0.4 * num1)), num2, num1], 
                               PI, 3 * PI / 2, 
                               int(3 * SCALE_FACTOR))
                
            if lvl[i][j] == 8:  
                pygame.draw.arc(screen, color, 
                               [(j * num2 - (num2 * 0.4)) - int(2 * SCALE_FACTOR), 
                                (i * num1 - (0.4 * num1)), num2, num1], 
                               3 * PI / 2, 2 * PI, 
                               int(3 * SCALE_FACTOR))
                
            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', 
                                (j * num2, i * num1 + (0.5 * num1)), 
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 
                                int(3 * SCALE_FACTOR))
            # Behaviour of 8 similar to 5

def draw_player():
    # 4 directions
    """
    Directions For Movements
    0----RIGHT
    1----LEFT
    2----UP
    3----DOWN
    """
    # Depending on speed animation so different motions for different time frame
    # Flipping in either x direction or y direction True False right-left
    # Rotating in the basis of angles 90 or 270 up-down    
    if direction == 0:     
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_positions(centerx, centery):
    turns = [False, False, False, False]
    # Calculate grid parameters
    num1 = (HEIGHT - int(50 * SCALE_FACTOR)) // 32
    num2 = (WIDTH // 30)
    num3 = int(12 * SCALE_FACTOR)  # Fudge factor

    # Check if within board boundaries
    if 0 < centerx // num2 < 29:
        # Check what's allowed in each direction based on current position
        # First, check if we can continue in current direction
        if level[centery // num1][(centerx + num3) // num2] < 3:
            turns[0] = True  # Right
        if level[centery // num1][(centerx - num3) // num2] < 3:
            turns[1] = True  # Left
        if level[(centery - num3) // num1][centerx // num2] < 3:
            turns[2] = True  # Up
        if level[(centery + num3) // num1][centerx // num2] < 3:
            turns[3] = True  # Down

        # Check for turns at intersections
        if direction == 2 or direction == 3:  # Moving up/down
            if 8 <= centerx % num2 <= 22:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 8 <= centery % num1 <= 22:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:  # Moving left/right
            if 8 <= centerx % num2 <= 22:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 8 <= centery % num1 <= 22:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        # Allow wrapping around screen edges
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x = play_x + player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x = play_x - player_speed
    elif direction == 2 and turns_allowed[2]:
        play_y = play_y - player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y = play_y + player_speed
    
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    # Scale coordinates
    screen_width = int(900 * SCALE_FACTOR)
    half_screen = int(450 * SCALE_FACTOR)

    # Runaway positions for powerup
    if player_x < half_screen:
        runaway_x = screen_width
    else:
        runaway_x = 0
    if player_y < half_screen:
        runaway_y = screen_width
    else:
        runaway_y = 0

    # Target positions
    return_target = (int(400 * SCALE_FACTOR), int(435 * SCALE_FACTOR))  # Deep inside box
    exit_point = (int(400 * SCALE_FACTOR), int(320 * SCALE_FACTOR))  # Above the gate

    # Box boundaries
    box_left = int(340 * SCALE_FACTOR)
    box_right = int(560 * SCALE_FACTOR)
    box_top = int(388 * SCALE_FACTOR)
    box_bottom = int(480 * SCALE_FACTOR)

    # Blinky
    if blinky_dead:
        blink_target = return_target  # Go to center when dead
    elif blinky.in_box and not blinky_dead and not blinky_dead:
        blink_target = exit_point  # Exit when alive and in box
    elif powerup and not eaten_ghosts[0]:
        blink_target = (runaway_x, runaway_y)
    else:
        blink_target = (player_x, player_y)

    # Inky
    if inky_dead:
        ink_target = return_target
    elif inky.in_box and not inky_dead:
        ink_target = exit_point
    elif powerup and not eaten_ghosts[1]:
        ink_target = (runaway_x, player_y)
    else:
        ink_target = (player_x, player_y)

    # Pinky
    if pinky_dead:
        pink_target = return_target
    elif pinky.in_box and not pinky_dead:
        pink_target = exit_point
    elif powerup and not eaten_ghosts[2]:
        pink_target = (player_x, runaway_y)
    else:
        pink_target = (player_x, player_y)

    # Clyde
    if clyde_dead:
        clyd_target = return_target
    elif clyde.in_box and not clyde_dead:
        clyd_target = exit_point
    elif powerup and not eaten_ghosts[3]:
        clyd_target = (half_screen, half_screen)
    else:
        clyd_target = (player_x, player_y)

    return [blink_target, ink_target, pink_target, clyd_target]

# Game loop everything we want to execute when the game runs
run = True
while run: 
    timer.tick(fps) # set fps
    """
    To control the speed of pacman we can change the counter variable
    or the constant variable 5 (By Default) which is used in draw_player
    function
    1----counter check
    2----counter//const

    To control the animation speed for powerups
    1----Change the constant counter>const
    2----Or make another counter condition 
    """
    if counter < 19:
        counter = counter + 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    # Powerup active and counter less than 10sec 600/60fps
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghosts = [False, False, False, False]
    # 3 sec delay to see the board initially
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True
    screen.fill('black') # Solid colour black for background
    draw_board(level)
    # Just scaling midpoint
    ###
    center_x = player_x + int(22.5 * SCALE_FACTOR)
    center_y = player_y + int(22.5 * SCALE_FACTOR)
    # Change speed as per powerup and death
    if powerup:
        ghost_speeds = [1] * 4  # Slow speed when power-up
    else:
        ghost_speeds = [2] * 4  # Normal speed

    if blinky_dead:
        ghost_speeds[0] = 4  # Faster when returning
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4
    # For Winning
    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), int(20 * SCALE_FACTOR), 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)
    if inky.in_box and not inky_dead:
        inky_direction = 2  # Face up to exit
    if pinky.in_box and not pinky_dead:
        pinky_direction = 2  # Face up to exit
    if clyde.in_box and not clyde_dead:
        clyde_direction = 2  # Face up to exit



    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    blinky.target = targets[0]
    inky.target = targets[1]
    pinky.target = targets[2]
    clyde.target = targets[3]

    draw_misc()

    # Check Position on board check certain action or position is allowed
    turns_allowed = check_positions(center_x, center_y)

    if moving:
        # Movement Of Pac Man
        player_x, player_y = move_player(player_x, player_y)

        # For Blinky
        if blinky_dead or blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()

        # For Inky
        if inky_dead or inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        else:
            inky_x, inky_y, inky_direction = inky.move_inky()

        # For Pinky
        if pinky_dead or pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()

        # For Clyde - always uses move_clyde
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        
    # Score
    score, powerup, power_counter, eaten_ghosts = check_collisions(score, powerup, power_counter, eaten_ghosts)
    # Collision between ghost rectangle and pac man circle
    if not powerup:
        # If collide and not dead
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or\
           (player_circle.colliderect(inky.rect) and not inky.dead) or\
           (player_circle.colliderect(pinky.rect) and not pinky.dead) or\
           (player_circle.colliderect(clyde.rect) and not clyde.dead):
            # 3 lives
            if lives > 0:
                lives -= 1
                powerup = False
                power_counter = 0
                startup_counter = 0
                # Positions and deaths reset
                player_x = int(450 * SCALE_FACTOR)
                player_y = int(663 * SCALE_FACTOR)
                direction = 0
                direction_command = 0
                blinky_x = int(56 * SCALE_FACTOR)
                blinky_y = int(58 * SCALE_FACTOR)
                blinky_direction = 0
                inky_x = int(440 * SCALE_FACTOR)
                inky_y = int(388 * SCALE_FACTOR)
                inky_direction = 2
                pinky_x = int(440 * SCALE_FACTOR)
                pinky_y = int(438 * SCALE_FACTOR)
                pinky_direction = 2
                clyde_x = int(440 * SCALE_FACTOR)
                clyde_y = int(438 * SCALE_FACTOR)
                clyde_direction = 2
                eaten_ghosts = [False, False, False, False]            
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
                
    # Not running into eye balls which are already dead and resetting
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghosts[0] and not blinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = int(450 * SCALE_FACTOR)
            player_y = int(663 * SCALE_FACTOR)
            direction = 0
            direction_command = 0
            blinky_x = int(56 * SCALE_FACTOR)
            blinky_y = int(58 * SCALE_FACTOR)
            blinky_direction = 0
            inky_x = int(440 * SCALE_FACTOR)
            inky_y = int(388 * SCALE_FACTOR)
            inky_direction = 2
            pinky_x = int(440 * SCALE_FACTOR)
            pinky_y = int(438 * SCALE_FACTOR)
            pinky_direction = 2
            clyde_x = int(440 * SCALE_FACTOR)
            clyde_y = int(438 * SCALE_FACTOR)
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
            
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghosts[1] and not inky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = int(450 * SCALE_FACTOR)
            player_y = int(663 * SCALE_FACTOR)
            direction = 0
            direction_command = 0
            blinky_x = int(56 * SCALE_FACTOR)
            blinky_y = int(58 * SCALE_FACTOR)
            blinky_direction = 0
            inky_x = int(440 * SCALE_FACTOR)
            inky_y = int(388 * SCALE_FACTOR)
            inky_direction = 2
            pinky_x = int(440 * SCALE_FACTOR)
            pinky_y = int(438 * SCALE_FACTOR)
            pinky_direction = 2
            clyde_x = int(440 * SCALE_FACTOR)
            clyde_y = int(438 * SCALE_FACTOR)
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
            
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghosts[2] and not pinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = int(450 * SCALE_FACTOR)
            player_y = int(663 * SCALE_FACTOR)
            direction = 0
            direction_command = 0
            blinky_x = int(56 * SCALE_FACTOR)
            blinky_y = int(58 * SCALE_FACTOR)
            blinky_direction = 0
            inky_x = int(440 * SCALE_FACTOR)
            inky_y = int(388 * SCALE_FACTOR)
            inky_direction = 2
            pinky_x = int(440 * SCALE_FACTOR)
            pinky_y = int(438 * SCALE_FACTOR)
            pinky_direction = 2
            clyde_x = int(440 * SCALE_FACTOR)
            clyde_y = int(438 * SCALE_FACTOR)
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
            
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghosts[3] and not clyde.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = int(450 * SCALE_FACTOR)
            player_y = int(663 * SCALE_FACTOR)
            direction = 0
            direction_command = 0
            blinky_x = int(56 * SCALE_FACTOR)
            blinky_y = int(58 * SCALE_FACTOR)
            blinky_direction = 0
            inky_x = int(440 * SCALE_FACTOR)
            inky_y = int(388 * SCALE_FACTOR)
            inky_direction = 2
            pinky_x = int(440 * SCALE_FACTOR)
            pinky_y = int(438 * SCALE_FACTOR)
            pinky_direction = 2
            clyde_x = int(440 * SCALE_FACTOR)
            clyde_y = int(438 * SCALE_FACTOR)
            clyde_direction = 2
            eaten_ghosts = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    # Power and collide and not dead then it will die and we can not eat them again
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghosts[0]:
        blinky_dead = True
        eaten_ghosts[0] = True
        blinky_revival_counter = 0  # Reset counter
        score += (2 ** eaten_ghosts.count(True)) * 100

    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghosts[1]:
        inky_dead = True
        eaten_ghosts[1] = True
        inky_revival_counter = 0  # Reset counter
        score += (2 ** eaten_ghosts.count(True)) * 100

    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghosts[2]:
        pinky_dead = True
        eaten_ghosts[2] = True
        pinky_revival_counter = 0  # Reset counter
        score += (2 ** eaten_ghosts.count(True)) * 100

    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghosts[3]:
        clyde_dead = True
        eaten_ghosts[3] = True
        clyde_revival_counter = 0  # Reset counter
        score += (2 ** eaten_ghosts.count(True)) * 100
    # Build in event handling for mouse keyboard etc
    for event in pygame.event.get():
        # Red close Button
        if event.type == pygame.QUIT:
            run = False
         # Check if a key was pressed
        if event.type == pygame.KEYDOWN:
            # Check if the pressed key is the Escape key  esc (pygame.K_ESCAPE)
            if event.key == pygame.K_ESCAPE:
                run = False  # Set 'run' to False to exit the game loop"
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives = 3
                startup_counter = 0
                player_x = int(450 * SCALE_FACTOR)
                player_y = int(663 * SCALE_FACTOR)
                direction = 0
                direction_command = 0
                blinky_x = int(56 * SCALE_FACTOR)
                blinky_y = int(58 * SCALE_FACTOR)
                blinky_direction = 0
                inky_x = int(440 * SCALE_FACTOR)
                inky_y = int(388 * SCALE_FACTOR)
                inky_direction = 2
                pinky_x = int(440 * SCALE_FACTOR)
                pinky_y = int(438 * SCALE_FACTOR)
                pinky_direction = 2
                clyde_x = int(440 * SCALE_FACTOR)
                clyde_y = int(438 * SCALE_FACTOR)
                clyde_direction = 2
                eaten_ghosts = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                level = copy.deepcopy(boards)
                game_won = False
                game_over = False
                score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            # Originally going this way but pressed another key by mistake
            # Pressing Two keys Current moving Right but pressed left  
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
    
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
        
    # So if reached to right max move to left
    if player_x > int(900 * SCALE_FACTOR):
        player_x = -int(47 * SCALE_FACTOR)
    elif player_x < -int(50 * SCALE_FACTOR):
        player_x = int(897 * SCALE_FACTOR)

    # If already eaten then return to normal speed only after revival
    if eaten_ghosts[0] and not blinky_dead:
        ghost_speeds[0] = 2
    if eaten_ghosts[1] and not inky_dead:
        ghost_speeds[1] = 2
    if eaten_ghosts[2] and not pinky_dead:
        ghost_speeds[2] = 2
    if eaten_ghosts[3] and not clyde_dead:
        ghost_speeds[3] = 2
        
    # If dead and in box then revived    
    # Handle ghost revival with counters
    if blinky.in_box and blinky_dead:
        blinky_revival_counter += 1
        if blinky_revival_counter > 120:  # 2 seconds at 60 fps
            blinky_dead = False
            eaten_ghosts[0] = False
            blinky_revival_counter = 0

    if inky.in_box and inky_dead:
        inky_revival_counter += 1
        if inky_revival_counter > 180:  # 3 seconds at 60 fps
            inky_dead = False
            eaten_ghosts[1] = False
            inky_revival_counter = 0

    if pinky.in_box and pinky_dead:
        pinky_revival_counter += 1
        if pinky_revival_counter > 240:  # 4 seconds at 60 fps
            pinky_dead = False
            eaten_ghosts[2] = False
            pinky_revival_counter = 0

    if clyde.in_box and clyde_dead:
        clyde_revival_counter += 1
        if clyde_revival_counter > 300:  # 5 seconds at 60 fps
            clyde_dead = False
            eaten_ghosts[3] = False
            clyde_revival_counter = 0

    pygame.display.flip() # Display 
pygame.quit()

"""
Could use jpeg but we will design a level with tiles    
0--- Blank Space
1--- Food (White Dots)
2--- Powerups (Big White Dots)
3--- Verticle (Blue Wall)
4--- Horizontal (Blue Wall)
5--- Left Down (Blue Wall)
6--- Down Right (Blue Wall)
7--- Up Right (Blue Wall)
8--- Left Up (Blue Wall)
9--- Gate Ghost (White Gate)
"""


