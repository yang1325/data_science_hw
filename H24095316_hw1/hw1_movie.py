#!/usr/bin/env python
# coding: utf-8

# In[73]:


#讀取資料
import pandas
import os
os.chdir("D:\\")
file=pandas.read_csv("IMDB-Movie-Data (1).csv")
file.head()


# In[74]:


#用bool_vector過濾出2016年的電影,再定義rating函數來找出前三排名的分數,再把符合分數的電影列印出來
def rating(column):
    for number in column:
        if(not(isinstance(number,float))):
            return -1
    column=sorted(column,reverse=True)
    rating_list=[]
    y=0
    z=[0,1,2]
    while(y<3):
        if(column[z[y]]==column[z[y]+1]):
            for x in range(2,y-1,-1):
                z[x]+=1
        else:
            rating_list+=[column[z[y]]]
            y+=1
    return rating_list
vector=[]
for i in range(len(file)):
    if(file.iloc[i]["Year"]==2016):
        vector+=[True]
    else:
        vector+=[False]
movie_2016=file[vector]
false_vector=[]
for x in range(len(movie_2016)):
    false_vector+=[False]
list1=movie_2016.apply(rating)[7]
print("Ans1:")
for x in range(3):
    print("The movie in 2016 of number",x+1,"are:")
    vector=list(false_vector)
    for y in range(len(movie_2016)):
        if(movie_2016.iloc[y]["Rating"]==list1[x]):
            vector[y]=True
    print(movie_2016[vector])


# In[75]:


#讀取資料中電影的收視率並記在ㄛ個字典里,然後以此計算演員的平均收視率並排列,並顯示
def mean(number_list):
    return sum(number_list)/len(number_list)
def get_actor(actor_string_list):
    all_actor_set=set()
    for actor_string in actor_string_list:
        if(not(isinstance(actor_string,str))):
            return -1
        actor_set=set(actor_string.split("|"))
        all_actor_set=all_actor_set | actor_set
    return all_actor_set
the_actor_set=file.apply(get_actor)[4]
actor_revernue=dict()
file.fillna(-1,inplace=True)
for i in range(len(file)):
    the_revernue=file.iloc[i]["Revenue (Millions)"]
    if (the_revernue==-1):
        continue
    actors_str=file.iloc[i]["Actors"]
    actor_list=actors_str.split("|")
    for actor in actor_list:
        actor_revernue[actor]=actor_revernue.get(actor,[])+[the_revernue]
def compare(actor_revernue):
    return actor_revernue[1]
actors_revernue_list=[]
for actor in list(actor_revernue):
    actor_revernue[actor]=mean(actor_revernue[actor])
    actors_revernue_list+=[[actor,actor_revernue[actor]]]
actors_revernue_list=sorted(actors_revernue_list,key=compare,reverse=True)
print("Ans2:")
print("the highest averange revernue are(",actors_revernue_list[0][1],"):",end="")
for x in range(len(actors_revernue_list)):
    if(actors_revernue_list[x][1]==actors_revernue_list[0][1]):
        print(actors_revernue_list[x][0],",",end="")
    else:
        print("with total",x,"actors")
        break


# In[76]:


def check_actor(actor,actor_string):
    actor_list=actor_string.split("|")
    if(actor_list.count(actor)!=0):
        return True
    return False
vector=[]
for i in range(len(file)):
    vector+=[check_actor("Emma Watson",file.iloc[i]["Actors"])]
actors_movies=file[vector]
Emma_Watson_rating=actors_movies["Rating"].sum()/len(actors_movies)
print("Ans3:\nEmma Watson’s averange rating is:",Emma_Watson_rating)


# In[77]:


#設立一個紀錄導演與合作的每一個演員(的集合)的字典,然後將導演和演員集合配對並記錄在一個合作關係串列,
#然後根據演員集合的長度排列並顯示
director_coorperate_actors_dict=dict()
for i in range(len(file)):
    director=file.iloc[i]["Director"]
    actor_string=file.iloc[i]["Actors"]
    actor_set=set(actor_string.split("|"))
    director_coorperate_actors_dict[director]=director_coorperate_actors_dict.get(director,set())|actor_set
director_coorperate_actors=[]
for director in list(director_coorperate_actors_dict):
    director_coorperate_actors+=[[director,director_coorperate_actors_dict[director]]]
def determine_name_len(director):
    return len(director[1])
director_coorperate_actors=sorted(director_coorperate_actors,key=determine_name_len,reverse=True)
print("Ans4:\nThe director who coorperate with most actors (:",len(director_coorperate_actors[0][1]),")are:",end="")
for x in range(len(director_coorperate_actors)):
    if(determine_name_len(director_coorperate_actors[x])==determine_name_len(director_coorperate_actors[0])):
        print(director_coorperate_actors[x][0])
        print(director_coorperate_actors[x][0],"cooperate wih:",end="")
        for y in list(director_coorperate_actors[x][1]):
            print(y,end=",")
        print("with total",len(director_coorperate_actors[0][1]),"actor")
    else:
        break


# In[78]:


#與第四題的方法類似,只是字串裡存入的是由(集合表示的劇種)組成的串列,用集合的數量排列,並顯示
def merge_list(the_list,the_set):
    if(the_list.count(the_set)==0):
        return the_list+[the_set]
    return the_list
actor_genres_dict=dict()
for i in range(len(file)):
    gernes_string=file.iloc[i]["Genre"]
    gernes_set=set(gernes_string.split("|"))
    actor_string=file.iloc[i]["Actors"]
    actor_list=actor_string.split("|")
    for actor in actor_list:
        actor_genres_dict[actor]=merge_list(actor_genres_dict.get(actor,[]),gernes_set)
actors_genres=[]
for actor in list(actor_genres_dict):
    actors_genres+=[[actor,actor_genres_dict[actor]]]
def determine_generes_len(actor):
    return len(actor[1])
actors_genres=sorted(actors_genres,key=determine_generes_len,reverse=True)
print("Ans5:\nTop-2 actors playing in the most genres of movies are :")
x=1
y=-1
while(x<3):
    print("number",x,"has",determine_generes_len(actors_genres[x+y]),"types,they are:",end="")
    while(determine_generes_len(actors_genres[x+y])==determine_generes_len(actors_genres[x+y+1])):
        print(actors_genres[x+y][0],",",end="")
        y+=1
    print(actors_genres[x+y][0],end="")
    print()
    x+=1


# In[79]:


#建立字典記錄演員的最近和最遠年份,然後存入一個串列,由最近和最遠年份的差來排列並顯示
def change_year(late_near,year):
    if(late_near[0]>year):
        return[year,late_near[1]]
    elif(late_near[1]<year):
        return[late_near[0],year]
    else:
        return late_near
actor_year_dict=dict()
for i in range(len(file)):
    movie_year=file.iloc[i]["Year"]
    actor_string=file.iloc[i]["Actors"]
    actor_list=actor_string.split("|")
    for actor in actor_list:
        actor_year_dict[actor]=change_year(actor_year_dict.get(actor,[movie_year,movie_year]),movie_year)
actors_gaps_year=[]
for actor in list(actor_year_dict):
    actors_gaps_year+=[[actor,actor_year_dict[actor]]]
def gap_years(actor):
    return (actor[1][1]-actor[1][0])
actors_gaps_year=sorted(actors_gaps_year,key=gap_years,reverse=True)
print("Ans6:\nThe actors who has the most maximum gaps of years(",gap_years(actors_gaps_year[0]),")are:")
for actor in actors_gaps_year:
    if(gap_years(actor)==gap_years(actors_gaps_year[0])):
        print(actor[0],",from",actor[1][0],"to",actor[1][1])
    else:
        break


# In[80]:


#把第三題的合作關係串列拿來修改成一個放有合作關係的人的集合的串列,再拿來製作一個有所有人員的集合B並複製一個備用C,和一個有人員和所與該人員
#有合作關係的人的集合的串列A,然後用串列A把集合B中與Johnny Depp有合作關係的人排除,再用C減去B得到結果,並顯示
for x in range(len(director_coorperate_actors)):
    director_coorperate_actors[x][1].add(director_coorperate_actors[x][0])
    director_coorperate_actors[x]=director_coorperate_actors[x][1]
all_actors_director_set=set()
for the_actors_and_director in director_coorperate_actors:
    all_actors_director_set=all_actors_director_set|the_actors_and_director
dict_operater=dict()
list_operater=[]
for directors_actor in list(all_actors_director_set):
    dict_operater[directors_actor]=len(list_operater) 
    the_set=set()
    for operaters in director_coorperate_actors:
        operaters_list=list(operaters)
        if(operaters_list.count(directors_actor)!=0):
            the_set=the_set|operaters
    the_set.remove(directors_actor)
    list_operater+=[the_set]
real_all_actors_director_set=set(all_actors_director_set)
Johnny_Depp_cooperate_set={"Johnny Depp"}
while(Johnny_Depp_cooperate_set!=set()):
    the_list=list(Johnny_Depp_cooperate_set)
    the_choosen_one=the_list[0]
    Johnny_Depp_cooperate_set.remove(the_choosen_one)
    all_actors_director_set.remove(the_choosen_one)
    the_list=list(all_actors_director_set)
    for actor in list(list_operater[dict_operater[the_choosen_one]]):
        if(the_list.count(actor)!=0):
            Johnny_Depp_cooperate_set.add(actor)
print("Ans7:\nThe actors or director who has collaborate with Johnny Depp in direct and indirect ways ",end="")
print("has",len(real_all_actors_director_set-all_actors_director_set),".They are:")
print(real_all_actors_director_set-all_actors_director_set)


# In[ ]:





# In[ ]:




