import pygame
import Player
import Obstacle

class GameEnv():
    def __init__(self,width,height):
        self.width = int(width *0.5)
        self.height = int(height *0.375)
        self.block_size = 40
        self.screen = pygame.display.set_mode((self.width , self.height))
        self.player = Player.Player(self.width,self.height,self.block_size)
        self.obstacle = Obstacle.Obstacle(self.width,self.height,self.block_size)
        self.font = pygame.font.SysFont("monospace", 25)
        self.ground_cords = self.player.player_cords.copy()
        #self.run_game()
        self.clock = pygame.time.Clock()
        
    def run_game(self):
        clock = pygame.time.Clock()
        running = True
        is_playing = True

        

        while running:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and not is_playing:
                            self.restart()
                            is_playing = True
                              
            while is_playing:
                self.screen.fill('grey')
                self.create_grid()
                pygame.draw.line(self.screen,(0,0,0), (0, self.ground_cords[1] + 2*self.block_size), (self.width, self.ground_cords[1] + 2*self.block_size),2)
                label = self.font.render(f"{self.player.score}", 5, (0,0,0))
                self.screen.blit(label, (round((self.width*0.50) / self.block_size,0) * self.block_size, round((self.height*0.10) / self.block_size,0) * self.block_size))
                
                self.player.show_player(self.screen)
                self.obstacle.create_obstacle(self.screen)
                # if self.player.check_reward(self.obstacle.obstacle_cords[0]):
                #     self.player.reward 

                # pygame.draw.line(self.screen,(0,0,0), (self.player.player_cords[0] + 4*self.block_size, self.player.player_cords[1]-self.block_size), (self.player.player_cords[0] + 4*self.block_size, self.player.player_cords[1]),2)
                
            
                # if self.player.check_collisions(self.player.player_cords,self.obstacle.obstacle_cords):
                #     is_playing = False
                    
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_playing= False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w and not self.player.jumping and not self.player.crouching:
                            self.player.jumping = True
                            self.player.jump_count = self.player.jump_value
                        if event.key == pygame.K_s and not self.player.jumping and not self.player.crouching:
                            self.player.state = 'Crouch'
                            self.player.crouching = True
                        

                if self.player.jumping:
                    self.player.jump()

                    
                if self.player.crouching:
                    self.player.crouch()
                    
                    
                self.player.score += 1
                
                
                
 
                
                    
                pygame.display.flip()

                clock.tick(60)  

        pygame.quit()

    

    def create_grid(self):
        for x in range(0,self.width,self.block_size):
            for y in range(0,self.height,self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, (250,250,250), rect, 1)
        
    def restart(self):
        self.obstacle = Obstacle.Obstacle(self.width,self.height,self.block_size)
        self.player = Player.Player(self.width,self.height,self.block_size)
        
    def update_game(self):
        self.screen.fill('grey')
        self.create_grid()
        pygame.draw.line(self.screen,(0,0,0), (0, self.ground_cords[1] + 2*self.block_size), (self.width, self.ground_cords[1] + 2*self.block_size),2)
        label = self.font.render(f"{self.player.score}", 5, (0,0,0))
        self.screen.blit(label, (round((self.width*0.50) / self.block_size,0) * self.block_size, round((self.height*0.10) / self.block_size,0) * self.block_size))
        
        self.player.show_player(self.screen)
        self.obstacle.create_obstacle(self.screen)
        
        pygame.display.flip()
        
    def step(self,action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self.move(action)
        reward = 0
        game_over = False
        if self.player.check_collisions(self.player.player_cords,self.obstacle.obstacle_cords):
            reward = -10
            game_over = True
            return reward,game_over,self.player.score
        
        if self.player.check_reward(self.obstacle.obstacle_cords[0]):
            reward = 1
            
        self.player.score += 1
        self.update_game()
        self.clock.tick(60)
            
        return reward,game_over,self.player.score


    def move(self,action):
        if action == [0,0,1]:
            pass
        if action == [0,1,0]:
            if not self.player.jumping and not self.player.crouching:
                self.player.jumping = True
                self.player.jump_count = self.player.jump_value
        elif action == [1,0,0]:
            if not self.player.jumping and not self.player.crouching:
                self.player.state = 'Crouch'
                self.player.crouching = True
                
        if self.player.jumping:
            self.player.jump()

            
        if self.player.crouching:
            self.player.crouch()
            

pygame.init()
screen_info = pygame.display.Info()

game = GameEnv(screen_info.current_w,screen_info.current_h)

#game = GameEnv(1920,1080)

