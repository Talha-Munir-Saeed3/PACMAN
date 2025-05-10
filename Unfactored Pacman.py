import pygame
from board import boards
import math
import copy
pygame.init()

WIDTH=900
HEIGHT=950

PI=math.pi
#color variable for the color of walls
color='blue'
#screen display
screen=pygame.display.set_mode([WIDTH,HEIGHT])

#speed at which game runs
timer=pygame.time.Clock()

#max speed 
fps=60

#Font for score game over etc
font=pygame.font.Font('freesansbold.ttf',20)

#Later on will alter this to list and make different levels boards[activelevels]
level=copy.deepcopy(boards)
player_images=[]
#Because 4 players animation of pacman
for i in range(1,5):
    #Load and scale the image 45x45 square for pacman
    player_images.append(pygame.transform.scale(pygame.image.load(f'images/player_images/{i}.png'),(45,45)))
#Ghost images
#Red one
blinky_img=pygame.transform.scale(pygame.image.load(f'images/ghost_images/red.png'),(45,45))
#Pink one
pinky_img=pygame.transform.scale(pygame.image.load(f'images/ghost_images/pink.png'),(45,45))
#Blue one
inky_img=pygame.transform.scale(pygame.image.load(f'images/ghost_images/blue.png'),(45,45))
#Orange one
clyde_img=pygame.transform.scale(pygame.image.load(f'images/ghost_images/orange.png'),(45,45))
#Powerup Frightened to be eaten
spooked_img=pygame.transform.scale(pygame.image.load(f'images/ghost_images/powerup.png'),(45,45))
#Eaten and returning to box
dead_img=pygame.transform.scale(pygame.image.load(f'images/ghost_images/dead.png'),(45,45))
"""
Ghost Classification
Red---------->Blinky
Pink--------->Pinky
Blue--------->Inky
Orange------->Clyde
Blue Fright-->Spooked
Eyes--------->Dead
"""
#Starting postion intially for pacman
player_x=450
player_y=663
#Starting positions for ghosts
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2
#Only blinky starts outside of the box rest inside the box and move up
#Simple Directions
direction=0
#Pac-Man Animation Variable
counter=0
#Flicker For the power ups feel Lively
flicker=False
#Valid turns R L U D By Default
turns_allowed=[False,False,False,False]
#For more of classic joystick functionality
direction_command=0
#Pac Man speed 
player_speed=2
#Ofcourse Score
score=0
#Powerup , Timer, Ghosts Eaten
powerup=False
power_counter=0
eaten_ghosts=[False,False,False,False]
#Targets for the ghosts may change like to scatter ,catch etc
targets=[(player_x,player_y),(player_x,player_y),(player_x,player_y),(player_x,player_y)]
#If ghosts dead variable
blinky_dead=False
inky_dead=False
pinky_dead=False
clyde_dead=False
#Inside Box or not varaible
blinky_box=False
inky_box=False
pinky_box=False
clyde_box=False
#Speed Of the ghost
ghost_speeds=[2,2,2,2]
startup_counter=0
lives=3
game_over=False
game_won=False
#class for ghosts
class Ghost:
    def __init__(self,x_coord,y_coord,target,speed,img,direct,dead,box,id):
        #Basic Attribuites Coordinates,target,speed,image,direction,dead,box id(0-3)
        self.x_pos=x_coord
        self.y_pos=y_coord
        self.center_x=self.x_pos+22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction=direct
        self.dead=dead
        self.in_box = box
        self.id = id
        #By position on the board to see some stuff
        self.turns,self.in_box=self.check_collisions()
        #For player colliding with pacman with the circle of the pacman and rectangle of the ghost
        self.rect=self.draw()
   
    def draw(self):
        #Lots Of conditions to take into consideration
        #Drawing Normal Ghost Base Image
        """
        1----No powerup Not dead
        2----Eaten (id) powerup On Not dead
        (Means did not comeback to the box)
        """
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):
            screen.blit(self.img,(self.x_pos,self.y_pos))
        #Spooked Image
        elif (powerup and not self.dead and not eaten_ghosts[self.id]):
            screen.blit(spooked_img,(self.x_pos,self.y_pos))
        #Dead / Eaten
        else:
            screen.blit(dead_img,(self.x_pos,self.y_pos))
        #Hitbox
        ghost_rect=pygame.rect.Rect((self.center_x-18,self.center_y-18),(36,36))
        return ghost_rect

    def check_collisions(self):
        #Just like for move player 
        #To check if the ghosts can move in a certain direction
        num1=((HEIGHT-50)//32)
        num2=(WIDTH//30)
        #Fudge factor square 30x30 hence better for 15 
        num3=15
        self.turns=[False,False,False,False]
        #self.in_box=True
        #At legitimate spot
        if 0<self.center_x//30<29:
            """
            So basically
            Will move on
            0---Blank Spaces
            1---Food
            2---PowerUps
            Or
            Back inside the box if they die to revive themself
            """
            #To detect ghost door then move up when move up
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            #Moving Left
            if level[self.center_y//num1][(self.center_x-num3)//num2]<3\
            or level[self.center_y//num1][(self.center_x-num3)//num2]==9\
            and (self.in_box or self.dead):
                self.turns[1]=True
            #Moving Right
            if level[self.center_y//num1][(self.center_x+num3)//num2]<3\
            or level[self.center_y//num1][(self.center_x+num3)//num2]==9\
            and (self.in_box or self.dead):
                self.turns[0]=True
            #Moving Down
            if level[(self.center_y+num3)//num1][(self.center_x)//num2]<3\
            or level[(self.center_y+num3)//num1][(self.center_x)//num2]==9\
            and (self.in_box or self.dead):
                self.turns[3]=True
            #Moving Up
            if level[(self.center_y-num3)//num1][(self.center_x)//num2]<3\
            or level[(self.center_y-num3)//num1][(self.center_x)//num2]==9\
            and (self.in_box or self.dead):
                self.turns[2]=True
            #Orginally moving in up and down direction
            if self.direction==2 or self.direction==3:
                #Again Refactoring towards the middle of a square
                if 12<=self.center_x%num2<=18:
                    #Go Down
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 
                    and (self.in_box or self.dead)):
                        self.turns[3] = True
                    #Go Up
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 
                    and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    #Go Left
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 
                    and(self.in_box or self.dead)):
                        self.turns[1] = True
                    #Go Right
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 
                    and (self.in_box or self.dead)):
                        self.turns[0] = True
            #Orginally moving in left and right direction            
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    #Go Down
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 
                    and (self.in_box or self.dead)):
                        self.turns[3] = True
                    #Go Up
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 
                    and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    #Moving Left
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                        self.turns[1] = True
                    #Moving Right
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 
                    and (self.in_box or self.dead)):
                        self.turns[0] = True
        #Can still move left and right
        else:
            self.turns[0] = True
            self.turns[1] = True
        #If inside box
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns,self.in_box

    def move_clyde(self):
        # clyde is going to turn whenever advantageous for pursuit
        #Moving Right and target is x and y coordinate pair
        if self.direction == 0:
            #If moving right then keep going right
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            #Going right but there was a collision 
            elif not self.turns[0]:
                #Logical Turns
                #Move Down if target down
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                #Move up if target up
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                #Move left if target behind
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                #Creater Preference again prefernce D-->U-->L
                #No Logical turns
                #For example target=right or above and cant move there so we have to give it direction
                #Move Down
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                #Move Up
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                #Move Left
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            #Going right but target not there
            elif self.turns[0]:
                #Going right but target not there but constant check up and down for better position
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                #Else moving right like he did
                else:
                    self.x_pos += self.speed
        #Same thing of left direction
        elif self.direction == 1:
            #Going left move down to proceed to target
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            #Going left then go left if benefitial
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            #If going left but collision on left
            elif not self.turns[1]:
                #Target below 
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                #Then go upwards
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                #Lastly we would go left 
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                #Non logical More of priorty on user 
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
        #Going Upwards
        elif self.direction == 2:
            #Go left if going upwards
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            #Going up if target above you
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
        #Again same stuff if going x the go x/y
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
            #The prefernce thing again if going down our choice
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        #Going outside
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
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
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
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
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
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
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

#Delay At start and if moving
startup_counter=0
moving=False
#Lives
lives=3


def draw_misc():
    score_text=font.render(f'Score:{score}',True,'white')
    screen.blit(score_text,(10,920))
    if powerup:
        pygame.draw.circle(screen,'white',(140,930),15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0],(30,30)),(650+i*40,915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))

def check_collisions(s,power,power_count,eaten_ghosts):
    #Out Of Bounds
    num1=(HEIGHT-50)//32
    num2=WIDTH//30
    if player_x>0 and player_x<870:
        #Face In Eating Animation
        #Food
        if level[center_y//(num1)][center_x//num2]==1:
            level[center_y//(num1)][center_x//num2]=0
            s=s+10
        #PowerUp
        if level[center_y//(num1)][center_x//num2]==2:
            level[center_y//(num1)][center_x//num2]=0
            s=s+50
            power=True
            #Resetting the powerup counter for the new powerup timer
            power_count=0
            eaten_ghosts=[False,False,False,False]
    return s,power,power_count,eaten_ghosts

def draw_board(lvl):
    
    #50 Pixel Padding for the score etc actual board 900x900 
    #32 verical numbers (Items)
    #30 horizontal numbers (Items)

    num1=((HEIGHT-50)//32)
    num2=(WIDTH//30)
    #Using floor division so int number returned
    for i in range(len(lvl)):
        #Row Loop
        for j in range(len(lvl[i])):
            #by default 0 then black space
            if lvl[i][j]==1:
                #X Y center coordinate j*num2=x coordinate +(0.5+num2) to center it
                # Line thickness last argument  
                pygame.draw.circle(screen,'white',(j*num2+(0.5*num2),i*num1+(0.5*num1)),4)
            if lvl[i][j]==2 and not flicker:
                pygame.draw.circle(screen,'white',(j*num2+(0.5*num2),i*num1+(0.5*num1)),10)
            if lvl[i][j]==3:
                #For line we will give starting position and ending postion(via coordinates)
                pygame.draw.line(screen,color,(j*num2+(0.5*num2),i*num1),(j*num2+(0.5*num2),i*num1+num1),3)
            if lvl[i][j]==4:
                pygame.draw.line(screen,color,(j*num2,i*num1+(0.5*num1)),(j*num2+num2,i*num1+(0.5*num1)),3)                     
            if lvl[i][j]==5:
                #Why arc because they are occupying 1/4 th of a circle
                #Start and end position in terms of PI sin curve
                pygame.draw.arc(screen,color,[(j*num2-(num2*0.4))-2,(i*num1+(0.5*num1)),num2,num1],0,PI/2,3)
            if lvl[i][j]==6:  
                pygame.draw.arc(screen,color,[(j*num2+(num2*0.5)),(i*num1+(0.5*num1)),num2,num1],PI/2,PI,3)
            if lvl[i][j]==7:  
                pygame.draw.arc(screen,color,[(j*num2+(num2*0.5)),(i*num1-(0.4*num1)),num2,num1],PI,3*PI/2,3)
            if lvl[i][j]==8:  
                pygame.draw.arc(screen,color,[(j*num2-(num2*0.4))-2,(i*num1-(0.4*num1)),num2,num1],3*PI/2,2*PI,3)
            if lvl[i][j]==9:
                pygame.draw.line(screen,'white',(j*num2,i*num1+(0.5*num1)),(j*num2+num2,i*num1+(0.5*num1)),3)
            #Behaviour of 8 similar to 5
            
def draw_player():
    #4 directions
    """
    Directions For Movements
    0----RIGHT
    1----LEFT
    2----UP
    3----DOWN
    """
    #Depending on speed animation so different motions for different time frame
    #Flipping in either x direction or y direction True False right-left
    #Rotating in the basis of angles 90 or 270 up-down    
    if direction==0:     
        screen.blit(player_images[counter//5],(player_x,player_y))
    elif direction==1:
        screen.blit(pygame.transform.flip(player_images[counter//5],True,False),(player_x,player_y))
    elif direction==2:
        screen.blit(pygame.transform.rotate(player_images[counter//5],90),(player_x,player_y))
    elif direction==3:
        screen.blit(pygame.transform.rotate(player_images[counter//5],270),(player_x,player_y))
    
def check_positions(centerx,centery):
    turns=[False,False,False,False]
    #Just like we needed them in draw boards function 
    #Hence need here to see where it can go
    num1=(HEIGHT-50)//32
    num2=(WIDTH//30)
    #Fudge Factor just for refactoring pixels
    num3=15
    #Checking collisions based on center x and y +/- fudge factor 
    #Turing Backwards from where you came from
    if centerx//30<29:
        #Going Right checking back
        if direction==0:
            if level[centery//num1][(centerx-num3)//num2]<3:
                turns[1]=True
        #Going Left
        if direction==1:
            if level[centery//num1][(centerx+num3)//num2]<3:
                turns[0]=True
        if direction==2:
            if level[(centery+num3)//num1][(centerx)//num2]<3:
                turns[3]=True
        if direction==3:
            if level[(centery-num3)//num1][(centerx)//num2]<3:
                turns[2]=True
        #Turning Up and Down
        if direction==2 or direction==3:
            #At the midpoint of that tile
            if centerx%num2>=12 and centerx%num2<=18:
                #Going up and down if we are at the center of the square
                #Move Down
                if level[(centery+num3)//num1][centerx//num2]<3:
                    turns[3]=True
                #Move Up
                if level[(centery-num3)//num1][centerx//num2]<3:
                    turns[2]=True
            #At the Midpoint of the tile
            if centery%num1>=12 and centery%num1<=18:
                #Going Left and Right if we are at the center of the square
                #Move left
                if level[(centery)//num1][(centerx-num2)//num2]<3:
                    turns[1]=True
                #Move right
                if level[(centery)//num1][(centerx+num2)//num2]<3:
                    turns[0]=True
        
        #Turning Left and Right
        if direction==0 or direction==1:
            #At the midpoint of that tile
            if centerx%num2>=12 and centerx%num2<=18:
                #Going up and down if we are at the center of the square
                #Move Down
                if level[(centery+num1)//num1][centerx//num2]<3:
                    turns[3]=True
                #Move Up
                if level[(centery-num1)//num1][centerx//num2]<3:
                    turns[2]=True
            #At the Midpoint of the tile
            if centery%num1>=12 and centery%num1<=18:
                #Going Left and Right if we are at the center of the square
                #Move left
                if level[(centery)//num1][(centerx-num3)//num2]<3:
                    turns[1]=True
                #Move right
                if level[(centery)//num1][(centerx+num3)//num2]<3:
                    turns[0]=True
    else:
        turns[0]=True 
        turns[1]=True

    return turns

def move_player(play_x,play_y):
    if direction==0 and turns_allowed[0]:
        play_x=play_x+player_speed
    elif direction==1 and turns_allowed[1]:
        play_x=play_x-player_speed
    elif direction==2 and turns_allowed[2]:
        play_y=play_y-player_speed
    elif direction==3 and turns_allowed[3]:
        play_y=play_y+player_speed
    
    return play_x,play_y

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    #Check where the pac man position is if powerup is active
    #pacman=Left run to right
    if player_x < 450:
        runaway_x = 900
    #Else no issuie 
    else:
        runaway_x = 0
    #pacman=right run to left    
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    #Ghost box if eaten return to this position variable
    return_target = (380, 400)
    #Power active
    if powerup:
        #Ghosts are not dead hence they should flee in directions
        if not blinky.dead and not eaten_ghosts[0]:
            blink_target = (runaway_x, runaway_y)
        #
        elif not blinky.dead and eaten_ghosts[0]:
            
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        #If dead then goto box
        else:
            blink_target = return_target
        
        if not inky.dead and not eaten_ghosts[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghosts[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghosts[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghosts[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghosts[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    #Powerup not active
    else:
        if not blinky.dead:
            #Blinky is inside the box
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                #Go out of the box
                blink_target = (400, 100)
            #If outside target pac man
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]
#Game loop everything we want to execute when the game runs

run=True
while run: 
    timer.tick(fps) #set fps
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
    if counter<19:
        counter=counter+1
        if counter>3:
            flicker=False
    else:
        counter=0
        flicker=True
    #Powerup active and counter less than 10sec 600/60fps
    if powerup and power_counter<600:
        power_counter+=1
    elif powerup and power_counter>=600:
        power_counter=0
        powerup=False
        eaten_ghosts=[False,False,False,False]
    #3 sec delay to see the board intially
    if startup_counter<180 and not game_over and not game_won:
        moving=False
        startup_counter+=1
    else:
        moving=True
    screen.fill('black') # Solid colour black for background
    draw_board(level)
    #Just scaling midpoint 
    center_x=player_x+23
    center_y=player_y+24
    #Change speed as per powerup and death
    if powerup:
        ghost_speeds=[1,1,1,1]
    else:
        ghost_speeds=[2,2,2,2]
    if blinky_dead:
        ghost_speeds[0]=5
    if inky_dead:
        ghost_speeds[1]=5
    if pinky_dead:
        ghost_speeds[2]=5
    if clyde_dead:
        ghost_speeds[3]=5
    #For Winning
    game_won=True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won=False


    player_circle=pygame.draw.circle(screen,'black',(center_x,center_y),20,2)
    draw_player()
    blinky=Ghost(blinky_x,blinky_y,targets[0],ghost_speeds[0],blinky_img,blinky_direction,blinky_dead,blinky_box,0)
    inky=Ghost(inky_x,inky_y,targets[1],ghost_speeds[1],inky_img,inky_direction,inky_dead,inky_box,1)
    pinky=Ghost(pinky_x,pinky_y,targets[2],ghost_speeds[2],pinky_img,pinky_direction,pinky_dead,pinky_box,2)
    clyde=Ghost(clyde_x,clyde_y,targets[3],ghost_speeds[3],clyde_img,clyde_direction,clyde_dead,clyde_box,3)
    draw_misc()
    targets=get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    #Check Position on board check certain action or position is allowed
    turns_allowed=check_positions(center_x,center_y)
    
    if moving:
        #Movement Of Pac Man
        player_x,player_y=move_player(player_x,player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x,blinky_y,blinky_direction=blinky.move_blinky()
        else:    
            blinky_x,blinky_y,blinky_direction=blinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x,inky_y,inky_direction=inky.move_inky()
        else:    
            inky_x,inky_y,inky_direction=inky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x,pinky_y,pinky_direction=pinky.move_pinky()
        else:    
            pinky_x,pinky_y,pinky_direction=pinky.move_clyde()
        if not clyde_dead and not clyde.in_box:
            clyde_x,clyde_y,clyde_direction=clyde.move_clyde()
        else:    
            clyde_x,clyde_y,clyde_direction=clyde.move_clyde()
        

    #Score
    score,powerup,power_counter,eaten_ghosts=check_collisions(score,powerup,power_counter,eaten_ghosts)
    #Collision between ghost rectangle and pac man circle
    if not powerup:
        #If collide and not dead
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or\
           (player_circle.colliderect(inky.rect) and not inky.dead) or\
           (player_circle.colliderect(pinky.rect) and not pinky.dead) or\
           (player_circle.colliderect(clyde.rect) and not clyde.dead):
            #3 lives
            if lives>0:
                lives-=1
                powerup=False
                power_counter=0
                startup_counter=0
                #Positions and deaths reset
                player_x=450
                player_y=663
                direction=0
                direction_command=0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghosts=[False,False,False,False]            
                blinky_dead=False
                inky_dead=False
                pinky_dead=False
                clyde_dead=False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    #Not running into eye balls which are already dead and resetting
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghosts[0] and not blinky.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
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
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
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
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
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
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
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
    #Power and collide and not dead then it will die and we can not eat them again
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghosts[0]:
        blinky_dead = True
        eaten_ghosts[0] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    #Power and collide and not dead then it will die and we can not eat them again
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghosts[1]:
        inky_dead = True
        eaten_ghosts[1] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    #Power and collide and not dead then it will die and we can not eat them again
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghosts[2]:
        pinky_dead = True
        eaten_ghosts[2] = True
        score += (2 ** eaten_ghosts.count(True)) * 100
    #Power and collide and not dead then it will die and we can not eat them again
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghosts[3]:
        clyde_dead = True
        eaten_ghosts[3] = True
        score += (2 ** eaten_ghosts.count(True)) * 100

    
    #Build in event handling for mouse keyboard etc
    for event in pygame.event.get():
        #Red close Button
        if event.type==pygame.QUIT:
            run=False
         # Check if a key was pressed
        if event.type == pygame.KEYDOWN:
            # Check if the pressed key is the Escape key  esc (pygame.K_ESCAPE)
            if event.key == pygame.K_ESCAPE:
                run = False  # Set 'run' to False to exit the game loop"
            if event.key==pygame.K_RIGHT:
                direction_command=0
            if event.key==pygame.K_LEFT:
                direction_command=1
            if event.key==pygame.K_UP:
                direction_command=2
            if event.key==pygame.K_DOWN:
                direction_command=3
            if event.key==pygame.K_SPACE and(game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghosts = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                level=copy.deepcopy(boards)
                game_won=False
                game_over=False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            #Orginally going this way but pressed another key by mistake
            #Pressing Two keys Current moving Right but pressed left  
            if event.key==pygame.K_RIGHT and direction_command==0:
                direction_command=direction
            if event.key==pygame.K_LEFT and direction_command==1:
                direction_command=direction
            if event.key==pygame.K_UP and direction_command==2:
                direction_command=direction
            if event.key==pygame.K_DOWN and direction_command==3:
                direction_command=direction

    
    if direction_command==0 and turns_allowed[0]:
        direction=0
    if direction_command==1 and turns_allowed[1]:
        direction=1
    if direction_command==2 and turns_allowed[2]:
        direction=2
    if direction_command==3 and turns_allowed[3]:
        direction=3
    #So if reaached to right max move to left
    if player_x>900:
        player_x=-47
    #If reached left max move to right
    elif player_x<-50:
        player_x=897
    #If already eaten then return to normal speed
    if eaten_ghosts[0]:
        ghost_speeds[0]=2
    if eaten_ghosts[1]:
        ghost_speeds[1]=2
    if eaten_ghosts[2]:
        ghost_speeds[2]=2
    if eaten_ghosts[3]:
        ghost_speeds[3]=2
    #If dead and in box then revived    
    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False 




    #timer.tick(fps) #set fps
    #screen.fill('black') # Solid colour black for background
    pygame.display.flip() #Display 
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




