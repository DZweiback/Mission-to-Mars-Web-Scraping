{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# # A web application that scapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.\n",
    "# Initial Imports - Import Dependencies\n",
    "import os\n",
    "import pandas as pd\n",
    "import requests\n",
    "import time\n",
    "from bs4 import BeautifulSoup as bs\n",
    "from splinter import Browser\n",
    "from selenium import webdriver"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import splinter and set the cromedriver path\n",
    "executable_path = {'executable_path': 'chromedriver'}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def init_browser():\n",
    "    \"\"\" Connects path to chromedriver \"\"\"\n",
    "    \n",
    "    executable_path = {'executable_path': '/Users/venessayeh/Downloads/chromedriver'}\n",
    "    return Browser(\"chrome\", **executable_path, headless=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape():\n",
    "    \"\"\" Scrapes all websites for Mars data \"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a dictionary to hold all elements\n",
    "mars_info = {}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use requests and BeautifulSoup to scrape Nasa News for latest news\n",
    "url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'\n",
    "response = requests.get(url)\n",
    "soup = bs(response.text, 'html.parser')\n",
    "results = soup.find('div', class_='features')\n",
    "news_title = results.find('div', class_='content_title').text\n",
    "news_p = results.find('div', class_='rollover_description').text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Store scraped data into dictionary\n",
    "mars_info[\"title\"] = news_title\n",
    "mars_info[\"description\"] = news_p"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scrape Nasa for url of latest featured image of Mars\n",
    "JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "browser.visit(JPL_url)\n",
    "JPL_html = browser.html\n",
    "JPL_soup = bs(JPL_html, 'html.parser')\n",
    "featured_image = JPL_soup.find('div', class_='fancybox-image')\n",
    "featured_image_url = 'https:www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19631_ip.jpg'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add results to dictionary\n",
    "mars_info[\"image\"] = featured_image_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Weather"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scrape Mars Weather twitter for latest weather report\n",
    "twitter_url = 'https://twitter.com/marswxreport?lang=en'\n",
    "twitter_response = requests.get(twitter_url)\n",
    "twitter_soup = bs(twitter_response.text, 'html.parser')\n",
    "twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')\n",
    "mars_weather = twitter_result.find('p', class_='js-tweet-text').text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add results to dictionary\n",
    "mars_info[\"weather\"] = mars_weather"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scrape facts about Mars from space-facts.com using Pandas read_html function\n",
    "mars_facts_url = 'https://space-facts.com/mars/'\n",
    "tables = pd.read_html(mars_facts_url)\n",
    "df = tables[0]\n",
    "df.columns = ['Description', 'Value']\n",
    "df.set_index('Description', inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Export scraped table into an json script    \n",
    "mars_facts = df.to_json()\n",
    "mars_facts.replace(\"\\n\",\"\")\n",
    "df.to_json('mars_facts.json')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add results to dictionary\n",
    "mars_info['mars_facts'] = mars_facts"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mars Hemisphere"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Call on chromedriver function to use for splinter\n",
    "browser = init_browser()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Scrape astrogeology.usgs.gov for urls of hemisphere images of Mars\n",
    "hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "browser.visit(hemisphere_url)\n",
    "hemisphere_html = browser.html\n",
    "hemisphere_soup = bs(hemisphere_html, 'html.parser')\n",
    "base_url =\"https://astrogeology.usgs.gov\"\n",
    "image_list = hemisphere_soup.find_all('div', class_='item')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a list to store dictionary of urls and image titles\n",
    "hemisphere_image_urls = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Loop through list of hemispheres and click on each one to find large resolution image\n",
    "for image in image_list:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a dicitonary to store urls and titles\n",
    "hemisphere_dict = {}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find link to large image\n",
    "href = image.find('a', class_='itemLink product-item')\n",
    "link = base_url + href['href']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit the link\n",
    "browser.visit(link)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Wait 1 second \n",
    "time.sleep(1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Parse the html of the new page\n",
    "hemisphere_html2 = browser.html\n",
    "hemisphere_soup2 = bs(hemisphere_html2, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find the title\n",
    "img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Append to dict\n",
    "hemisphere_dict['title'] = img_title"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find image url\n",
    "img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Append to dict\n",
    "hemisphere_dict['url_img'] = img_url"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Append dict to list\n",
    "hemisphere_image_urls.append(hemisphere_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add hemisphere image urls to dictionary\n",
    "mars_info['hemisphere_image_urls'] = hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "return scrape_mars_dict"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
