import pygame
import random

class Obstacle():
    def __init__(self,width,height,block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.obstacle_cords = [self.width+10,round((self.height*0.70) / self.block_size,0) * self.block_size+10]

        
        
    def random_obstacle_choose(self):
        temp = random.randint(0,100)
        if  0<=temp<20 : 
            self.obstacle_cords[1] = round((self.height*0.70) / self.block_size,0) * self.block_size+10
        elif 20<=temp<85:
            self.obstacle_cords[1] = round((self.height*0.75) / self.block_size,0) * self.block_size+10
        elif 85<=temp<=100:
            self.obstacle_cords[1] = round((self.height*0.60) / self.block_size,0) * self.block_size+10
        
    def create_obstacle(self,screen):
        if self.obstacle_cords[0] < 0:
            self.random_obstacle_choose()
            self.obstacle_cords[0] = round((self.width /self.block_size) *self.block_size,0)  
        else:
            self.obstacle_cords[0] -= self.block_size/2
            
        rect = pygame.Rect(self.obstacle_cords[0],self.obstacle_cords[1], self.block_size/2, self.block_size/2) 
        self.obstacle_cords[1] = rect.top
        pygame.draw.rect(screen, (0,0,0), rect, 0)