#!/usr/bin/env python
# coding: utf-8

# ## Instructions
# 
# #### 。 This homework has two parts
#     1. There are 6 simple questions, just follow the instrctions and get the same output as the following.
#     2. It's how simple neural networks working. As the same as part 1, just follow the instructions and get the same output
# 
# #### 。 All of this homework should use Numpy or Pandas
# 
# #### 。 Please follow the same variable name as the instuctions of every questions 

# ## Part 1

# **1. Import both numpy and pandas packages**

# In[197]:


import numpy as np
import pandas as pd


# **2. Create a 3x3 matrix with values ranging from 0 to 8**

# In[198]:


np.arange(0,9).reshape(3,3)


# **3. Create a 5x5 matrix with row values ranging from 0 to 4**

# In[199]:


b=np.arange(0,5)
np.array([b]*5)


# **4. How to swap the first and second rows of a**

# In[200]:


a = np.arange(25).reshape(5,5)
b=a[0]+0
a[0]=a[1]
a[1]=b
a


# **5. Give two ways to show how to get the n largest values of a (no sort the value is fine)**

# In[201]:


# Don't need to change this cell
a = np.arange(100)
np.random.shuffle(a)
n = 5


# In[202]:


# Way 1
max_list=[]
b=a+0
while(len(max_list)<n):
    maximum=b.max()
    max_list+=[maximum]
    b=b[b<maximum]
print(max_list)


# In[203]:


# Way 2
a=np.flip(np.sort(a))
print(a[:n])


# **6. Compare if array a and array b is totally the same**

# In[204]:


np.random.seed(123)
a = np.round(np.random.random(100)*100, 0)
b = np.random.randint(1, 100, 100)

# Put your code here
print(list(a-b)==[0]*100)


# ## Part 2

# ### Online Shoppers Purchasing Intention Dataset
# 
# The dataset consists of 10 numerical and 8 categorical attributes. The 'Revenue' attribute can be used as the class label.
# 
# * ``0 Administrative``, ``1 Administrative Duration``, ``2 Informational``, ``3 Informational Duration``, ``4 Product Related`` and ``5 Product Related Duration`` - represent the number of different types of pages visited by the visitor in that session and total time spent in each of these page categories. The values of these features are derived from the URL information of the pages visited by the user and updated in real time when a user takes an action, e.g. moving from one page to another. 
# 
# 
# * ``6 Bounce Rate``, ``7 Exit Rate`` and ``8 Page Value`` - represent the metrics measured by "Google Analytics" for each page in the e-commerce site. The value of "Bounce Rate" feature for a web page refers to the percentage of visitors who enter the site from that page and then leave ("bounce") without triggering any other requests to the analytics server during that session. The value of "Exit Rate" feature for a specific web page is calculated as for all pageviews to the page, the percentage that were the last in the session. The "Page Value" feature represents the average value for a web page that a user visited before completing an e-commerce transaction. 
# 
# 
# * ``9 Special Day`` - indicates the closeness of the site visiting time to a specific special day (e.g. Mother’s Day, Valentine's Day) in which the sessions are more likely to be finalized with transaction. The value of this attribute is determined by considering the dynamics of e-commerce such as the duration between the order date and delivery date. For example, for Valentina’s day, this value takes a nonzero value between February 2 and February 12, zero before and after this date unless it is close to another special day, and its maximum value of 1 on February 8. 
# 
# 
# * The dataset also includes ``11 operating system``, ``12 browser``, ``13 region``, ``14 traffic type``, ``15 visitor type`` as returning or new visitor, a Boolean value indicating whether the date of the visit is ``16 weekend``, and ``9 month of the year``.
# 
# 
# ---
# * **``17 Revenue``** - binary labels
# 
# 
# 
# * More information of this data: [UCI | Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset#)

# **Use pandas to import the data and check the shape of dataset and save it as `" shoppers "`**

# In[205]:


import os
os.chdir("D:\\hw2\\hw2_numpy")
shoppers = bank = pd.read_csv('online_shoppers_intention.csv')
print(shoppers.shape)


# **Use pandas function to let label be numeric as below and save it as `" label "`**

# In[206]:


label=np.zeros(len(shoppers),dtype=int)
label[shoppers["Revenue"]]=1
label


# **See some information of this data**

# In[207]:


shoppers.head()


# In[208]:


shoppers.describe()


# **Choose column [1, 4, 5, 11, 12, 14] and turn into numpy array ``" x "``**

# In[209]:


x = np.array([shoppers["Administrative_Duration"],shoppers["ProductRelated"],shoppers["ProductRelated_Duration"]
              ,shoppers["OperatingSystems"],shoppers["Browser"],shoppers["TrafficType"]])
x = x.transpose()


# In[210]:


x


# **Use numpy function to load weight data, bias data and check their shape**

# In[211]:


weight_1 = np.load(open("layer_1_weight.npy", "rb"))
weight_2 = np.load(open("layer_2_weight.npy", "rb"))

bias_1 = np.load(open("layer_1_bias.npy", "rb"))
bias_2 = np.load(open("layer_2_bias.npy", "rb"))


# In[212]:


print('weight_1 shape:', weight_1.shape)
print('weight_2 shape:', weight_2.shape)
print('')
print('bias_1 shape:', bias_1.shape)
print('bias_2 shape:', bias_2.shape)


# **Use numpy function to compute `" x "` and weight_1 matrix multiplication, and check the shape**

# In[213]:


x = x.dot(weight_1)
print(x.shape)


# **Use numpy function to compute `" x "` and bias_1 matrix addtion, and check the shape**

# In[214]:


x = x + bias_1
print(x.shape)


# **Use numpy function to compute `" x "` and weight_2 matrix multiplication, and check the shape**

# In[215]:


x = x.dot(weight_2)
print(x.shape)


# **Use numpy function to compute `" x "` and bias_2 matrix addtion, and check the shape**

# In[216]:


x = x + bias_2
print(x.shape)


# **Check if your x is same as below**

# In[217]:


x


# **Use numpy function to find out each row which one value is bigger, and save it as `" pre "`**

# In[218]:


pre = x.argmax(axis=1)
pre


# **Use numpy function to check if `pre[i]` is the same as `label[i]`, and save it as `" check "`**

# In[219]:


check = (pre+label-1)**2
check


# **Use numpy function to calculate the accuracy**

# In[220]:


print('accuracy:',check.mean())

