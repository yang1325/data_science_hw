#!/usr/bin/env python
# coding: utf-8

# ## HW2 | KNN Graph Instruction
# 
# #### 1. Fill in all code (under # put your code here)
# 
# #### 2. Must use Pandas or Numpy if there is an instruction 
# 
# #### 3. Generate the plot that is exactly the same as the table right after each code block
# 
# #### 4. Answer the question at the end of this jupyter notebook
# 

# In[199]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


# ## Swiss Banknote Dataset
# 
# Six variables measured on 100 genuine and 100 counterfeit old Swiss 1000-franc
# bank notes. The data stem from Flury and Riedwyl (1988). The columns correspond
# to the following one label and six variables:
# 
# 0. Conterfeit - 0: genuine bank notes、1: genuine bank notes (Labels)
# 
# 
# 1. Length - Length of the bank note
# 
# 
# 2. Left - Height of the bank note, measured on the left
# 
# 
# 3. Right - Height of the bank note, measured on the right
# 
# 
# 4. Bottom - Distance of inner frame to the lower border
# 
# 
# 5. Top - Distance of inner frame to the upper border
# 
# 
# 6. Diagonal - Length of the diagonal
# 
# 
# 
# More details: [Kaggle | Swiss banknote conterfeit detection](https://www.kaggle.com/chrizzles/swiss-banknote-conterfeit-detection)

# In[200]:


# Use [Pandas] to import data | banknotes.csv
# Put your code here 
import os
os.chdir("D:\\hw2\\hw2_knn_graph")
bank = pd.read_csv('banknotes.csv')
label = bank.conterfeit

bank.head()


# In[201]:


# Use [Numpy function] to stack the following columns
# The 5-th column "Bottom" as X, the 6-th column "Top" as Y
# Put your code here
data_xy = np.array([bank["Bottom"],bank["Top"]])
data_xy = data_xy.transpose()
data_xy


# In[202]:


# Use [Numpy function] to find where label = 0 / label = 1
# Put your code here

index_0 = np.array([bank["Bottom"][bank["conterfeit"]==0],bank["Top"][bank["conterfeit"]==0]])
index_1 = np.array([bank["Bottom"][bank["conterfeit"]==1],bank["Top"][bank["conterfeit"]==1]])

# Use data_xy to plot the scatter plot 
# Label = 0 → color = green | Label = 1 → color = red
# Fill X and Y in the plt.scatter 
# Remember to put on grid and legend and equal axis
# Put your code here

plt.figure(figsize = (10, 10))
plt.scatter(index_0[0],index_0[1],s=20, color = "green",alpha=0.8,label="real banknote")
plt.scatter(index_1[0],index_1[1],s=20, color = "red",alpha=0.8,label="fake banknote")
plt.legend(loc="upper right")
plt.axis('equal')
plt.grid(b=True)


# In[203]:


# Use [Numpy function] to calculate the squared distance matrix between each points
# Put your code here
x_points=data_xy[:,0][:,np.newaxis]
x_points_=data_xy[:,0][np.newaxis,:]
y_points=data_xy[:,1][:,np.newaxis]
y_points_=data_xy[:,1][np.newaxis,:]
dist_sq = ((x_points_-x_points)**2+(y_points_-y_points)**2)


# In[204]:


dist_sq


# In[205]:


def nearest_partition(dist_sq, K):
    # Use [Numpy function] to return the "K Nearest Neighbor"
    # Put your code here
    the_main_array=[]
    for i in range(len(dist_sq)):
        minimum=np.sort(dist_sq[i])[K]
        the_array=np.where(dist_sq[i]<minimum)
        the_equal=np.where(dist_sq[i]==minimum)
        length=len(the_array[0])
        for r in range(K+1-length):
            the_array=np.append(the_array,np.array([the_equal[0][r]]))
        the_array=np.setdiff1d(the_array,i)
        the_main_array+=[the_array]
    return the_main_array


# In[206]:


# Use [Numpy function] to find where label = 0 / label = 1
# Put your code here

index_0 = np.array([bank["Bottom"][bank["conterfeit"]==0],bank["Top"][bank["conterfeit"]==0]])
index_1 = np.array([bank["Bottom"][bank["conterfeit"]==1],bank["Top"][bank["conterfeit"]==1]])


# Use data_xy to plot the scatter plot 
# Label = 0 → color = green | Label = 1 → color = red
# Fill X and Y in the plt.scatter
# Remember to put on grid and legend and equal axis
# Put your code here

plt.figure(figsize = (10, 10))
plt.scatter(index_0[0],index_0[1],s=20, color = "green",alpha=0.8,label="real banknote")
plt.scatter(index_1[0],index_1[1],s=20, color = "red",alpha=0.8,label="fake banknote")
plt.legend(loc="upper right")
plt.axis('equal')
plt.grid(b=True)
    
# Draw lines from each point to its three nearest neighbors (set K=3)
# Use some zip magic to make it happen (Hint is at below cell)
# You might need loops to generate the plot below
# set parameter [color='black', linewidth=1, alpha=0.5] when you draw lines 
# Put your code here

K = 3
plot_data=nearest_partition(dist_sq, K)
for i in range(len(plot_data)):
    for r in range(len(plot_data[i])):
        plt.plot(*zip([bank.iloc[plot_data[i][r]]["Bottom"],bank.iloc[plot_data[i][r]]["Top"]]
                      ,[bank.iloc[i]["Bottom"],bank.iloc[i]["Top"]]), color='black', linewidth=1, alpha=0.5)


# In[207]:


# Set seed = 10 | Random select three dots from data_xy
# Save dots index in varible "target" 
# Don't need to change below three lines

random.seed(10)
target = np.array([random.randint(0, len(data_xy)) for i in range(3)])
text = ['A', 'B', 'C']


# Use [Numpy function] to find where label = 0 / label = 1
# Put your code here
the_index_0=list(bank["conterfeit"]==0)
the_index_1=list(bank["conterfeit"]==1)
target_dot=[[],[]]
for i in target:
    the_index_0[i]=False
    the_index_1[i]=False
    target_dot[0]+=[bank.iloc[i]["Bottom"]]
    target_dot[1]+=[bank.iloc[i]["Top"]]
index_0 = np.array([bank["Bottom"][the_index_0],bank["Top"][the_index_0]])
index_1 = np.array([bank["Bottom"][the_index_1],bank["Top"][the_index_1]])

# Use data_xy to plot the scatter plot 
# Label = 0 → color = green | Label = 1 → color = red | Target → color = blue
# Fill X and Y in the plt.scatter
# Remember to put on grid and legend and equal axis
# Put your code here

plt.figure(figsize = (10, 10))
plt.scatter(index_0[0],index_0[1],s=20, color = "green",alpha=0.8,label="real banknote")
plt.scatter(index_1[0],index_1[1],s=20, color = "red",alpha=0.8,label="fake banknote")
plt.scatter(target_dot[0], target_dot[1],s=60, color = "blue",label="target dot") # Target dots
plt.legend(loc="upper right")
plt.axis('equal')
plt.grid(b=True)


# Draw lines from the selected three point to its three nearest neighbors (set K=3)
# Use some zip magic to make it happen (Hint is at below cell)
# You might need loops to generate the plot below
# set parameter [color='black', linewidth=1, alpha=0.5] when you draw lines 
# Put text A, B, C on each dots (location: Right + 0.1、 Up + 0.1)
# Put your code here


K = 3
for i in target:
    for r in range(len(plot_data[i])):
        plt.plot(*zip([bank.iloc[plot_data[i][r]]["Bottom"],bank.iloc[plot_data[i][r]]["Top"]]
                      ,[bank.iloc[i]["Bottom"],bank.iloc[i]["Top"]]), color='black', linewidth=1, alpha=0.5)
for i in range(len(text)):
    plt.annotate(text[i], (target_dot[0][i]+0.1, target_dot[1][i]+0.1))


# ### Question：由上圖進行判斷，回答 ABC 三點各自被 KNN 分為哪一群，並說明原因。
# 
# ### Your Answer：

# In[ ]:


print("由上圖進行判斷,A 屬於fake banknote,因為它至少與兩個fake banknote 的資料點靠近")
print("由上圖進行判斷,C 屬於fake banknote,因為它與三個fake banknote 的資料點靠近")
print("由上圖進行判斷,B 屬於real banknote,因為它與三個real banknote 的資料點靠近")


# In[ ]:


# Hint: How to drow a line between two dots

dots = np.array([[1, 2], [6, 3], [5, 6]])

plt.figure(figsize=(15, 5))

plt.subplot(121)
plt.title('Wrong way')        
for i in range(len(dots)):
    plt.scatter(dots[i][0], dots[i][1], color='red')

for i in range(len(dots)):
    for j in range(len(dots)):
        plt.plot(dots[i], dots[j], color = 'black')

plt.subplot(122)
plt.title('Right way')

for i in range(len(dots)):
    plt.scatter(dots[i][0], dots[i][1], color='red')

for i in range(len(dots)):
    for j in range(len(dots)):
        plt.plot(*zip(dots[i], dots[j]), color = 'blue')


# In[ ]:




