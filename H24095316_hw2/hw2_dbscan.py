#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import math

UNCLASSIFIED = False
NOISE = -1


# In[9]:


def _dist(p,q):
    # compute and return the euclidean distance
    # put your code here
    distance=((p[0]-q[0])**2+(p[1]-q[1])**2)**(1/2)
    return distance


# In[10]:


def _eps_neighborhood(p,q,eps):
    # check if the distance between p and q is below eps
    # return True or False
    # put your code here
    return (_dist(p,q)<=eps)


# In[11]:


def _region_query(m, point_id, eps):
    # find and return all points that belong to eps-neighborhood of point_id
    # put your code here
    n_points = m.shape[1]
    seeds = []
    for i in range(n_points):
        if(_eps_neighborhood([m[0,i],m[1,i]],[m[0,point_id],m[1,point_id]],eps)):
            seeds += [i]
    return seeds


# In[12]:


def _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    # expand the cluster of cluster_id from point_id
    # identify all points belonging to cluster_id
    # update the clustering results in "classification" by assigning cluster_id to each point
    # return True if point_id is a core, False if point_id is not a core
    # write your code below
    the_points_list=_region_query(m, point_id, eps)
    if(len(the_points_list)>=min_points):
        classifications[point_id]=cluster_id
        for x in the_points_list:
            if(classifications[x]!=UNCLASSIFIED):
                continue
            classifications,determined=_expand_cluster(m, classifications, x, cluster_id, eps, min_points)
            if (not determined):
                classifications[x]=cluster_id
    return classifications,(len(_region_query(m, point_id, eps))>=min_points)


# In[13]:


def dbscan(m, eps, min_points):
    """Implementation of DBSCAN
    You can refer to wikipedia for detailed algorithm: https://en.wikipedia.org/wiki/DBSCAN
    Use Euclidean Distance as the measure
    
    Inputs:
    m - A matrix whose columns are feature vectors
    eps - Maximum distance two points can be to be regionally related
    min_points - The minimum number of points to make a cluster
    
    Outputs:
    An array with either a cluster id number or dbscan.NOISE (None) for each column vector in m
    """
    cluster_id = 1
    n_points = m.shape[1]
    classifications = [UNCLASSIFIED] * n_points    
    # the main dbscan algorithm
    # put your code here
    while(classifications.count(UNCLASSIFIED)!=0):
        n=classifications.index(UNCLASSIFIED)
        while(len(_region_query(m, n, eps))<=min_points or classifications[n]!=UNCLASSIFIED):
            n+=1
            if(n==n_points):
                while(classifications.count(UNCLASSIFIED)!=0):
                    classifications[classifications.index(UNCLASSIFIED)]=NOISE
                break
        if(n==n_points):
            break
        classifications,determine=_expand_cluster(m, classifications,n, cluster_id, eps, min_points)
        cluster_id+=1
    return classifications


# In[14]:


# test here
import pandas as pd
import numpy as np
##
##
import os
os.chdir("D:\\hw2\\hw2_dbscan")
dataset_1 = pd.read_csv('blobs.csv')[:80].values
m = np.asmatrix(dataset_1)
m = m.transpose()


# In[15]:


eps = 1.6
min_points = 5
a = dbscan(m, eps, min_points)


# In[16]:


get_ipython().run_line_magic('matplotlib', 'inline')
import dbscan_lab_helper as helper

result = np.asarray(a)
helper.plot_clustered_dataset(dataset_1, result, neighborhood=True, epsilon=eps)


# In[17]:


dataset_2 = pd.read_csv('varied.csv')[:300].values
m = np.asmatrix(dataset_2)
m = m.transpose()


# In[18]:


eps = 1.3
min_points = 5
a = dbscan(m, eps, min_points)


# In[19]:


result = np.asarray(a)
helper.plot_clustered_dataset(dataset_2, result, xlim=(-14, 5), ylim=(-12, 7), neighborhood=True, epsilon=eps)


# In[ ]:




