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


# In[ ]:


url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
html = requests.get(url)
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)


# In[ ]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[ ]:


db = client.mission_to_mars_db
collection = db.scrape


# In[ ]:


news_soup = BeautifulSoup(html.text, 'html.parser')
print(news_soup.prettify())


# In[ ]:


news_title = news_soup.find_all('div', class_='content_title')[0].text
news_p = news_soup.find_all('div', class_='rollover_description_inner')[0].text


# In[ ]:


print('\n-----------------\n')
print('Title:', news_title)
print('Description:', news_p)
article = {
    'Title': news_title,
    'Description': news_p,}


# In[ ]:


jpl_nasa_url = 'https://www.jpl.nasa.gov'
images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(images_url)
html = browser.html
images_soup = BeautifulSoup(html, 'html.parser')
relative_image_path = images_soup.find_all('img')[3]["src"]
featured_image_url = jpl_nasa_url + relative_image_path


# In[ ]:


# weather_url = 'https://twitter.com/marswxreport?lang=en'
# browser.visit(weather_url)
# weather_html = browser.html
# weather_soup = BeautifulSoup(weather_html, 'html.parser')
# print(weather_soup.prettify())


# In[ ]:


# mars_weather = weather_soup.find_all('p', class_='')[0].text


# In[ ]:


facts_url = 'https://space-facts.com/mars/'


# In[ ]:


import json

tables = pd.read_html(facts_url)
mars_facts_df = tables[2]
mars_facts_df.columns = ["Description", "Value"]
mars_html_table = mars_facts_df.to_html()
mars_html_table.replace('\n', '')

print(mars_facts_df)


# In[ ]:


# df = tables[0]
# df = df.to_json()

# json.dumps(df)
# # collection.insert_one(df)


# In[ ]:


usgs_url = 'https://astrogeology.usgs.gov'
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)
hemispheres_html = browser.html
hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')


# In[ ]:


all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
hemisphere_image_urls = []


# In[ ]:


# results2 = soup.find_all('div', class_='item')


# In[ ]:


for i in mars_hemispheres:
    
    # Collect Title
    hemisphere = i.find('div', class_="description")
    title = hemisphere.h3.text        
    # Collect image link by browsing to hemisphere page
    hemisphere_link = hemisphere.a["href"]    
    browser.visit(usgs_url + hemisphere_link)        
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')        
    image_link = image_soup.find('div', class_='downloads')
    image_url = image_link.find('li').a['href']
    # Create Dictionary to store title and url info
    image_dict = {}
    image_dict['title'] = title
    image_dict['img_url'] = image_url        
    hemisphere_image_urls.append(image_dict)


# In[ ]:


mars_dict = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "mars_weather": "",
    "fact_table": str(mars_html_table),
    "hemisphere_images": hemisphere_image_urls
}


# In[ ]:


mars_dict


# In[ ]:


browser.quit()


# In[ ]:


get_ipython().system(' jupyter nbconvert --to script mission_to_mars.ipynb')

