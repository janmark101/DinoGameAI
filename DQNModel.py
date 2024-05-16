import random
from collections import deque
import torch as tt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


MAX_MEMORY_SIZE = 100_000
BATCH_SIZE = 32


class Network(nn.Module):
    def __init__(self,state_n,action_n):
        super().__init__()
        self.l_1 = nn.Linear(state_n,256)
        self.l_2 = nn.Linear(256,action_n)
        
    def forward(self,x):
        x = F.relu(self.l_1(x))
        x = self.l_2(x)
        return x

class ReplayMemory():
    def __init__(self,model,target_model,gamma,lr):
        self.memory = deque(maxlen=MAX_MEMORY_SIZE)
        self.batch_size = 32
        self.model = model
        self.target_model = target_model
        self.gamma = gamma
        self.lr = lr
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.loss = 0
        
    def update_memory(self,state,action,reward,new_state,done):
        self.memory.append((state,action,reward,new_state,done))
    
    def sample(self):
        return random.sample(self.memory,self.batch_size)
    
    def train_from_memory(self,sample):
        states,actions,rewards,new_states,dones = zip(*sample)
        
        states = np.asarray(states)
        actions = np.asarray(actions)
        rewards = np.asarray(rewards)
        new_states = np.asarray(new_states)
        dones = np.asarray(dones)
        
        states_t = tt.tensor(states,dtype=tt.float32)
        actions_t = tt.tensor(actions,dtype=tt.int64)
        rewards_t = tt.tensor(rewards,dtype=tt.float32)
        new_states_t = tt.tensor(new_states,dtype=tt.float32)
        dones_t = tt.tensor(dones,dtype=tt.float32)
        
        if len(states.shape) == 1:
            # (1, x)
            states_t = tt.unsqueeze(states, 0)
            new_states_t = tt.unsqueeze(new_states, 0)
            actions_t = tt.unsqueeze(actions, 0)
            rewards_t = tt.unsqueeze(rewards, 0)
            dones_t = (dones, )

        
        
        target_q_values = self.target_model(new_states_t)
        q_values = self.model(states_t)
        
        targets = q_values.clone().detach()
        for i in range(len(sample)):
            targets[i, tt.argmax(actions_t[i]).item()] = rewards_t[i] + self.gamma * (1 - dones_t[i]) * tt.max(target_q_values[i])
        
        # max_target_q_values = target_q_values.max(dim=1,keepdim=True)[0]
        # targets = rewards + self.gamma * (1-dones) * max_target_q_values
        # action_q_values = tt.gather(input=q_values,dim=1,index=actions)
        # loss = F.smooth_l1_loss(action_q_values,targets)
        
        loss = F.smooth_l1_loss(q_values,targets)
        self.loss = loss.item()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
         