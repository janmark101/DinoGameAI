import itertools
import numpy as np
from collections import deque
import random
import torch as tt
from DinoGame import GameEnv
from DQNModel import Network,ReplayMemory
import pygame
import matplotlib.pyplot as plt

EPSILON_DECAY = 10000
EPSILON_END = 0.02
EPSILON_START = 1.0
UPDATE_FREQ = 100

class Agent():
    def __init__(self):
        self.model = Network(6,3)
        self.target_model = Network(6,3)
        self.epsilon = 1.0
        self.gamma = 0.95 
        self.memory = ReplayMemory(self.model,self.target_model,self.gamma,0.001)
            
    def get_state(self,game):        
        player_pos = game.player.player_cords.copy()
        obstacle_cords = game.obstacle.obstacle_cords.copy()
        
        point_eu = [player_pos[0] + 4*game.block_size , player_pos[1]]
        point_ed = [player_pos[0] + 4*game.block_size , player_pos[1] + game.block_size]
        point_neu = [player_pos[0] + 4*game.block_size , player_pos[1] - game.block_size]
        
        # state[0] - jump, state[1] - crouch, state[2] - nothing, state[3] - jumping, state[4] - crouching, state[5] - normal
        state = [
            
            # Distance to obstacle
            obstacle_cords[0] - player_pos[0],
            
            # Height of obstacle
            obstacle_cords[1],
            
            # Obstacle speed
            20,
            
            # # Obstacle to jump
            # self.collisions(point_ed,obstacle_cords),
            
            # # Obstacle to crouch
            # self.collisions(point_eu,obstacle_cords),
            
            # # Obstacle to do nothing
            # self.collisions(point_neu,obstacle_cords),
            
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
    
        
    def get_action(self,state):
        action = [0,0,0]
        if random.random() <= self.epsilon:
            rand_action = random.randint(0,2)
            action[rand_action] = 1
        else:
            state = tt.tensor(state,dtype=tt.float)
            nn_action = self.model(state)
            action[tt.argmax(nn_action).item()] = 1

        return action   
    

def train():
    agent = Agent()
    game = GameEnv(2560,1440)
    record = 0
    games = 0
    total_score = 0
    plt_scores = []
    plt_loss = []
    plt_average_score = []
    
    
    for _ in range(500):
        state = agent.get_state(game)
        action = agent.get_action(state)
        
        reward,done,score = game.step(action)
        new_state = agent.get_state(game)
        
        agent.memory.update_memory(state,action,reward,new_state,done)

        if done:
            game.restart()
            
    
    game.restart()
    print('Memory initializing done !')

    for step in itertools.count():

        epsilon = np.interp(step,[0,EPSILON_DECAY],[EPSILON_START,EPSILON_END])
        agent.epsilon = epsilon
        
        state = agent.get_state(game)
        action = agent.get_action(state)

        reward,done,score = game.step(action)
        
        if score > record :
            reward = 10

        new_state = agent.get_state(game)
        
        agent.memory.update_memory(state,action,reward,new_state,done)
        sample = agent.memory.sample()

        agent.memory.train_from_memory(sample)

        
        if step % UPDATE_FREQ == 0 :
            agent.target_model.load_state_dict(agent.model.state_dict())
            
        if done:
            game.restart()
            games += 1

            if score > record:
                record = score
            
            print('Game', games, 'Score', score, 'Record:', record,'loss',agent.memory.loss)
            total_score += score
            plt_scores.append(score)
            plt_average_score.append(total_score/games)
            plt_loss.append(agent.memory.loss)
            
        if games >= 500:
            make_plot(plt_scores,games,'Score')
            make_plot(plt_average_score,games,'Average Score')
            make_plot(plt_loss,games,'Loss')
            break
            


def make_plot(array,games,x,y='Games'):
    plt.figure(figsize=(10, 8))  # Ustawienie większego rozmiaru wykresu
    plt.plot([i for i in range(games)], array)  # Dodanie punktów i wykresu liniowego
    plt.title(f'{x} plot')  # Tytuł wykresu
    plt.xlabel(y)  # Etykieta osi X
    plt.ylabel(x)  # Etykieta osi Y
    plt.grid(True)  # Dodanie siatki
    plt.show()  # Wyświetlenie wykresu

train()