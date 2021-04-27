#!/usr/bin/env python
# coding: utf-8

# In[29]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[18]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[19]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[20]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[21]:


slide_elem.find('div', class_='content_title')


# In[22]:


news_title=slide_elem.find('div', class_='content_title').get_text()
news_title


# In[23]:


news_summary=slide_elem.find('div', class_='article_teaser_body').get_text()
news_summary


# ### Featured Image

# In[24]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[25]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[26]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[27]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[28]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[30]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[31]:


df.to_html()


# In[32]:


browser.quit()

