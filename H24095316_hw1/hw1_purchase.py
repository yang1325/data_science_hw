#!/usr/bin/env python
# coding: utf-8

# In[37]:


#讀取資料
import pandas
import os
os.chdir("D:\\")
file=pandas.read_csv("purchase_data.csv")
file.head()


# In[38]:


#定義一個可以將串列中的所有的元素放在一個集合內並輸出集合長度的count函數,再將該函數apply到玩家名稱上得到結果
def count(x):
    set1=set()
    for y in x:
        set1.add(y)
    return len(set1)
total_number=pandas.DataFrame({"Total Players":pandas.Series([file.apply(count)[1]])})
total_number


# In[39]:


#用count函數算出"Number of Unique Items",定義一個sum函數並以此算出總收入,再用資料長度得到平均收入和購買發生次數
def the_sum(x):
    for number in x:
        if(not(isinstance(number,float))):
            return -1
    return x.sum()
revernue=file.apply(the_sum)[6]
number_of_items=file.apply(count)[4]
dict_data=dict()
dict_data["Number of Unique Items"]=[number_of_items]
dict_data["Average Price"]=[round(revernue/len(file),2)]
dict_data["Number of Purchases"]=[len(file)]
dict_data["Total Revenue"]=[revernue]
pandas.DataFrame(dict_data)


# In[40]:


#用bool_vector將資料中的三種性別分開,並用count函數得到個別數量,並以此計算百分比
Gender_list=["Male","Female","Other / Non-Disclosed"]
Percentage_of_Players=[]
Total_Count=[]
for gender in Gender_list:
    vector=[]
    for i in range(len(file)):
        vector+=[(file.iloc[i]["Gender"]==gender)]
    data=file[vector]
    Total_Count+=[data.apply(count)[1]]
    Percentage_of_Players+=[round(data.apply(count)[1]/file.apply(count)[1]*100,2)]
Ans3=pandas.DataFrame({"Percentage of Players":pandas.Series(Percentage_of_Players,index=Gender_list),
                 "Total Count":pandas.Series(Total_Count,index=Gender_list)})
Ans3


# In[41]:


#用bool_vector將資料中的三種性別分開,用sum函數算出總收入,再用資料長度和第三題的結果得到平均收入,每人平均收入和購買發生次數
data_dict=dict()
Gender_list=["Female","Male","Other / Non-Disclosed"]
Purchase_Count=[]
Average_Purchase_Price=[]
Total_Purchase_Value=[]
Avg_Purchase_Total_per_Person=[]
for gender in Gender_list:
    vector=[]
    for i in range(len(file)):
        vector+=[(file.iloc[i]["Gender"]==gender)]
    data=file[vector]
    Purchase_Count+=[len(data)]
    Total_Purchase_Value+=[data["Price"].sum()]
    Average_Purchase_Price+=[round(data["Price"].sum()/len(data),5)]
    Avg_Purchase_Total_per_Person+=["$"+str(round(data["Price"].sum()/Ans3.loc[gender]["Total Count"],2))]
for i in range(len(Gender_list)):
    Gender_list[i]=tuple([Gender_list[i]])
pandas.DataFrame({"Purchase Count":Purchase_Count,
                 "Average Purchase Price":Average_Purchase_Price,
                 "Total Purchase Value":Total_Purchase_Value,
                 "Avg Purchase Total per Person":Avg_Purchase_Total_per_Person},
                 index=pandas.MultiIndex.from_tuples(Gender_list,names=["Gender"]))


# In[42]:


#用cut函數分出年齡段,並用與第三題相似的方法(以年齡標籤取代性別標籤)
Age_list=["<10","10-14","15-19","20-24","25-29","30-34","35-39","40+"]
file["Age seperation"]=pandas.cut(file["Age"],[0,10,15,20,25,30,35,40,999],labels=Age_list,right=False)
Percentage_of_Players=[]
Total_Count=[]
for age in Age_list:
    vector=[]
    for i in range(len(file)):
        vector+=[(file.iloc[i]["Age seperation"]==age)]
    data=file[vector]
    Total_Count+=[data.apply(count)[1]]
    Percentage_of_Players+=[round(data.apply(count)[1]/file.apply(count)[1]*100,2)]
Ans5=pandas.DataFrame({"Percentage of Players":pandas.Series(Percentage_of_Players,index=Age_list),
                 "Total Count":pandas.Series(Total_Count,index=Age_list)})
Ans5


# In[43]:


#用cut函數分出年齡段,並用與第四題相似的方法(以年齡標籤取代性別標籤)
Purchase_Count=[]
Average_Purchase_Price=[]
Total_Purchase_Value=[]
Avg_Purchase_Total_per_Person=[]
for age in Age_list:
    vector=[]
    for i in range(len(file)):
        vector+=[(file.iloc[i]["Age seperation"]==age)]
    data=file[vector]
    Purchase_Count+=[len(data)]
    Total_Purchase_Value+=["$"+str(round(data["Price"].sum(),2))]
    Average_Purchase_Price+=["$"+str(round(data["Price"].sum()/len(data),2))]
    Avg_Purchase_Total_per_Person+=["$"+str(round(data["Price"].sum()/Ans5.loc[age]["Total Count"],2))]
pandas.DataFrame({"Purchase Count":pandas.Series(Purchase_Count,index=Age_list),
                 "Average Purchase Price":pandas.Series(Average_Purchase_Price,index=Age_list),
                 "Total Purchase Value":pandas.Series(Total_Purchase_Value,index=Age_list),
                 "Avg Purchase Total per Person":pandas.Series(Avg_Purchase_Total_per_Person,index=Age_list),})


# In[44]:


#讀取玩家消費次數和消費數據並建立兩個字典,並以消費次數來排列,用前讀取的資料進行運算後輸出
Total_Purchase_Value_dict=dict()
Purchase_Count_dict=dict()
for i in range(len(file)):
    Total_Purchase_Value_dict[file.iloc[i]["SN"]]=Total_Purchase_Value_dict.get(file.iloc[i]["SN"],0)+file.iloc[i]["Price"]
    Purchase_Count_dict[file.iloc[i]["SN"]]=Purchase_Count_dict.get(file.iloc[i]["SN"],0)+1
Total_Purchase_Value_list=[]
for player in list(Total_Purchase_Value_dict):
    Total_Purchase_Value_list+=[[player,Total_Purchase_Value_dict[player]]]
def compare(player):
    return player[1]
Total_Purchase_Value_list=sorted(Total_Purchase_Value_list,key=compare,reverse=True)
player_list=[]
Purchase_Count=[]
Average_Purchase_Price=[]
Total_Purchase_Value=[]
for i in range(5):
    player_list+=[Total_Purchase_Value_list[i][0]]
    Purchase_Count+=[Purchase_Count_dict[Total_Purchase_Value_list[i][0]]]
    Average_Purchase_Price+=["$%.2f"%(Total_Purchase_Value_list[i][1]/Purchase_Count_dict[Total_Purchase_Value_list[i][0]])]
    Total_Purchase_Value+=["$%.2f"%(Total_Purchase_Value_list[i][1])]
for i in range(len(player_list)):
    player_list[i]=tuple([player_list[i]])
pandas.DataFrame({"Purchase Count":Purchase_Count,
                 "Average Purchase Price":Average_Purchase_Price,
                 "Total Purchase Value":Total_Purchase_Value},
                index=pandas.MultiIndex.from_tuples(player_list,names=["SN"]))


# In[45]:


#與第七題的方法類似
Item_Price_dict=dict()
Purchase_Count_dict=dict()
Item_name_dict=dict()
for i in range(len(file)):
    Item_name_dict[file.iloc[i]["Item ID"]]=file.iloc[i]["Item Name"]
    Item_Price_dict[file.iloc[i]["Item ID"]]=file.iloc[i]["Price"]
    Purchase_Count_dict[file.iloc[i]["Item ID"]]=Purchase_Count_dict.get(file.iloc[i]["Item ID"],0)+1
Item_list=[]
for item in list(Purchase_Count_dict):
    total=Item_Price_dict[item]*Purchase_Count_dict[item]
    Item_list+=[[item,Item_name_dict[item],Item_Price_dict[item],Purchase_Count_dict[item],total]]
def compare(item):
    return item[3]
Item_list=sorted(Item_list,key=compare,reverse=True)
ID_list=[]
Item_Price=[]
Purchase_Count=[]
Total_Purchase_Value=[]
for i in range(5):
    ID_list+=[(Item_list[i][0],Item_list[i][1])]
    Item_Price+=["$%.2f"%(Item_list[i][2])]
    Purchase_Count+=[Item_list[i][3]]
    Total_Purchase_Value+=["$%.2f"%(Item_list[i][4])]
pandas.DataFrame({"Purchase Count":Purchase_Count,
                 "Item Price":Item_Price,
                 "Total Purchase Value":Total_Purchase_Value},
                index=pandas.MultiIndex.from_tuples(ID_list,names=["Item ID","Item Name"]))


# In[46]:


#使用第八題的串列並以總金額排列,然後輸出
def compare(item):
    return item[4]
Item_list=sorted(Item_list,key=compare,reverse=True)
ID_list=[]
Item_Price=[]
Purchase_Count=[]
Total_Purchase_Value=[]
for i in range(5):
    ID_list+=[(Item_list[i][0],Item_list[i][1])]
    Item_Price+=["$%.2f"%(Item_list[i][2])]
    Purchase_Count+=[Item_list[i][3]]
    Total_Purchase_Value+=["$%.2f"%(Item_list[i][4])]
pandas.DataFrame({"Purchase Count":Purchase_Count,
                 "Item Price":Item_Price,
                 "Total Purchase Value":Total_Purchase_Value},
                index=pandas.MultiIndex.from_tuples(ID_list,names=["Item ID","Item Name"]))


# In[ ]:




