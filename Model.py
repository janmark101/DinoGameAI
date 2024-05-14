import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class DQNModel(nn.Module):
    def __init__(self,n_observations,n_actions):
        super(DQNModel,self).__init__()
        self.layer_1 = nn.Linear(n_observations,128)
        self.layer_2 = nn.Linear(128,128)
        self.layer_3 = nn.Linear(128,n_actions)
        
    
    def forward(self,x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        return self.layer_3(x)
    
    def save(self,file_name='model.pth'):
        file_name = os.path.join('./', file_name)
        torch.save(self.state_dict(), file_name)