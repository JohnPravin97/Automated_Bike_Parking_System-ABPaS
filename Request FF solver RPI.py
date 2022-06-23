#!/usr/bin/env python
# coding: utf-8

# In[144]:


import requests
import json
import os


# In[145]:


domainfile = r"C:\Users\johnp\Desktop\John - Studies\University of Stuttgart - New\Smart Cities and Internet of Things\PDDL Planning\John Project\domain.pddl"


# In[152]:


start=1
pir = 0


# In[153]:


out_lis = ["Is_Start s_val", "Is_Pir_Motion p_val", "Is_HighTemp t_val", "Is_No_HighTemp t_val"]
i=0
temp = 4

problem_file = """(define (problem STOP_Action) (:domain ABPaS_domain)
(:objects 
    l_val r_val u_val s_val bcv st_val t_val buzz_val exh_Val p_val d_val b_val
)
"""

problem_file += """(:init
"""
if start == 1:
    problem_file += "(" + out_lis[0] + ")" +"\n"
    
if temp >=35:
    problem_file += "(" + out_lis[2] + ")" +"\n"

else:
    problem_file += "(" + out_lis[3] + ")" +"\n"

if pir==1:
     problem_file += "(" + out_lis[1] + ")" +"\n"
        

problem_file += """ )
(:goal (or 
(and (Emermove_stop bcv) (Exhaust_Fan exh_Val))
(Door_Motor d_val)
(Parking_Led_Glow p_val)
)

))"""


# In[154]:


problem_file


# In[155]:


filename = "ABPaS_problem"

with open(filename, "w") as f:
    f.write(problem_file)

data = {'domain': open(domainfile, 'r').read(), 'problem': open(filename, 'r').read()}
response = requests.post('http://solver.planning.domains/solve', json=data).json()


# In[156]:


response


# In[157]:


response['result']['plan']


# In[158]:


for a in response['result']['plan']:
    print(a['name'])


# In[159]:


actresult = []
for act in response['result']['plan']:
    step = act['name']
    actuations = step[1:len(step)-1].split(' ')
    actresult.append(actuations)


# In[160]:


actresult


# In[ ]:




