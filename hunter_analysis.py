import pandas as pd
import corner
from sys import exit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

num_pars=5
norm=False # normalize values to have a maximum of 1

# read in csv file
data_pd = pd.read_csv("Edi_Uni_Moodys_MonteCarlo.csv", index_col=False)

#label_idx = [0,1,2]

# make a corner plot
data_np = data_pd.values
labels = data_np[:num_pars,1]
data_np_new = []
for i in range(len(data_np)):
    data_np_new.append(pd.to_numeric(data_np[i,2:]))

data_np = np.array(data_np_new)

# normalize values to be between 0 and 1
if norm == True:
    for i in range(data_np.shape[1]):
        data_np[:,i] /= np.max(data_np[:,i])
        #data_np[:,i] = -1 + 2.*(data_np[:,i] - min(data_np[:,i])) / (max(data_np[:,i]) - min(data_np[:,i]))
        #data_np[:,i] = 2*( (data_np[:,i]- np.min(data_np[:,i])) / (np.max(data_np[:,i]) - np.min(data_np[:,i])) ) - 1

# get trails data
num_trials=5000
cnt=0
for i in range(num_trials):
    if i == 0:
        corner_data = data_np[cnt:num_pars,:].T
        cnt+=59*2
        continue
    corner_data = np.vstack([corner_data,data_np[59*i:cnt-(59-num_pars),:].T])
    cnt+=59

#from pandas.plotting import scatter_matrix
#scatter_matrix(pd.DataFrame(corner_data), alpha = 0.2, figsize = (6, 6), diagonal = 'kde')

figure = corner.corner(corner_data, quantiles=(0.16,0.84), labels=labels,label_kwargs=dict(fontsize='9'))
plt.savefig('corner_result.pdf')
plt.close()
