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
RED   = (255, 0, 0)

BACKGROUND = WHITE

def change_color(rgb_tup=[], change_pos=[], change_amounts=[]):
    new_color = list(rgb_tup)
    for pos_to_change, amount in zip(change_pos,change_amounts):
        new_color[pos_to_change] += amount
        if new_color[pos_to_change] > 255:
            new_color[pos_to_change] = 255
        elif new_color[pos_to_change] < 0:
            new_color[pos_to_change] = 0    

    return tuple(new_color)


class Organism(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, radius=5, color=BLACK, speed=[0,0], starting_genome=None):
        super().__init__()


        self.radius = radius

        self.image = pygame.Surface([self.radius * 2, self.radius * 2])   #creates the surface where to draw the sprite
        self.image.fill(BACKGROUND)         #fills a square with the background color
        self.color = color

        self.pos    = np.array([x,y], dtype=np.float64)   #current position of the sprite
        self.speed  = np.asarray(speed, dtype=np.float64)   #speed as a vector (the speed in the x and y directions independently). This will be the distance or change in self.pos per frame update

        self.width  = width    #world boundary
        self.height = height   #world boundary

        self.alive  = True
        self.energy = 100

        # pygame.draw.circle(
        #     self.image, self.color, (self.radius, self.radius), self.radius   #draw a circle (so our organism is a circle for now)
        # )
        self.draw_shape()

        self.rect   = self.image.get_rect()     #get the bounding boxes for the sprite (used for collisions and other stuff)
        
        # self.x      = x
        # self.y      = y
        # self.color  = BLACK
        # self.speed  = [0,0]   #x and y values
        # self.radius = 5

    def draw_shape(self, **params):
        surface = params.get('surface', self.image)
        color   = params.get('color'  , self.color)
        radius  = params.get('radius' , self.radius)
        pygame.draw.circle(
            #self.image, self.color, (self.radius, self.radius), self.radius
            surface, color, (radius, radius), radius
        )
        #self.draw_text()

    def draw_text(self):
        text = f"E={self.energy:.1f}"
        self.text_surface = pygame.font.Font(None, 6)
        self.image.blit(self.text_surface.render(text, True, BLACK), self.pos)

    def is_alive(self):
        return self.alive 

    def dies(self):
        self.alive = False
        self.color = RED
        self.draw_shape()

    def grow(self, amount=1):
        self.radius += amount
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(BACKGROUND)
        self.color = change_color(self.color, [0], [5])
        #print(self.color)
        self.draw_shape()

    def speed_gaussian_noise(self, std=1.0):
        x_center = self.speed[0]
        y_center = self.speed[1]
        noise = [np.random.normal(loc=x_center, scale=std), 
                 np.random.normal(loc=y_center, scale=std)]
        
        return np.array(noise)

    def spend_energy(self, amount=1, _type='move'):
        if _type.lower() == 'move':
            #self.energy -= self.moving_energy()
            self.energy -= np.sum(self.speed) * 0.5
        elif _type == 'idle':
            self.energy -= 1
        elif _type == 'misc':
            self.energy -= amount

    def moving_energy(self):
        return np.sum(self.speed) * 0.5

    def update(self):
        if not self.is_alive():
            return 

        self.pos += self.speed * self.speed_gaussian_noise(std=0.15)
        #self.energy -= self.moving_energy()   #this should be modified
        self.spend_energy(_type='move')
        if self.energy <= 0:
            self.kill()
            self.dies()
            #self.alive = False

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

    def collide(self, other_group):
        collisions = pygame.sprite.spritecollide(self, other_group, False)  #list of sprites that collided with self
        for org in collisions:
            if self.energy > org.energy:
                org.kill()
                org.dies()
                self.energy += 2.5
                self.grow()
            elif self.energy < org.energy:
                org.energy += 2.5
                org.grow()
                self.dies()
                self.kill()
                break            
            elif self.energy == org.energy:
                org.speed *= -1
                self.speed *= -1
                

class Simulation(object):
    def __init__(self,width=600, height=400, total_creatures=500):
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

            #================Collision handling here================#
            # collision_group = pygame.sprite.groupcollide(
            #     self.population_container,
            #     self.population_container,
            #     True, 
            #     True
            # )

            # for org in collision_group:
            #     org.speed *= -1
            #     org.energy += 1

            for org in self.population_container:
                self.population_container.remove(org)
                org.collide(self.population_container)
                if org.is_alive():
                    self.population_container.add(org)
                else:
                    self.dead_container.add(org)


            #=======================================================#
            self.population_container.draw(screen)
            pygame.display.flip()     #not sure what this is for, yet.
            clock.tick(15)          #delay between clock ticks, probably in milliseconds

        pygame.quit()

if __name__ == '__main__':
    sim = Simulation()
    sim.start(20000)


