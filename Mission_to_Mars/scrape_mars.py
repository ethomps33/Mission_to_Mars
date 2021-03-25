#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import os
import pymongo
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


url = 'https://mars.nasa.gov/news/'
html = requests.get(url)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url2)


# In[3]:


soup = BeautifulSoup(html.text, 'html.parser')
print(soup.prettify())


# In[4]:


results = soup.find_all('div', class_='features')


# In[5]:


for result in results:
    
    title = result.find('div', class_='content_title')
    
    try:
       
        news_title = title.text
        news_p = result.a.div.text

        if (news_title or news_p):
            print('\n-----------------\n')
            print('Title:', news_title)
            print('Description:', news_p)
    except AttributeError as e:
        print(e)


# In[6]:


html2 = browser.html
soup = BeautifulSoup(html2, 'html.parser')

feats = soup.find('img', class_='headerimage fade-in')
link = feats['src']
featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{link}'
print(featured_image_url)


# In[7]:


url3 = 'https://space-facts.com/mars/'


# In[8]:


tables = pd.read_html(url3)
tables


# In[9]:


df = tables[0]
df.head()


# In[10]:


url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
html3 = requests.get(url4)


# In[11]:


soup = BeautifulSoup(html3.text, 'html.parser')
print(soup.prettify())


# In[30]:


results2 = soup.find_all('div', class_='item')


# In[37]:


hemisphere_image_url = []
for result in results2:
    
    title = result.find('h3').text
    img_url = result.img['src']
    
    hemisphere_image_url.append({"Title": title, "img_url": img_url})
    
print(hemisphere_image_url)


# In[ ]:





# In[ ]:




