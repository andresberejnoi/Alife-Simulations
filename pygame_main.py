'''
This script has been writen following the tutorial from:
https://www.youtube.com/watch?v=84njPYepKIU

on how to create a disease simulation using PyGame. 
I'm adapting it to my own artificial life simulations.
'''

import pygame
import numpy as np
import sys

BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE  = (0, 100, 255)

BACKGROUND = WHITE

class Organism(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, radius=5, color=BLACK, speed=[0,0], starting_genome=None):
        super().__init__()

        self.image = pygame.Surface([radius * 2, radius * 2])   #creates the surface where to draw the sprite
        self.image.fill(BACKGROUND)         #fills a square with the background color
        pygame.draw.circle(
            self.image, color, (radius, radius), radius   #draw a circle (so our organism is a circle for now)
        )

        self.rect   = self.image.get_rect()     #get the bounding boxes for the sprite (used for collisions and other stuff)
        self.pos    = np.array([x,y], dtype=np.float64)   #current position of the sprite
        self.speed  = np.asarray(speed, dtype=np.float64)   #speed as a vector (the speed in the x and y directions independently). This will be the distance or change in self.pos per frame update

        self.width  = width    #world boundary
        self.height = height   #world boundary
        # self.x      = x
        # self.y      = y
        # self.color  = BLACK
        # self.speed  = [0,0]   #x and y values
        # self.radius = 5

    def update(self):
        self.pos += self.speed

        x, y = self.pos 

        #Boundary conditions (currently, organism will appear on the other side of the screen
        # when crossing the edge)
        if x < 0:
            self.pos[0] = self.width
            x = self.width
        elif x > self.width:
            self.pos[0] = 0
            x = 0

        if y < 0:
            self.pos[1] = self.height
            y = self.height
        elif y > self.height:
            self.pos[1] = 0
            y = 0

        self.rect.y = y
        self.rect.x = x

class Simulation(object):
    def __init__(self,width=600, height=400, total_creatures=100):
        self.WIDTH           = width 
        self.HEIGHT          = height
        self.TOTAL_CREATURES = total_creatures
        
        self.alive_container = pygame.sprite.Group()
        self.dead_container  = pygame.sprite.Group()

        self.population_container = pygame.sprite.Group()

    def start(self, t_steps=1000):
        pygame.init()
        screen = pygame.display.set_mode(
            [self.WIDTH, self.HEIGHT]
        )

        for i in range(self.TOTAL_CREATURES):
            x = np.random.randint(0, self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)

            speed = np.random.rand(2) * 2 - 1
            org   = Organism(x, y, self.WIDTH, self.HEIGHT, color=BLUE, speed=speed)
            self.alive_container.add(org)
            self.population_container.add(org)
        
        timesteps = t_steps
        clock     = pygame.time.Clock()

        for i in range(timesteps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            self.population_container.update()    #calls the update method on each organism in the container
            screen.fill(BACKGROUND)
            self.population_container.draw(screen)
            pygame.display.flip()
            clock.tick(15)

        pygame.quit()

        
def main_old():
    WIDTH           = 600
    HEIGHT          = 400
    TOTAL_CREATURES = 100
    
    pygame.init()
    screen = pygame.display.set_mode(
        [WIDTH, HEIGHT]
    )

    container = pygame.sprite.Group()

    
    for i in range(TOTAL_CREATURES):
        x = np.random.randint(0, WIDTH + 1)
        y = np.random.randint(0, HEIGHT + 1)

        speed = np.random.rand(2) * 2 - 1
        org   = Organism(x, y, WIDTH, HEIGHT, color=BLUE, speed=speed)
        container.add(org)

    timesteps = 2000
    clock     = pygame.time.Clock()

    for i in range(timesteps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        container.update()    #calls the update method on each organism in the container
        screen.fill(BACKGROUND)
        container.draw(screen)
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()

if __name__ == '__main__':
    sim = Simulation()
    sim.start(700)


