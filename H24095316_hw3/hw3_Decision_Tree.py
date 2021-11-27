#!/usr/bin/env python
# coding: utf-8

# ## HW: Decision Tree with ID3 Algorithm

# ### Introduction
# 
# In this homework, you will implement a simple ``ID3 Decision Tree`` method that we introduce in the lecture.
# 
# Given a dataset, where each row is a mushroom, and each column contains ``features`` (or called ``attributes``) of the mushroom. **The goal is to predict whether the mushroom is poisonous or not (i.e., poisonous or edible) based on features.** Note that the first column is the class of ``poisonous`` or ``edible``.
# 
# The mushroom dataset is taken from UCI data repository. The value of each feature/attribute column (from the second column) is categorical or ordinal. Each feature/attribute value is an abbreviation. You can refer to the detailed description for each feature/attribute value abbreviation from [UCI Mushroom Data Set](https://archive.ics.uci.edu/ml/datasets/mushroom). Below we copy and paste the official description.
# 
# This data set includes descriptions of hypothetical samples corresponding to 23 species of gilled mushrooms in the Agaricus and Lepiota Family (pp. 500-525). Each species is identified as definitely edible, definitely poisonous, or of unknown edibility and not recommended. This latter class was combined with the poisonous one. The Guide clearly states that there is no simple rule for determining the edibility of a mushroom; no rule like "leaflets three, let it be" for Poisonous Oak and Ivy.
# 
# 
# Feature/Attribute Information:
# 
# 1. cap-shape: bell=b,conical=c,convex=x,flat=f, knobbed=k,sunken=s
# 2. cap-surface: fibrous=f,grooves=g,scaly=y,smooth=s
# 3. cap-color: brown=n,buff=b,cinnamon=c,gray=g,green=r, pink=p,purple=u,red=e,white=w,yellow=y
# 4. bruises?: bruises=t,no=f
# 5. odor: almond=a,anise=l,creosote=c,fishy=y,foul=f, musty=m,none=n,pungent=p,spicy=s
# 6. gill-attachment: attached=a,descending=d,free=f,notched=n
# 7. gill-spacing: close=c,crowded=w,distant=d
# 8. gill-size: broad=b,narrow=n
# 9. gill-color: black=k,brown=n,buff=b,chocolate=h,gray=g, green=r,orange=o,pink=p,purple=u,red=e, white=w,yellow=y
# 10. stalk-shape: enlarging=e,tapering=t
# 11. stalk-root: bulbous=b,club=c,cup=u,equal=e, rhizomorphs=z,rooted=r,missing=?
# 12. stalk-surface-above-ring: fibrous=f,scaly=y,silky=k,smooth=s
# 13. stalk-surface-below-ring: fibrous=f,scaly=y,silky=k,smooth=s
# 14. stalk-color-above-ring: brown=n,buff=b,cinnamon=c,gray=g,orange=o, pink=p,red=e,white=w,yellow=y
# 15. stalk-color-below-ring: brown=n,buff=b,cinnamon=c,gray=g,orange=o, pink=p,red=e,white=w,yellow=y
# 16. veil-type: partial=p,universal=u
# 17. veil-color: brown=n,orange=o,white=w,yellow=y
# 18. ring-number: none=n,one=o,two=t
# 19. ring-type: cobwebby=c,evanescent=e,flaring=f,large=l, none=n,pendant=p,sheathing=s,zone=z
# 20. spore-print-color: black=k,brown=n,buff=b,chocolate=h,green=r, orange=o,purple=u,white=w,yellow=y
# 21. population: abundant=a,clustered=c,numerous=n, scattered=s,several=v,solitary=y
# 22. habitat: grasses=g,leaves=l,meadows=m,paths=p, urban=u,waste=w,woods=d
# 

# In[46]:


import pandas as pd
import os
os.chdir("D:\\hw_data\\hw3_decision_tree")
df_shroom = pd.read_csv('mushrooms.csv')
df_shroom


# ### Entropy
# 
# The decision tree algorithm works by looking at all the features, and picking the 'best' one to split the data on, then running recursively on the split data.
# 
# The way we pick the 'best' feature to split on is by picking the feature that decreases 'entropy'.
# 
# What's entropy? Recall that we're trying to classify mushrooms as poisonous or not. Entropy is a value that will be low if a group of mushrooms mostly has the same class (all poisonous or all edible) and high if a group of mushrooms varies in their classes (half poisonous and half edible). So every split of the data that minimizes entropy is a split that does a good job classifying.

# In[47]:


import math
def entropy(probs):
    ### take a list of probabilities and calculate their entropy values
    # your code here
    list_entropy=0
    for prob in probs:
        list_entropy-=prob*(math.log2(prob))
    return list_entropy
    

def entropy_of_list(a_list):
    ### take a list of items with discrete values (e.g., poisonous, edible)
    ### and return the list of entropy values for those items
    
    # your code here
    a_list=list(a_list)
    n=len(a_list)
    probs=[]
    while(len(a_list)>0):
        element=str(a_list[0])
        probs+=[a_list.count(element)/n]
        while(a_list.count(element)!=0):
            a_list.remove(element)
    return entropy(probs)
    
# the initial entropy of the poisonous/edible column for all instances in the dataset
total_entropy = entropy_of_list(df_shroom['class'])
print(total_entropy)


# In order to decide which feature to split on, we want to quantify how each feature decreases the entropy. 
# 
# We do this in a fairly intuitive way: we split our dataset by the possible values of an feature, then do a weighted sum of the entropies for each of these split datasets, weighted by how big that sub-dataset is. 
# 
# We'll create a function that quantifies the decrease in entropy, or conversely, the ``information gain``.

# In[48]:


def information_gain(df, split_feature_name, target_feature_name):
    
    ### take a dataFrame of features, and quantify the entropy of a target feature
    ### after performing a split along the values of another feature
    ### and calculate the corresponding information gain

    # your code here
    feature_list=list(set(df[split_feature_name]))
    info_gain=entropy_of_list(list(df[target_feature_name]))
    n=len(df)
    for feature in feature_list:
        prob_list=list(df[target_feature_name][df[split_feature_name]==feature])
        info_gain-=entropy_of_list(prob_list)*len(prob_list)/n
    return info_gain

print('\nExample: information gain for the best feature is ' + str(information_gain(df_shroom, 'odor', 'class')))


# ### ID3 Decision Tree Algorithm
# 
# Now you will write the decision tree algorithm itself, called ``ID3``.
# 
# HINT: you can utilize ``nested dictionary`` to implement the tree.

# In[49]:


def id3(df, target_feature_name, feature_names, default_class = None):
    
    ## counting for the target feature
    from collections import Counter
    cnt = Counter(x for x in df[target_feature_name])
    
    ## First check: do instances in this split of the dataset belong to the same class?
    # (i.e., all mushrooms in this set are poisonous)
    # if yes, return that homogenous label (e.g., 'poisonous')
    if len(cnt) == 1:
        return list(cnt.keys())[0]
    
    ## Second check: is this split of the dataset empty?
    # if yes, return a default value
    elif df.empty or (not feature_names):
        return default_class 
    
    ## Otherwise: this dataset is ready to be split!
    else:
        ### step 1: get the default value for next recursive call of this function
        index_of_max = list(cnt.values()).index(max(cnt.values())) 
        default_class = list(cnt.keys())[index_of_max] # most common value of target feature in dataset
        
        ### step 2: choose the best feature to split on
        
        # your code here
        feature_value=dict()
        for feature in feature_names:
            feature_value[feature]=information_gain(df, feature, target_feature_name)
        feature_value=Counter(feature_value)
        best_index=list(feature_value.values()).index(max(feature_value.values())) 
        best_feature=list(feature_value.keys())[best_index]
        
        ### step 3: create an empty tree, to be populated in a moment
        
        # your code here
        tree={best_feature:dict()}
    
    
        ### Step 4: split dataset
        # on each split, recursively call this "id3" function
        # populate the empty tree with subtrees, which
        # are the result of the recursive call
        
        # your code here
        feature_names.remove(best_feature)
        for feature in list(set(df[best_feature])):
            tree[best_feature][feature]=id3(df[df[best_feature]==feature], target_feature_name, feature_names)
        
        return tree


# In[50]:


# get feature names (all but 'class' column)
feature_names = list(df_shroom.columns)
feature_names.remove('class')


# In[51]:


# visualize the constructed decision tree using pprint package
from pprint import pprint
# use all instances (df_shroom) to build the decision (suppose all instances are for training)
tree = id3(df_shroom, 'class', feature_names)
pprint(tree)


# ### Classification Accuracy: Entire Datast as Training Data and Testing Data
# 
# Let's make sure the resulting tree accurately predicts the class, based on the features.
# 
# Below is a ``classify`` algorithm that takes an instance and classifies it based on the decision tree.

# In[52]:


def classify(instance, tree, default = None):
    feature = list(tree.keys())[0]
    if instance[feature] in list(tree[feature].keys()):
        result = tree[feature][instance[feature]]
        if isinstance(result, dict): # this is a tree, delve deeper
            return classify(instance, result)
        else:
            return result # this is a label
    else:
        return default


# In[53]:


df_shroom['predicted'] = df_shroom.apply(classify, axis=1, args=(tree,'poisonous')) 
    # classify func allows for a default arg: when tree does not have a prediction result for a particular
    # combitation of feature-values, we can use 'poisonous' as the default prediction (better safe than sorry!)

print('Accuracy on all instances is ' + str(sum(df_shroom['class'] == df_shroom['predicted']) / (1.0*len(df_shroom.index))))

df_shroom[['class', 'predicted']]


# ### Classification Accuracy: Split the Dataset into Training and Testing Sets
# 
# A better evaluation the classification algorithm is to train it on a subset of the data (i.e., training data), then test it on a different subset (i.e., test data), where two subsets are disjoint.

# In[54]:


training_data = df_shroom.iloc[1:-3000].copy() # all but last 3 thousand instances
test_data  = df_shroom.iloc[-3000:].copy() # just the last 3 thousand
train_tree = id3(training_data, 'class', feature_names)

test_data['predicted2'] = test_data.apply(                               # <---- test_data source
                                          classify, 
                                          axis=1, 
                                          args=(train_tree,'poisonous')) # <---- train_data tree

print('Accuracy on the test data is ' + str(sum(test_data['class']==test_data['predicted2'] ) / (1.0*len(test_data.index))))


# In[ ]:




