# <splinter.driver.webdriver.chrome.WebDriver object at 0x10fc83cf8>
# error msg in terminal


# import dependencies
import os
from bs4 import BeautifulSoup
import requests
import time
from splinter import Browser
import pandas as pd



# load browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# scrape mars news
def mars_scrape():
    browser = init_browser()
    global_mars = {}
        
    news_url = 'http://mars.nasa.gov/news'
    browser.visit(news_url)
    time.sleep(5)

    news_html = browser.html 
    news_soup = BeautifulSoup(news_html, 'html.parser')

    articles = news_soup.find('ul', class_='item_list')
    first_item = articles.find('li', class_='slide')
    news_title = first_item.find("div", class_="content_title").text
    news_p = first_item.find("div", class_="article_teaser_body").text

    # create entry into global dictionary
    global_mars["news_title"] = news_title
    global_mars["news_paragraph"] = news_p


    # scrape mars images

    # images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(images_url)

    # images_html = browser.html 
    # images_soup = BeautifulSoup(images_html, 'html.parser')
    # # try:

    # image_url = images_soup.find('figure', class_='lede')
    # image_link = image_url.find("a")["href"]
    # featured_image_url = 'https://www.jpl.nasa.gov' + image_link

    # # create entry into global dictionary
    # global_mars["featured_image_url"] = featured_image_url

    # ##############################
    # elem = browser.find_by_id("full_image")
    # elem.click()

    # browser.is_element_not_present_by_text("more info")
    # more_elem = browser.find_link_by_partial_text("more info")
    # more_elem.click()

    # img_html = browser.html 
    # img_soup = BeautifulSoup(img_html, 'html.parser')
    # ##############################


    # scrape mars tweets

    tweets_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweets_url)
    time.sleep(1)

    tweets_html = browser.html 
    tweets_soup = BeautifulSoup(tweets_html, 'html.parser')

    tweets_list = tweets_soup.find('div', class_='js-tweet-text-container')
    mars_weather = tweets_list.find('p').text

    # create entry into global dictionary
    global_mars["mars_weather"] = mars_weather



    # scrape mars facts

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(1)

    marsfacts = pd.read_html('https://space-facts.com/mars/')
    marsfacts_df = marsfacts[1]
    marsfacts_df.columns=["Description", "Value"]
    marsfacts_df.set_index("Description", inplace=True)
    marsfacts_df
        
    marstable = marsfacts_df.to_html()
    marstable

    # create entry into global dictionary
    global_mars["marsfacts"] = marstable


    # scrape mars hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(1)

    hemi_html = browser.html 
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')

    hemisphere_list = []

    hemiresults = hemi_soup.find("div", class_="result-list")
    hemi = hemiresults.find_all("div", class_="item")

    hemi_mainurl = 'https://astrogeology.usgs.gov/'

    for x in hemi:
        title = x.find("h3").text
    
        image_url = x.find("a")["href"]
    
        image_fullurl = hemi_mainurl + image_url
    
        browser.visit(image_fullurl)
    
        hi_html = browser.html
        hi_soup = BeautifulSoup(hi_html, 'html.parser')
    
        other_url = hi_soup.find("div", class_="downloads")
        new_imageurl = other_url.find("a")["href"]

        hemisphere_list.append({"title" : title, "img_url" : new_imageurl})

    # create entry into global dictionary
    global_mars["hemisphere_list"] = hemisphere_list

    browser.quit()

    return global_mars