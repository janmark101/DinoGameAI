import Player
import Obstacle
import numpy as np

class Agent():
    def __init__(self):
        pass
    
    def get_state(self,game):
        
        state = [0,0,1]
        
        player_pos = game.player.player_cords.copy()
        obstacle_cords = game.obstacle.obstacle_cords.copy()
        
        point_eu = [player_pos[0] + 4*game.block_size , player_pos[1]]
        point_ed = [player_pos[0] + 4*game.block_size , player_pos[1] + game.block_size]
        point_neu = [player_pos[0] + 4*game.block_size , player_pos[1] - game.block_size]
        
        # state[0] - jump, state[1] - crouch, state[2] - nothing, state[3] - jumping, state[4] - crouching, state[5] - normal
        state = [
            # Obstacle to jump
            self.collisions(point_ed,obstacle_cords),
            
            # Obstacle to crouch
            self.collisions(point_eu,obstacle_cords),
            
            # Obstacle to do nothing
            self.collisions(point_neu,obstacle_cords),
            
            # Is jumping
            game.player.jumping,
            
            # Is crouching
            game.player.crouching,
            
            # Is doing nothing
            not (game.player.jumping or game.player.crouching)
        ]
        
        return np.array(state,dtype=int)
    
    
    def collisions(self,point,obstacle_cords):
        if  point[1] < obstacle_cords[1] < point[1] + 40 and point[0] < obstacle_cords[0] < point[0] + 40:
            return True
        return False
        