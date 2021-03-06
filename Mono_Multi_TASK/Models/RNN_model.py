import torch


class Model_RNN(nn.Module):
    
    def __init__(self,input_size,output_size,hidden_dim, n_layers):
        
        super(Model,self).__init__()
        
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        
        self.rnn = nn.RNN(input_size,hidden_dim, n_layers, batch_first = True)
        self.fc = nn.Linear(hiddem_dim, output_size)
        
        
    def forward(self,x):
        
        batch_size = x.size(0)
        hidden = self.init_hidden(batch_size)
        out,hidden = self.rnn(x,hidden)
        
        out = out.contiguous().view(-1,self.hidden_dim)
        out = self.fc(out)
        
        
        return out, hidden
   
    def init_hidden(self,batch_size):
        hidden = torch.zeros(self.n_layers,batch_size,self.hidden_dim)
        
        return hidden