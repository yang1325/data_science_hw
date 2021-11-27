#!/usr/bin/env python
# coding: utf-8

# In[31]:


#讀取資料並用兩個串列分別存入x座標和y座標
import pandas
import os
os.chdir("D:\\")
file=pandas.read_csv("cdata.csv")
pointx_list=[]
pointy_list=[]
for i in range(len(file)):
    pointx_list+=[file.iloc[i]["x"]]
    pointy_list+=[file.iloc[i]["y"]]


# In[32]:


#定義距離,產生中心點方法,和分群和找出新的中心點的方法
import random
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)
def cerate_center(x_list,y_list,k):
    distance_list=[]
    rad=(random.randint(0,len(x_list)-1))
    center_list=[[x_list[rad]],[y_list[rad]]]
    for i in range(k-1):
        max_index=0
        pointer=0
        max_distance=0
        for x,y in zip(x_list,y_list):
            the_distance=[]
            for r in range(len(center_list[0])):
                the_distance+=[distance(x,y,center_list[0][r],center_list[1][r])]
            min_distance=min(the_distance)
            if(min_distance>max_distance):
                max_distance=float(min_distance)
                max_index=int(pointer)
            pointer+=1
        center_list[0]+=[x_list[max_index]]
        center_list[1]+=[y_list[max_index]]
    return center_list
def regenerate_center(xs_list,ys_list,the_center_list):
    pointer=0
    number=0
    new_xs_list=[]
    new_ys_list=[]
    new_center_list=[[],[]]
    for center in the_center_list[0]:
        new_xs_list+=[[]]
        new_ys_list+=[[]]
    for x_list,y_list in zip(xs_list,ys_list):
        for x,y in zip(x_list,y_list):
            the_distance=[]
            for r in range(len(the_center_list[0])):
                the_distance+=[distance(x,y,the_center_list[0][r],the_center_list[1][r])]
            min_distance_index=the_distance.index(min(the_distance))
            new_xs_list[min_distance_index]+=[x]
            new_ys_list[min_distance_index]+=[y]
            if(min_distance_index!=pointer):
                number+=1
        pointer+=1
    for x_list,y_list in zip(new_xs_list,new_ys_list):
        new_center_list[0]+=[sum(x_list)/len(x_list)]
        new_center_list[1]+=[sum(y_list)/len(y_list)]
    return [new_xs_list,new_ys_list,new_center_list,number]


# In[33]:


#運用函數並繪圖
import matplotlib.pyplot as plt
n=20
times=0
Total_x_list=[]
Total_y_list=[]
Total_center_list=[]
The_center_list=cerate_center(pointx_list,pointy_list,4)
new_pointx_list=[pointx_list]
new_pointy_list=[pointy_list]
while(n!=0 and times-n<10):
    times+=1
    data_list=regenerate_center(new_pointx_list,new_pointy_list,The_center_list)
    new_pointx_list=data_list[0]
    new_pointy_list=data_list[1]
    The_center_list=data_list[2]
    n=data_list[3]
    Total_x_list+=[new_pointx_list]
    Total_y_list+=[new_pointy_list]
    Total_center_list+=[The_center_list]
if(isinstance(times**(1/2),int)):
    times**=1/2
    times2=times
else:
    times=int(times**(1/2))+2
    times2=times-2
n=0
colour_code=["#FF0000","#00FF00","#0000FF","#FFFF00"]
label_list=["A","B","C","D"]
for i in range(len(Total_x_list)):
    plt.subplot(times,times2,i+1)
    for r in range(4):
        plt.scatter(Total_x_list[i][r],Total_y_list[i][r],c=colour_code[r],label=label_list[r])
    plt.scatter(Total_center_list[i][0],Total_center_list[i][1],c="#000000",marker="X",label="Centriod")
    plt.title("Round%d"%(i+1))


# In[34]:


#使函數運用在2至50的範圍並記錄SSE並繪圖
SSE_list=[]
for K in range(2,51):
    n=20
    times=0
    The_center_list=cerate_center(pointx_list,pointy_list,K)
    new_pointx_list=[pointx_list]
    new_pointy_list=[pointy_list]
    while(n!=0 and times-n<10):
        times+=1
        data_list=regenerate_center(new_pointx_list,new_pointy_list,The_center_list)
        new_pointx_list=data_list[0]
        new_pointy_list=data_list[1]
        The_center_list=data_list[2]
        n=data_list[3]
    SSE=0
    for i in range(K):
        for x,y in zip(new_pointx_list[i],new_pointy_list[i]):
            SSE+=distance(x,y,The_center_list[0][i],The_center_list[1][i])
    SSE_list+=[SSE]
plt.plot(list(range(2,51)),SSE_list)
plt.title("SSE from k=2 to k=50")
plt.xlabel('Number of k')
plt.ylabel('Sum of square error')


# In[35]:


#使函數運用10在10並記錄SSE並繪圖
SSE_list=[]
for K in range(10):
    n=20
    times=0
    The_center_list=cerate_center(pointx_list,pointy_list,10)
    new_pointx_list=[pointx_list]
    new_pointy_list=[pointy_list]
    while(n!=0 and times-n<10):
        times+=1
        data_list=regenerate_center(new_pointx_list,new_pointy_list,The_center_list)
        new_pointx_list=data_list[0]
        new_pointy_list=data_list[1]
        The_center_list=data_list[2]
        n=data_list[3]
    SSE=0
    for integer in range(10):
        for x,y in zip(new_pointx_list[integer],new_pointy_list[integer]):
            SSE+=distance(x,y,The_center_list[0][integer],The_center_list[1][integer])
    SSE_list+=[SSE]
X=list(range(10))
plt.bar(X,SSE_list)
plt.title("result of ten times randomly pick initial point")
plt.xlabel('Fix k=10')
plt.ylabel('Sum of square error')


# In[ ]:




