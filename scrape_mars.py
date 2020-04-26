#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import re
import lxml

def scrape():
    
    mars_dict = {}

    # URL of webpage to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', headless=False)

    # URL of webpage to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(10)

    
    html = browser.html
    soup = bs(html, 'html.parser')

    news_div = soup.find_all('div', class_='content_title')[1]
    news_title = news_div.find('a').text

    mars_dict['news_title'] = news_title


    paragraph_div = soup.find_all('div', class_='article_teaser_body')[0]
    news_paragraph = paragraph_div.text

    mars_dict['news_paragraph'] = news_paragraph


    # URL of webpage to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)


    html = browser.html
    soup = bs(html, 'html.parser')

    photo_anchor_tag = soup.find('a', id='full_image')

    featured_image_url =  photo_anchor_tag.get('data-fancybox-href')
    featured_image_url = 'https://jpl.nasa.gov' + featured_image_url

    mars_dict['featured_image_url'] = featured_image_url


    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather_span = soup('span', text=re.compile('InSight sol .*'))[0]
    mars_weather = mars_weather_span.text

    mars_dict['mars_weather'] = mars_weather


    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')
    mars_facts_table = soup('table', id='tablepress-p-mars-no-2')[0]

    mars_dict['mars_facts_table'] = mars_facts_table


    mars_facts_dfs = pd.read_html('https://space-facts.com/mars/')
    mars_facts_df = mars_facts_dfs[0]

    mars_dict['mars_facts_df'] = mars_facts_df

    mars_facts_df.set_index(0)


    # Navigate to initial page
    # (Sleep time to allow page to fully load)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(3)

    # Find all the text links
    html = browser.html
    soup = bs(html, 'html.parser')
    link_divs = soup.find_all('div', class_='description')

    # Loop over text links to populate array of dicts.
    hemisphere_image_urls = []

    for item in link_divs:
        link_dict = {}  #Creates new dict
        link_dict['title'] = item.a.text #Sets anchor tag text into 'title'
        # Code below visits link to get full image URL
        browser.visit('https://astrogeology.usgs.gov' + item.a['href']) 
        time.sleep(3)
        loop_html = browser.html # Gets html from new page
        loop_soup = bs(loop_html, 'html.parser') # Sets up soup
        image = loop_soup.find_all('img', class_='wide-image')[0] # Uses soup to find all images with class of 'wide-image'
        link_dict['img_url'] = 'https://astrogeology.usgs.gov/' + image['src'] # Sets image's url into the dict
        hemisphere_image_urls.append(link_dict) # Appends to dict

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict




