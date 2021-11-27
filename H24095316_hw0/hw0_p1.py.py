#!/usr/bin/env python
# coding: utf-8

# In[1]:


#把輸入字串轉換成幾個多項式的字串如:'(-3x^2y+5xy-7)(3x^2y+5z)'變成['-3x^2y+5xy-7','3x^2y+5z']
u=input("Input the polynomial:")
u=u.split(")(")
if(u[0].startswith("(")):
    thelist=list(u[0])
    thelist.remove("(")
    u[0]="".join(thelist)
if(u[len(u)-1].endswith(")")):
    thelist=list(u[len(u)-1])
    thelist.remove(")")
    u[len(u)-1]="".join(thelist)


# In[2]:


#把多項式的字串轉換成由每一項組成的串列如:'-3x^2y+5xy-7'變成['-3x^2y','+5xy','-7']
for x in range(len(u)):
    list1=list(u[x])
    the_term=""
    list2=[]
    for y in range(len(list1)):
        if(y==0 and list1[0]=="-"):
            the_term="-"
        elif(list1[y]=="-" or list1[y]=="+"):
            list2+=[the_term]
            the_term=list1[y]
        else:
            the_term+=list1[y]
    list2+=[the_term]
    u[x]=list2


# In[3]:


#把串列中的每一項轉換成方便運算的格式...如'3x^2y'變成[3,{'x':2,'y':1}]
expression=False
for x in range(len(u)):
    for y in range(len(u[x])):
        the_term=list(u[x][y])
        determine=True
        number=""
        power=""
        variable=""
        the_processed_term=[]
        for z in the_term:
            if(z=="+" or z=="-" or z.isdigit()):
                number+=z
            elif(determine):
                if(number=="+" or number=="-" or number==""):
                    number+="1"
                the_processed_term=[int(number)]
                number=""
                variable=z
                power=dict()
                determine=False
            else:
                if(z=="^"):
                    expression=True
                    continue
                elif(power!=""):
                    if(number==""):
                        number+="1"
                    power[variable]=int(number)
                    number=""
                else:
                    power=dict()
                variable=z
        if(power==""):
            u[x][y]=[int(number),dict()]
            continue
        elif(number==""):
            number+="1"
        power[variable]=int(number)
        the_processed_term+=[power]
        u[x][y]=the_processed_term


# In[4]:


#定義多項式的加法和乘法
def clearNone(the_list):
    while(the_list.count(None)!=0):
        the_list.remove(None)
    return the_list
def addterm(term1,term2):
    return [term1[0]+term2[0],term1[1]]
def multiplyterm(term1,term2):
    a_term1=dict()
    for variable in list(term1[1]):
        a_term1[variable]=term1[1][variable]+term2[1].get(variable,0)
    for variable in list(term2[1]):
        if(a_term1.get(variable,"does not exsit")=="does not exsit"):
            a_term1[variable]=term2[1][variable]
    return[term1[0]*term2[0],a_term1]
def addpolnomial(polynomial):
    for x in range(len(polynomial)):
        for y in range(x+1,len(polynomial)):
            if(polynomial[x][1]==polynomial[y][1]):
                polynomial[y]=addterm(polynomial[y],polynomial[x])
                polynomial[x]=None
                break
    polynomial=clearNone(polynomial)
    for x in range(len(polynomial)):
        if(polynomial[x][0]==0):
            polynomial[x]=None
    polynomial=clearNone(polynomial)
    return polynomial
def multiplypolnomial(polynomial1,polynomial2):
    polynomial=[]
    for term1 in polynomial1:
        for term2 in polynomial2:
            polynomial+=[multiplyterm(term1,term2)]
    polynomial=addpolnomial(polynomial)
    return polynomial


# In[5]:


#進行多項式的乘法
while(len(u)>1):
    u[1]=multiplypolnomial(u[0],u[1])
    u[0]=None
    u=clearNone(u)


# In[6]:


#進行排列並顯示
def arrange(term):
    number=0
    for variable in list(term[1]):
        number+=term[1][variable]
    return number
the_poly=u[0]
if(len(the_poly)==0):
    the_poly=[[0,dict()]]
the_poly=sorted(the_poly, key=arrange,reverse=True)
print(the_poly[0][0],end="")
for variable in list(the_poly[0][1]):
    print(variable,end="")
    if(expression and the_poly[0][1][variable]!=1):
            print("^",end="")
    if(the_poly[0][1][variable]!=1):
        print(the_poly[0][1][variable],end="")
del the_poly[0]
for term in the_poly:
    if(term[0]>0):
        print("+",end="")
    if(term[0]==-1):
        print("-",end="")
    elif(term[0]!=1):
        print(term[0],end="")
    for variable in list(term[1]):
        print(variable,end="")
        if(expression and term[1][variable]!=1):
            print("^",end="")
        if(term[1][variable]!=1):
            print(term[1][variable],end="")


# In[ ]:




