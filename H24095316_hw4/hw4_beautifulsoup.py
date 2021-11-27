#!/usr/bin/env python
# coding: utf-8

# # import packages
# Let's start by importing the following packages!
# * requests
# * BeautifulSoup
# * seaborn
# * matplotlib
# * pandas
# * re

# In[1]:


# import package
import requests
from bs4 import BeautifulSoup
import seaborn
import matplotlib
import pandas
import re


# # crawler THSR information
# Let's start to crawl the imformation of each station of THSR!
# * Target web: [THSR Homepage](https://www.thsrc.com.tw)  
# * Choose each station:
#     1. Homepage -> Travel Information -> Stations
#     2. choose different stations by changing url
# * Task:
#     1. crawler the name, address, operation hours and ticketing hours of each station
#     2. organize into a DataFrame

# In[2]:


# setting each station name and their url
url = "http://www.thsrc.com.tw/ArticleContent/2f940836-cedc-41ef-8e28-c2336ac8fe68"
website = "http://www.thsrc.com.tw"
response = requests.get(url)
soup = BeautifulSoup (response.text, "html.parser")
word = soup.find(class_ = "nav nav-tabs si-tab swiper-wrapper")
box = word.find_all('a')
station_list = []
for i in range(len(box)):
    station_list += [[website + box[i].get('href'),box[i].text]]


# In[3]:


# crawler the address of each station
for i in range(len(station_list)):
    url = station_list[i][0]
    response = requests.get(url)
    soup = BeautifulSoup (response.text, "html.parser")
    word = soup.find(class_ = "table")
    box = word.find(class_="google-map-link orange")
    station_list[i] += [box.text]


# In[4]:


# crawler the operation hours and ticketing hours of each station station_list[i] += [box.text]
for i in range(len(station_list)):
    url = station_list[i][0]
    response = requests.get(url)
    soup = BeautifulSoup (response.text, "html.parser")
    word = soup.find(class_ = "table")
    box = word.find_all(class_="gray")
    for j in range(2):
        box[j] = box[j].text
        box[j] = box[j].split('：')
        box[j] = box[j][1]
    del station_list[i][0]
    station_list[i] += [box[0], box[1]]


# In[5]:


# create a DataFrame
data = pandas.DataFrame(station_list, columns = ["station", "address", "operation_hours", "ticketing_hours"])
data


# # Crawler GDP and CPI
# Let's start to crawl GDP and CPI!
# * Target web: 
#     1. [Wiki GDP](https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal))  
#     2. [Wiki CPI](https://en.wikipedia.org/wiki/Corruption_Perceptions_Index)
# * Task:
#     1. crawler GDP table (top 50: United States ~ New Zealand)
#     2. organize into a DataFrame (columns: Country, Region, IMF_Estimate, IMF_Year, United_Nations_Estimate, United_Nations_Year, World_Bank_Estimate, World_Bank_Year)
#     3. crawler CPI table which contains country and 2020 CPI (top 100: Denmark ~ Suriname)
#     4. organize into a DataFrame (columns: Country, CPI_2020)
#     5. merge GDP(DataFrame) and CPI(DataFrame), based on Country of GDP
#     6. plot and text the names of GDP top 10 countrys

# In[6]:


# crawler GDP
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
response = requests.get(url)
soup = BeautifulSoup (response.text, "html.parser")
word = soup.find(class_ = "wikitable sortable static-row-numbers plainrowheaders srn-white-background")
box = word.find('tbody')
country_list = word.find_all('tr')
del country_list[0:2]
country_list = list(country_list)
data_list=[]
for i in range(len(country_list)):
    y = country_list[i]
    the_list = list(y.find_all('td'))
    country_data_list = []
    correction = 0
    for j in range(len(the_list)):
        x = the_list[j].text
        if(j == 0):
            x = x.split("\xa0")
            country_data_list += [x[1]]
        elif(j == 1):
            country_data_list += [x]
        elif(x == "N/A\n" or x == "N/A"):
            country_data_list += ["N/A", "N/A"]
            correction += 1
        elif((correction+j) % 2 == 0 ):
            x = x.split(",")
            x.reverse()
            number = 0
            for i in range(len(x)):
                number += int(x[i])*(1000**i)
            country_data_list += [number]
        else:
            x = x.split("]")
            x.reverse()
            x = x[0]
            x = x.split("\n")
            country_data_list += [x[0]]
    data_list += [country_data_list]


# In[7]:


# create GDP DataFrame
GDP_data = pandas.DataFrame(data_list, columns = [ 'Country', 'Region', 'IMF_Estimate', 'IMF_Year', 'United_Nations_Estimate'
                                              , 'United_Nations_Year', 'World_Bank_Estimate', 'World_Bank_Year'])
GDP_data.head(50)


# In[8]:


# crawler CPI
url = "https://en.wikipedia.org/wiki/Corruption_Perceptions_Index"
response = requests.get(url)
soup = BeautifulSoup (response.text, "html.parser")
word = soup.find(class_ = "wikitable sortable") 
box = word.find_all('tr')
box = list(box)
del box[0:2]
data_list = []
for i in range(len(box)):
    country_data_list = []
    country_list = box[i].find_all('td')
    x = country_list[1].text
    x = x.split("\xa0")
    x.reverse()
    country_data_list += [x[0]]
    x = country_list[2].text
    country_data_list += [int(x)]
    data_list += [country_data_list]


# In[9]:


# CPI DataFrame
CPI_data = pandas.DataFrame(data_list, columns = [ 'Country', 'CPI_2020'])
CPI_data.head(40)


# In[10]:


# merge GDP and CPI DataFrame
GDP_data = GDP_data.merge(CPI_data, on='Country', how="left")
GDP_data = GDP_data.dropna()
GDP_data


# In[11]:


# plot
GDP_data["World_Bank_Estimate"][GDP_data["World_Bank_Estimate"] == "N/A"] = GDP_data["United_Nations_Estimate"][GDP_data["World_Bank_Estimate"] == "N/A"]
seaborn.scatterplot(x = GDP_data.CPI_2020, y = GDP_data.World_Bank_Estimate, hue = GDP_data.Region)
for i in range(10):
    matplotlib.pyplot.annotate(GDP_data.Country[i], (GDP_data.CPI_2020[i], GDP_data.World_Bank_Estimate[i]))


# In[ ]:




