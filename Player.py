import pygame

class Player():
    def __init__(self,width,height,block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.gravity = 0.5
        self.player_cords = [round((self.width*0.10) / self.block_size,0) * self.block_size, round((self.height*0.70) / self.block_size,0) * self.block_size]  
        self.state = 'Normal'
        self.jump_count = 0
        self.jump_value = 15
        self.jumping = False
        self.crouching = False
        self.crouch_time = 15
        self.score = 0
        self.reward = 0
        
    def show_player(self,screen):
        if self.state =='Normal':
            self.player = pygame.Rect(self.player_cords[0],self.player_cords[1], self.block_size, 2*self.block_size)
        elif self.state == 'Crouch':
            self.player = pygame.Rect(self.player_cords[0],self.player_cords[1] + self.block_size, self.block_size, 1*self.block_size)
        pygame.draw.rect(screen, (0,0,0), self.player, 0)
        
    def jump(self):
        self.player_cords[1] -= self.jump_count
        if self.jump_count > -self.jump_value:
            self.jump_count -= 1
        else:
            self.jumping = False
    
    def crouch(self):
        self.crouch_time -=0.5
        if self.crouch_time <= 0:
            self.state = 'Normal'
            self.crouching = False
            self.crouch_time = 15   
            
    def check_collisions(self,player_cords,obstacle_cords):
        if self.state == 'Normal':
            if  player_cords[1] < obstacle_cords[1] < player_cords[1] + 80 and player_cords[0] < obstacle_cords[0] < player_cords[0] + 40:
                self.reward -=10
                return True
        elif self.state == 'Crouch':
            if  player_cords[1] + 40 < obstacle_cords[1] < player_cords[1] + 80 and player_cords[0] < obstacle_cords[0] < player_cords[0] + 40:
                self.reward -= 10
                return True
            
    def check_reward(self,obstacle_cords):
        if obstacle_cords == self.player_cords[0] - 10 :
            return True
        return False