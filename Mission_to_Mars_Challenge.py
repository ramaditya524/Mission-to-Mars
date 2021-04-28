#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


news_title=slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


news_summary=slide_elem.find('div', class_='article_teaser_body').get_text()
news_summary


# ### Featured Image

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[15]:


#browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[17]:


html = browser.html
img_soup = soup(html, 'html.parser')


# In[18]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for desc in img_soup.find_all('div',class_='description'):
    #create empty dictionary in each loop
    info = {}
    #retreive url of for image
    url = desc.find('a').get('href')
    #splinter command to move to image page
    browser.visit(f'https://marshemispheres.com/{url}')
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #find div tag that contains the full-sized image
    image = img_soup.find('div',class_='downloads') 
    #add image url to dictionary
    info['img_url']= "https://marshemispheres.com/"+image.find('a').get('href')
    #find and add title to dictionary
    info['title']=img_soup.find('h2',class_='title').get_text()
    #append dictionaries to list
    hemisphere_image_urls.append(info)
    #code to send browser back to home page
    browser.back()


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[20]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




