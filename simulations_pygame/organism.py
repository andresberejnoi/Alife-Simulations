from numpy.lib.arraysetops import isin
from numpy.lib.twodim_base import _trilu_indices_form_dispatcher
import pygame
import numpy as np

from basic_colors import *

def change_color(rgb_tup=[], change_pos=[], change_amounts=[]):
    new_color = list(rgb_tup)
    for pos_to_change, amount in zip(change_pos,change_amounts):
        new_color[pos_to_change] += amount
        if new_color[pos_to_change] > 255:
            new_color[pos_to_change] = 255
        elif new_color[pos_to_change] < 0:
            new_color[pos_to_change] = 0    

    return tuple(new_color)

class BaseOrganism(object):
    def __init__(self):
        pass 

class Organism(pygame.sprite.Sprite):
    def __init__(self, 
                 x, 
                 y, 
                 width, 
                 height, 
                 radius=5, 
                 color=BLACK, 
                 speed=[0,0], 
                 brain=None,
                 starting_genome=None):
        super().__init__()

        self.pos    = np.array([x,y], dtype=np.float64)
        self.width  = width
        self.height = height 
        self.radius = radius
        self._color  = color
        self.speed  = np.asarray(speed, dtype=np.float64)
        self.brain  = brain

        self.alive  = True
        self.energy = 100

        #instead of the above, I should be taking the genome and setting properties based on that
        #self.decode_genome()   -> something like this

        #======Graphics======#
        self.image = self.make_surface() 
        self.draw_shape()  
        self.rect  = self.image.get_rect()

    #===================================Graphical Functions=================================#
    def make_surface(self):
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(BACKGROUND)
        return self.image

    def draw_shape(self, **params):
        surface = params.get('surface', self.image)
        color   = params.get('color'  , self.color)
        radius  = params.get('radius' , self.radius)
        pygame.draw.circle(
            surface, color, (radius, radius), radius
        )
    
    def draw_text(self):
        text = f"E={self.energy:.1f}"
        self.text_surface = pygame.font.Font(None, 6)
        self.image.blit(self.text_surface.render(text, True, BLACK), self.pos)

    #=============================Evolutionary Functions====================================#
    @classmethod
    def produce_phenotype(genome):
        '''read genome and produce an Organism object 
        with the specified properties'''

        return Organism(0,0,600,400) 

    #=============================Organism Functionality====================================#
    def dies(self):
        self.alive = False
        self.color = RED
        self.draw_shape()

    def grow(self, amount=1):
        self.radius += amount
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(BACKGROUND)
        self.color = change_color(self.color, [0], [5])
        self.draw_shape()
    
    #============Getters and Setters============#
    def is_alive(self):
        return self.alive 
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, new_color):
        temp_color = []
        if isinstance(new_color, tuple):
            for channel in new_color:
                if channel > 255:
                    channel = 255
                elif channel < 0:
                    channel = 0
                temp_color.append(channel)
        self._color = tuple(temp_color)
    
    #==========================TIMESTEP FUNCTIONS============================#
    def update(self, brain_inputs=None):
        if not self.is_alive():
            return 

        self.pos += self.speed * self.speed_gaussian_noise(std=0.15)
        #self.energy -= self.moving_energy()   #this should be modified
        self.spend_energy(_type='move')
        if self.energy <= 0:
            self.kill()
            self.dies()

        x, y = self.pos 

        #Boundary conditions (org crosses to the other side)
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

    #==================================USEFUL FUNCTIONS=======================================#
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
    

