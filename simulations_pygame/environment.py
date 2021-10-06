import pygame
import numpy as np

from organism import Organism
from basic_colors import *

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