#!/usr/bin/env python
# coding: utf-8

# In[41]:


# # A web application that scapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.
# Initial Imports - Import Dependencies
import os
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver


# # NASA Mars News

# In[42]:


def init_browser():
    """ Connects path to chromedriver """
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=True)


# In[43]:


def scrape():
    """ Scrapes all websites for Mars data """

    # In[44]:

    # Create a python dictionary to hold all elements
    mars_info = {}


    # In[45]:


    # Use requests and BeautifulSoup to scrape Nasa News for latest news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    results = soup.find('div', class_='features')
    news_title = results.find('div', class_='content_title').text
    news_p = results.find('div', class_='rollover_description').text


    # In[46]:


    # Store scraped data into dictionary
    mars_info["title"] = news_title
    mars_info["description"] = news_p


    # # JPL Mars Space Images - Featured Image

    # In[47]:


    # Call on chromedriver function to use for splinter
    browser = init_browser()


    # In[48]:


    # Scrape Nasa for url of latest featured image of Mars
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)
    JPL_html = browser.html
    JPL_soup = bs(JPL_html, 'lxml')
    featured_image = JPL_soup.find('div', class_='fancybox-image')
    featured_image_url = 'https:www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19631_ip.jpg'


    # In[49]:


    # Add results to dictionary
    mars_info["featured_image_url"] = featured_image_url


    # # Mars Weather

    # In[50]:


    # Scrape Mars Weather twitter for latest weather report
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'lxml')
    twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')
    mars_weather = twitter_result.find('p', class_='js-tweet-text').text


    # In[51]:


    # Add results to dictionary
    mars_info["mars_weather"] = mars_weather


    # # Mars Facts

    # In[52]:


    # Scrape facts about Mars from space-facts.com using Pandas read_html function
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)


    # In[53]:


    # Export scraped table into an json script    
    mars_facts = df.to_json()
    mars_facts.replace("\n","")
    df.to_json('mars_facts.json')


    # In[54]:


    # Add results to dictionary
    mars_info['mars_facts'] = mars_facts


    # # Mars Hemisphere

    # In[55]:


    # Scrape astrogeology.usgs.gov for urls of hemisphere images of Mars
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"
    image_list = hemisphere_soup.find_all('div', class_='item')


    # In[56]:


    # Create a list to store dictionary of urls and image titles
    hemisphere_image_urls = []


    # In[57]:


    # Loop through list of hemispheres and click on each one to find large resolution image
    for image in image_list:
        
        # Create dictionary to store urls and titles
        hemisphere_dict = {}
        
        # Find link to large image and visit the link
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        # Wait one second
        time.sleep(1)
        
        # Parse the html of the new page
        hemisphere_html2 = browser.html
        hemisphere_soup2 = bs(hemisphere_html2, 'lxml')
        
        # Find the title and append to dictionary
        img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
        
        # Find image url and append to dictionary
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
        
        # Append dict to list
        hemisphere_image_urls.append(hemisphere_dict)
        
    # Add hemisphere image urls to dictionary
    mars_info['hemisphere_image_urls'] = hemisphere_image_urls       
        
    return mars_info


    # In[ ]:




