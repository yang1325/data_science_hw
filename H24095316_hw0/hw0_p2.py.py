#!/usr/bin/env python
# coding: utf-8

# In[101]:


#讀取資料並存入List
file=open('D:\\IMDB-Movie-Data (1).csv','rt')
movie_list=file.read()
movie_list=movie_list.split("\n")
del movie_list[0]
del movie_list[-1]
for x in range(len(movie_list)):
    movie_list[x]=movie_list[x].split(",")
    movie_list[x][2]=set(movie_list[x][2].split("|"))
    movie_list[x][4]=movie_list[x][4].split("|")


# In[102]:


#讀取資料中的電影評價並為2016年的電影+10分的評價,使得排列時2016年的電影並評價高的電影靠前,並顯示
def rating_2016(movie):
    rating=float(movie[7])
    if(movie[5]=="2016"):
        rating+=10
    return rating
movie_list=sorted(movie_list,key=rating_2016,reverse=True)
print("Ans1:\nThe top 3 rating movie in 2016 are:")
y=0
x=0
while(x<3):
    print("movie in 2016 of rating number",x+1,":<",movie_list[x+y][1],">,rating:",movie_list[x+y][7],end="")
    while(rating_2016(movie_list[x])==rating_2016(movie_list[x+y+1])):
        print(":<",movie_list[x+y][1],">,rating:",movie_list[x+y][7],end="")
        y+=1
    x+=1
    print()


# In[103]:


#讀取資料中電影的收視率和演員演出電影數並記在兩個字典里,然後以此計算演員的平均收視率並排列,並顯示
actor_revenue=dict()
actor_movie_number=dict()
for movie in movie_list:
    if(movie[9]==""):
        continue
    for actor in movie[4]:
        if(actor_revenue.get(actor,"does not exsit")=="does not exsit"):
            actor_revenue[actor]=float(movie[9])
            actor_movie_number[actor]=1
        else:
            actor_revenue[actor]+=float(movie[9])
            actor_movie_number[actor]+=1
actor_averange_revenue=[]
for actor in list(actor_revenue):
    averange=actor_revenue[actor]
    averange/=actor_movie_number[actor]
    actor_averange_revenue+=[[actor,averange]]
def arrange_revenue(the_actor_averange):
    return the_actor_averange[1]
actor_averange_revenue=sorted(actor_averange_revenue,key=arrange_revenue,reverse=True)
print("Ans2:\nThe actors who generate most averange revenue(",arrange_revenue(actor_averange_revenue[0]),")are:")
for x in range(len(actor_averange_revenue)):
    if (arrange_revenue(actor_averange_revenue[x])==arrange_revenue(actor_averange_revenue[0])):
        print(actor_averange_revenue[x][0])
    else:
        break


# In[104]:


#與第二題的方法相似,而只讀取有Emma Watson的電影的評價,將結果計算出並顯示
Emma_Watson_rating=0
Emma_Watson_number=0
for movie in movie_list:
    for actor in movie[4]:
        if(actor!="Emma Watson"):
            continue
        Emma_Watson_rating+=float(movie[7])
        Emma_Watson_number+=1
Emma_Watson_averange_rating=Emma_Watson_rating/Emma_Watson_number
print("Ans3:\nEmma Watson’s averange revenue is:",Emma_Watson_averange_rating)


# In[105]:


#設立一個串列紀錄與一個導演合作的每一個演員(的集合)和一個紀錄該集合位置的字典,然後將導演和演員集合配對並記錄在一個合作關係串列,
#然後根據演員集合的長度排列並顯示
directors=dict()
the_actors=[]
for movie in movie_list:
    if(directors.get(movie[3],"does not exist")=="does not exist"):
        directors[movie[3]]=len(the_actors)
        the_actors+=[set(movie[4])]
    else:
        the_actors[directors[movie[3]]]=the_actors[directors[movie[3]]]|set(movie[4])
director_coorperate_actors=[]
for director in list(directors):
    director_coorperate_actors+=[[director,the_actors[directors[director]]]]
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


# In[106]:


#與第四題的方法類似,只是字串裡存入的是由集合表示的劇種組成的串列,用集合的數量排列,並顯示
actors=dict()
the_genres=[]
for movie in movie_list:
    for actor in movie[4]:
        if(actors.get(actor,"does not exist")=="does not exist"):
            actors[actor]=len(the_genres)
            the_genres+=[[movie[2]]]
        elif(the_genres[actors[actor]].count(movie[2])==0):
            the_genres[actors[actor]]+=[movie[2]]
actors_genres=[]
for actor in list(actors):
    actors_genres+=[[actor,the_genres[actors[actor]]]]
def determine_generes_len(actor):
    return len(actor[1])
actors_genres=sorted(actors_genres,key=determine_generes_len,reverse=True)
print("Ans5:\nTop-2 actors playing in the most genres of movies are :")
print("number1:",actors_genres[0][0],"of playing",len(actors_genres[0][1]),'types of movies')
print("number2:",actors_genres[1][0],"of playing",len(actors_genres[1][1]),'types of movies')


# In[107]:


#建立兩個字典分別記錄演員的最近和最遠年份,然後存入一個串列,由最近和最遠年份的差來排列並顯示
actors_near_now=dict()
actors_far_now=dict()
for movie in movie_list:
    for actor in movie[4]:
        if(actors_far_now.get(actor,"does not exist")=="does not exist"):
            actors_near_now[actor]=int(movie[5])
            actors_far_now[actor]=int(movie[5])
        else:
            if(actors_near_now[actor]<int(movie[5])):
                actors_near_now[actor]=int(movie[5])
            elif(actors_far_now[actor]>int(movie[5])):
                actors_far_now[actor]=int(movie[5])
actors_gaps_year=[]
for actor in list(actors_near_now):
    actors_gaps_year+=[[actor,[actors_near_now[actor],actors_far_now[actor]]]]
def gap_years(actor):
    return (actor[1][0]-actor[1][1])
actors_gaps_year=sorted(actors_gaps_year,key=gap_years,reverse=True)
print("Ans6:\nThe actors who has the most maximum gaps of years(",gap_years(actors_gaps_year[0]),")are:")
for actor in actors_gaps_year:
    if(gap_years(actor)==gap_years(actors_gaps_year[0])):
        print(actor[0],",",actor[0],",from",actor[1][0],"to",actor[1][1])
    else:
        break


# In[108]:


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




