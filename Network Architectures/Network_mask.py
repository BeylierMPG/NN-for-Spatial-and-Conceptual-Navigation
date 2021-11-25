import torch
import torch.nn as nn
import torch.nn.functional as F



class Net_1(torch.nn.Module):
    def __init__(self,input_dimension, output_dimension):
        super(Net_1, self).__init__()
        self.fc1 = nn.Linear(in_features = input_dimension, out_features = 2)
        self.fc2 = nn.Linear(in_features = 2, out_features = 2)
        self.fc3 = nn.Linear(in_features = 2, out_features = output_dimension)


    def forward(self, x):

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return torch.sigmoid(x)

class Net_1_bis(torch.nn.Module):
    def __init__(self,input_dimension, output_dimension):
        super(Net_1_bis, self).__init__()
        self.fc1 = nn.Linear(in_features = input_dimension, out_features = 1)
        self.fc2 = nn.Linear(in_features = 1, out_features = 2)
        self.fc3 = nn.Linear(in_features = 2, out_features = output_dimension)


    def forward(self, x):

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return torch.sigmoid(x)
    
    
    
class Net_2(torch.nn.Module):
    def __init__(self,input_dimension, output_dimension):
        super(Net_2, self).__init__()
        self.fc1 = nn.Linear(in_features = input_dimension, out_features = 2)
        self.fc2 = nn.Linear(in_features = 2, out_features = 4)
        self.fc3 = nn.Linear(in_features = 4, out_features = output_dimension)


    def forward(self, x):

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return torch.sigmoid(x)
    
    

    
    


class Training_fusion():

  # The class initialisation function.
    def __init__(self,model,opti,loss):
        self.model = model
        self.optimizer = opti
        self.criterion = loss
    
    def train_network(self,data,target,pumpkin_seed):
        
        if pumpkin_seed == 1:
            self.mask2 = torch.tensor([[0,0],[0,0],[1,1],[1,1]])
            self.mask3 = torch.tensor([[0,0,0,0],[0,0,1,1]])  

        if pumpkin_seed == 0:
            self.mask2 = torch.tensor([[1,1],[1,1],[0,0],[0,0]])
            self.mask3 = torch.tensor([[1,1,0,0],[0,0,0,0]])
        
        with torch.no_grad():
            self.model.fc2.weight.mul_(self.mask2)
            self.model.fc3.weight.mul_(self.mask3)
            
        #Compute the prediction
        output = self.model.forward(data)
        # Calculate the loss for this transition.
        loss =  self.criterion(output,target)
        # Set all the gradients stored in the optimiser to zero.
        self.optimizer.zero_grad()
        # Compute the gradients based on this loss, i.e. the gradients of the loss with respect to the Q-network parameters.
        loss.backward()    
        
        with torch.no_grad():
            self.model.fc3.weight.grad.mul_(self.mask3)
           # print('Step {}, weight {}, weight.grad {}'.format(pumpkin_seed, self.model.fc3.weight, self.model.fc3.weight.grad))
            self.model.fc2.weight.grad.mul_(self.mask2)
            #print('Step {}, weight {}, weight.grad {}'.format(pumpkin_seed, self.model.fc2.weight, self.model.fc2.weight.grad))
        # Take one gradient step to update the Q-network. 
        self.optimizer.step()
        # Return the loss as a scalar
        return loss

    
    
class Training_dissociated():

  # The class initialisation function.
    def __init__(self,model,opti,loss):
        self.model = model
        self.optimizer = opti
        self.criterion = loss
    
    def train_network(self,data,target):
            
        #Compute the prediction
        output = self.model.forward(data)
        # Calculate the loss for this transition.
        loss =  self.criterion(output,target.unsqueeze(1))
        # Set all the gradients stored in the optimiser to zero.
        self.optimizer.zero_grad()
        # Compute the gradients based on this loss, i.e. the gradients of the loss with respect to the Q-network parameters.
        loss.backward()    
         # Take one gradient step to update the Q-network. 
        self.optimizer.step()
        # Return the loss as a scalar
        return loss




 #print('Step {}, weight {}, weight.grad {}'.format(1, self.model.fc1.weight, self.model.fc1.weight.grad))
        #print(self.model.fc2.weight)