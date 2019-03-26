import pandas as pd
import corner
from sys import exit
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

norm=False # normalize values to have a maximum of 1 if True
num_trials=5000 # number of trials to use

# read in csv file
data_pd = pd.read_csv("Edi_Uni_Moodys_MonteCarlo.csv", index_col=False)

# choose your time and parameters here
# label is parameter and time is time
label_idx = list(np.arange(start=25,stop=51,step=1))
# label_idx = [42,46]
time_idx = list(np.arange(start=0,stop=51,step=1))
# time_idx = [0,1]

# make a corner plot
data_np = data_pd.values
labels = data_np[label_idx,1]
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

# get requested data
cnt=0
for i in range(num_trials):
    if i == 0:
        corner_data = data_np[label_idx,:]
        corner_data = corner_data[:,time_idx].T
        cnt+=59
        continue
    corner_data = np.vstack([corner_data,data_np[(np.array(label_idx)+cnt),:][:,time_idx].T])
    cnt+=59

# make corner plot
figure = corner.corner(corner_data, quantiles=(0.16,0.84), labels=labels,label_kwargs=dict(fontsize='9'))
plt.savefig('corner_result.pdf')
plt.close()
