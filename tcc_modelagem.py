# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 22:06:28 2021

@author: rodrigo.gosmann
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import torch #pytorch
import torch.nn as nn
from torch.autograd import Variable 

class LSTM1(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
        super(LSTM1, self).__init__()
        self.num_classes = num_classes #number of classes
        self.num_layers = num_layers #number of layers
        self.input_size = input_size #input size
        self.hidden_size = hidden_size #hidden state
        self.seq_length = seq_length #sequence length
 
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                      num_layers=num_layers, batch_first=True) #lstm
        self.fc_1 =  nn.Linear(hidden_size, 128) #fully connected 1
        self.fc = nn.Linear(128, num_classes) #fully connected last layer

        self.relu = nn.ReLU()

    def forward(self,x):
        h_0 = Variable(torch.zeros(
              self.num_layers, x.size(0), self.hidden_size)) #hidden state
         
        c_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size)) #internal state
       
        # Propagate input through LSTM
    
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
       
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
    
        out = self.relu(hn)
    
        out = self.fc_1(out) #first Dense
    
        out = self.relu(out) #relu
    
        out = self.fc(out) #Final Output
   
        return out 





col_modelagem = list(['K_GR2','HGROSS_1H','PHG2','GE_02','NJ_1H','mes','VT_02'])
X = dados[col_modelagem[0:-1]]
y = dados[[col_modelagem[-1]]]

mm = MinMaxScaler()
ss = StandardScaler()


X_ss = ss.fit_transform(X)
y_mm = mm.fit_transform(y) 

qtd_amo_treino = 20000
X_train = X_ss[:qtd_amo_treino, :]
X_test = X_ss[qtd_amo_treino:, :]

y_train = y_mm[:qtd_amo_treino, :]
y_test = y_mm[qtd_amo_treino:, :] 

print("Training Shape", X_train.shape, y_train.shape)
print("Testing Shape", X_test.shape, y_test.shape) 

X_train_tensors = Variable(torch.Tensor(X_train))
X_test_tensors = Variable(torch.Tensor(X_test))

y_train_tensors = Variable(torch.Tensor(y_train))
y_test_tensors = Variable(torch.Tensor(y_test)) 

#reshaping to rows, timestamps, features

X_train_tensors_final = torch.reshape(X_train_tensors,   (X_train_tensors.shape[0], 1, X_train_tensors.shape[1]))


X_test_tensors_final = torch.reshape(X_test_tensors,  (X_test_tensors.shape[0], 1, X_test_tensors.shape[1])) 

print("Training Shape", X_train_tensors_final.shape, y_train_tensors.shape)
print("Testing Shape", X_test_tensors_final.shape, y_test_tensors.shape) 

num_epochs = 1000 #1000 epochs
learning_rate = 0.001 #0.001 lr

input_size = X.shape[1] #number of features
hidden_size = 40 #number of features in hidden state
num_layers = 1 #number of stacked lstm layers

num_classes = 1 #number of output classes 

##############################
##### treino pytorch
lstm1 = LSTM1(num_classes, input_size, hidden_size, num_layers, X_train_tensors_final.shape[1]) #our lstm class 

criterion = torch.nn.MSELoss()    # mean-squared error for regression
optimizer = torch.optim.Adam(lstm1.parameters(), lr=learning_rate) 

for epoch in range(num_epochs):
    outputs = lstm1.forward(X_train_tensors_final) #forward pass
    optimizer.zero_grad() #caluclate the gradient, manually setting to 0
 
    # obtain the loss function
    loss = criterion(outputs, y_train_tensors)
 
    loss.backward() #calculates the loss of the loss function
 
    optimizer.step() #improve from loss, i.e backprop
    if epoch % 100 == 0:
        print("Epoch: %d, loss: %1.5f" % (epoch, loss.item())) 

##############################
##### treino floresta

regressor = RandomForestRegressor(n_estimators = 100, random_state = 0)
# regressor = RandomForestRegressor(n_estimators = 100, random_state = 0,max_depth=6)
regressor.fit(X_train, np.ravel(y_train))

# prediz com toda a base de dados
y_pred_forest_norm = regressor.predict(ss.transform(X))

y_pred_forest =  mm.inverse_transform(y_pred_forest_norm.reshape(-1,1))


##############################
##### predicao, usando todo o dataset

df_X_ss = ss.transform(X) #old transformers
df_y_mm = mm.transform(y) #old transformers

df_X_ss = Variable(torch.Tensor(df_X_ss)) #converting to Tensors
df_y_mm = Variable(torch.Tensor(df_y_mm))
#reshaping the dataset
df_X_ss = torch.reshape(df_X_ss, (df_X_ss.shape[0], 1, df_X_ss.shape[1]))

train_predict = lstm1(df_X_ss)#forward pass
data_predict = train_predict.data.numpy() #numpy conversion
dataY_plot = df_y_mm.data.numpy()

data_predict = mm.inverse_transform(data_predict) #reverse transformation
dataY_plot = mm.inverse_transform(dataY_plot)

# Calculo dos residuos

residuo_nn=dataY_plot-data_predict
residuo_ft=dataY_plot-y_pred_forest

residuos=pd.DataFrame(np.concatenate([residuo_nn,residuo_ft],axis=1),columns=['neural_net','forest'])



