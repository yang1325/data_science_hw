#!/usr/bin/env python
# coding: utf-8

# ## Association Rule Mining in Retail Store
# 
# ### Problem Statement:
#  * What are the items that may be frequently purchased together?
# 
# ### Objective:
# * To learn how Apriori Algorithm and Association Rules works.
# * To learn how Combination and Permutation helps to find Support and Confidence of itemsets respectively.
# * To find frequent itemsets with high confidence and lift, keeping both item together will help to increase sales.
# 

# ### Introduction
# * Association rule mining is one of an important technique of data mining for knowledge discovery.
# * The knowledge of the correlation between the items in the data transaction can use association rule mining.
# * Retail store analysis is one of an application area of association rule mining technique.
# * The possible percentage of the correlation of combined items gives the new knowledge. Therefore, it is a very helpful for determiner to take the decisions

# ### Analysis

# In[1]:


# Importing Required Library

import pandas as pd
import numpy as np


# In[2]:


# Reading Excel file 
# need to install 1.2.0 version xlrd package to read excel files: pip install xlrd==1.2.0
import os
os.chdir('D:/hw_data/hw4_arm/hw4-arm-implement')
bread = pd.read_excel('raw_bread.xlsx')


# In[3]:


## Here we have transaction data, which include column, Date,Time,Transaction,Item
## we should remove duplicate transaction, it shows quantity of item in same transaction,
## it is not needed in appriori aglo as we only care about different item in particular transaction
bread


# In[4]:


## dropping Duplicate Transaction
bread = bread.drop_duplicates()


# In[5]:


## we need to split transaction data into Dataframe/tabular structure as follow
new = bread['Date,Time,Transaction,Item'].str.split(',', n = 3, expand = True)


# In[6]:


import warnings
warnings.filterwarnings('ignore')


# In[7]:


## assigning column to data frame "bread"
bread['Date'] = new[0]
bread['Time'] = new[1]
bread['Transaction'] = new[2]
bread['Item'] = new[3]


# In[8]:


# in this dataframe we only need column Trasaction and Item, rest is not needed in association mining rule
bread[['Date', 'Time', 'Transaction', 'Item']].head(10)
                                                    


# In[9]:


# we need to convert cloumn transacton & item into Crosstab or we can say Binary Matrix as follow
transaction = pd.crosstab(index= bread['Transaction'], columns= bread['Item'])
transaction


# In[10]:


## Just writing csv file to check result
## we have one unwanted column named "NONE", we should remove it as follow and proceed further
#tab.to_csv('tab.csv')


# In[11]:


## removing unwanted col "NONE"
transaction = transaction.drop(['NONE'], axis = 1)


# In[12]:


transaction


# ### Creating APRIORI function to generate frequent itesets based on minimum threshold support = 0.02

# In[13]:


def APRIORI(data, min_support = 0.04,  max_length = 4):
    # Collecting Required Library
    import numpy as np
    import pandas as pd
    from itertools import combinations
    
    support = dict()
    L = list(data.columns)
    
    # write your code here !!
    total = len(data)
    the_dict=dict(data.mean(axis=0))
    old_list=[]
    for x in L:
        if(the_dict[x]>0.04):
            support[frozenset({x})]=the_dict[x]
            old_list+=[frozenset({x})]
    new_list=[]
    for i in range(2,max_length+1):
        leng=len(old_list)
        for a in range(leng):
            for b in range(a+1,leng):
                if(len(old_list[a] | old_list[b]) == i):
                    item_set = frozenset(old_list[a] | old_list[b])
                    the_data=data
                    for item in item_set:
                        the_data = the_data[the_data[item]>0]
                    if(len(the_data)/total>0.04):
                        new_list += [item_set]
                        support[item_set] = len(the_data) / total
        old_list=list(new_list)
        new_list =[]
    result = pd.DataFrame(list(support.items()), columns = ["Items", "Support"])
    return result


# In[14]:


## finding frequent itemset with min support = 4%
my_freq_itemset = APRIORI(transaction, 0.04, 3)
my_freq_itemset.sort_values(by = 'Support', ascending = False)


# ### Creating ASSOCIATION_RULE function to generate rules based on minimun threshold confidence.

# In[15]:


def ASSOCIATION_RULE(df, min_confidence_threshold = 0.5):
    import pandas as pd
    from itertools import permutations
    
    support = pd.Series(df.Support.values, index=df.Items).to_dict()
    data = []
    L = df.Items.values
    # write your code here !!
    def build_data(the_a_set,support,the_c_set,min_confidence_threshold = 0.5):
        if(len(the_a_set)<2):
            return []
        data_list=[]
        a_list = list(the_a_set)
        for item in a_list:
            c_set = set(the_c_set)
            a_set = set(the_a_set)
            c_set.add(item)
            a_set.remove(item)
            cof = support[frozenset(a_set | c_set)]/support[frozenset(a_set)]
            if( cof > min_confidence_threshold ):
                data_list += [frozenset(a_set), frozenset(c_set)]
                data_list += [support[frozenset(a_set)], support[frozenset(c_set)], support[frozenset(a_set | c_set)], cof]
                data_list += [data_list[4] / (data_list[2] * data_list[3]), data_list[4] - (data_list[2] * data_list[3]) ] 
                data_list += [(1-data_list[3])/(1-cof)]
                data_list =  [data_list]
                data_list += build_data(frozenset(a_set), support, frozenset(c_set), min_confidence_threshold)
        return data_list
    for item_set in L:
        if(len(item_set)<2):
            continue
        data += build_data(frozenset(item_set),support,frozenset({}),min_confidence_threshold)
    result = pd.DataFrame(data, columns = ["antecedents", "consequents", "antecedent support", "consequent support",
                                        "support", "confidence", "Lift", "Leverage", "Convection"])
    return result


# In[16]:


## Rule with minimun confidence = 50%
my_rule = ASSOCIATION_RULE(my_freq_itemset, 0.5)
my_rule
# the column names in the following table is the same as those generated by mlxtend
# you can refer to http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/ 
# to find the formulas of lift, leverage, convection


# ### Finally sorting results by Lift to get highly associated itemsets.

# In[17]:


my_rule.sort_values(by='Lift', ascending= False).head(10)


# ## Cross Verifying results with  apriori and association rule from mlxtend

# In[18]:


# Loading standard package
from mlxtend.frequent_patterns import apriori, association_rules


# In[19]:


## finding frequent itemset with min support = 4%
frequent_itemset = apriori(df = transaction, min_support= 0.04, use_colnames= True)
frequent_itemset.sort_values(by = 'support', ascending = False)


# ### Createing associate rule such that item brought with conditional probability(Confidence) more than 50% with corresponding item

# In[20]:


## Rule with minimun confidence = 50%
Rules = association_rules(frequent_itemset, min_threshold= 0.5)
Rules


# In[21]:


## Finally sorting results by Lift to get highly associated itemsets.
Rules.sort_values(by='lift', ascending= False).head(10)


# ### Conclusion
#  * Results from developed function(APRIORI, ASSOCIATION_RULE) has matched with builts packages.
#  * it is observed that "Toast" & "Coffee" are highly associated with lift 1.48.
#  * Coffee has been brought most frequently with 47.5% of all the transactions

# In[ ]:





# In[ ]:





# In[ ]:




