# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemisphere_data":{}
    }
    data['hemisphere_data']=mars_hemisphere(browser)
    # top webdriver and return data
    browser.quit()
    return data



def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        news_title=slide_elem.find('div', class_='content_title').get_text()
        #news_title
        news_summary=slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_summary
    except AttributeError:
        return None, None

    return news_title,news_summary

# ### Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url
    return img_url

def mars_facts():
    try:

        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html()

def mars_hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
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
    # 4. Print the list that holds the dictionary of each image url and title.
    return  hemisphere_image_urls

#browser.quit()
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
