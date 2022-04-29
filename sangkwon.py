#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


sk_df = pd.read_excel('sk_meta.xlsx')


# In[4]:


poly = list(map(list, np.flip(np.array([x.strip().replace('(','').replace(')','').split(',') for x in sk_df['상권좌표'].iloc[2].split('|')], dtype='float'))))


# In[6]:


import folium
center = [37.279693, 127.047023]
m = folium.Map(location=center, zoom_start=100)
for i in range(len(sk_df)):
    poly = list(map(list, np.flip(np.array([x.strip().replace('(','').replace(')','').split(',') for x in sk_df['상권좌표'].iloc[i].split('|')], dtype='float'))))
    folium.Polygon(locations=poly, fill=True, tooltip='Polygon').add_to(m)


# In[7]:


schools= pd.read_csv('schools.csv', encoding='cp949')


# In[8]:


stu = pd.read_csv('학생수현황.csv', encoding='cp949')


# In[9]:


stu = stu[stu['기준년도']==2020]
stu = stu[['학교명','합계사항(명)']]


# In[10]:


stu.drop_duplicates('학교명',inplace=True)


# In[11]:


condition = schools['교육지원청명'].isin(['경기도수원교육지원청','경기도용인교육지원청'])
element = schools[condition][['학교명','학교급구분','교육지원청명','위도','경도']]


# In[12]:


element = element[element['학교급구분']=='초등학교']


# In[13]:


element.drop_duplicates('학교명',inplace=True)


# In[14]:


element = pd.merge(element, stu, left_on='학교명', right_on='학교명')


# In[16]:


for i in range(len(element)):
    gps = element[['위도','경도']].values.tolist()
    folium.Marker(gps[i], popup=element['학교명'].iloc[i], tooltip=element['합계사항(명)'].iloc[i]).add_to(m)


# In[17]:


kinder = pd.read_csv('유치원현황.csv', encoding='cp949')


# In[19]:


condition_1 = kinder['시군명'].isin(['용인시','수원시'])
kinder = kinder[condition_1][['시설명','WGS84위도','WGS84경도']]


# In[21]:


for i in range(len(kinder)):
    gps = kinder[['WGS84위도','WGS84경도']].values.tolist()
    folium.Marker(gps[i], popup=kinder['시설명'].iloc[i], icon=folium.Icon('red', icon='star')).add_to(m)


# In[22]:


hk = pd.read_csv('체육도장업체현황.csv', encoding='cp949')


# In[24]:


condition_2 = hk['시군명'].isin(['용인시','수원시'])
hk = hk[condition_2][['사업장명','영업상태명','WGS84위도','WGS84경도']]


# In[25]:


hk=hk[hk['영업상태명']=='영업중']


# In[26]:


hk = hk[hk['사업장명'].str.contains('태권도')]


# In[27]:


hk.dropna(inplace=True)


# In[28]:


for i in range(len(hk)):
    gps = hk[['WGS84위도','WGS84경도']].values.tolist()
    folium.Marker(gps[i], popup=hk['사업장명'].iloc[i], icon=folium.Icon('green', icon='star')).add_to(m)


# In[29]:


m


# In[193]:


m.save('map.html')


# In[ ]:




