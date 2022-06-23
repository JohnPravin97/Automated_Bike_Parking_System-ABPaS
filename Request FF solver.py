#!/usr/bin/env python
# coding: utf-8

# In[402]:


import requests
import json
import os


# In[403]:


domainfile = r"C:\Users\johnp\Desktop\John - Studies\University of Stuttgart - New\Smart Cities and Internet of Things\PDDL Planning\John Project\domain.pddl"


# In[404]:


json_file = r"C:\Users\johnp\Desktop\John - Studies\University of Stuttgart - New\Smart Cities and Internet of Things\RPi Sub Code\BCV1_Json_Data"


# In[405]:


with open(json_file, 'r') as outfile:
    json_lis = outfile.readlines()


# In[406]:


del json_lis[0]


# In[407]:


dic_json = []
for i in json_lis:
    if json.loads(i)["BCV1_ESP8266"]["IR3_status"] == 1 and json.loads(i)["BCV1_ESP8266"]["IR2_status"] == 1:
        dic_json.append(json.loads(i))


# In[408]:


dic_json


# In[409]:


"""
dic_json = []
for i in json_lis:
    dic_json.append(json.loads(i))"""


# In[410]:


start=1


# In[411]:


out_lis = ["Is_Start s_val", "Is_Stop st_val", "Is_Right_IR r_val", "Is_Left_IR l_val", "Is_Both_IR b_val", "Is_Ultrasonic u_val", "Is_No_Ultrasonic u_val", "Is_HighTemp t_val", "Is_No_HighTemp t_val"]
i=0
temp = 4

problem_file = """(define (problem STOP_Action) (:domain ABPaS_domain)
(:objects 
    l_val r_val u_val s_val bcv st_val t_val buzz_val exh_Val pir_val d_val b_val
)
"""

problem_file += """(:init
"""
if start == 1:
    problem_file += "(" + out_lis[0] + ")" +"\n"

if (dic_json[1]["BCV1_ESP8266"]["Ultrasonic_D_CM"])<=10:
    problem_file += "(" + out_lis[6] + ")" +"\n"

elif (dic_json[1]["BCV1_ESP8266"]["Ultrasonic_D_CM"])>10:
    problem_file += "(" + out_lis[5] + ")" +"\n"

if temp >=35:
    problem_file += "(" + out_lis[7] + ")" +"\n"

else:
    problem_file += "(" + out_lis[8] + ")" +"\n"

if (dic_json[1]["BCV1_ESP8266"]["IR2_status"] == 1):
    if (dic_json[1]["BCV1_ESP8266"]["IR3_status"] == 1):
        problem_file += "(" + out_lis[4] + ")" +"\n"
    else:
        problem_file += "(" + out_lis[2] + ")" +"\n"
        
else:
    if (dic_json[1]["BCV1_ESP8266"]["IR3_status"] == 0):
        problem_file += "(" + out_lis[1] + ")" +"\n"
    else:
        problem_file += "(" + out_lis[3] + ")" +"\n" 


problem_file += """ )
(:goal (or 
(Emermove_stop bcv)
(Exhaust_Fan exh_Val)
(Move_Forward bcv)
(Move_Stop bcv)
(Move_Left bcv) 
(Move_Right bcv) 
(Parking_Led_Glow pir_val)
)

))"""


# In[412]:


problem_file


# In[396]:


filename = "ABPaS_problem"

with open(filename, "w") as f:
    f.write(problem_file)

data = {'domain': open(domainfile, 'r').read(), 'problem': open(filename, 'r').read()}
response = requests.post('http://solver.planning.domains/solve', json=data).json()


# In[397]:


response


# In[398]:


response['result']['plan']


# In[399]:


for a in response['result']['plan']:
    print(a['name'])


# In[400]:


actresult = []
for act in response['result']['plan']:
    step = act['name']
    actuations = step[1:len(step)-1].split(' ')
    actresult.append(actuations)


# In[401]:


actresult


# In[ ]:




