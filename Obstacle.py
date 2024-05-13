import pygame
import random

class Obstacle():
    def __init__(self,width,height,block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.obstacle_cords = [32*self.block_size,0]
        self.kind_of_obstacle = 1
        
    def create_obstacle(self,size_bool,screen):
        if self.obstacle_cords[0] < 0:
            self.kind_of_obstacle = random.randint(0,100)
            self.obstacle_cords[0] = round((self.width /self.block_size) *self.block_size,0)  
        else:
            self.obstacle_cords[0] -= self.block_size/4
            
        rect = pygame.Rect(self.obstacle_cords[0]+10,round((self.height*0.70) / self.block_size,0) * self.block_size+10 if size_bool else round((self.height*0.75) / self.block_size,0) * self.block_size+10, self.block_size/2, self.block_size/2) 
        self.obstacle_cords[1] = rect.top
        pygame.draw.rect(screen, (0,0,0), rect, 0)