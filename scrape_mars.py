#!/usr/bin/env python
# Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import time
import pandas as pd
import requests
from selenium import webdriver 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_scrape_data = {}

def scrape():

    try:

        # Initialize browser
        browser = init_browser()

        # Navigate to NASA Mars News site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())

        # Collect the latest News Title and Paragraph Text
        news_title = soup.find('div', class_='content_title').text
        print(news_title)
        news_p = soup.find('div', class_= 'article_teaser_body').text
        print(news_p)

        # Visit the url for JPL Featured Space Image 
        url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url_jpl)

        # Scrape page into Soup
        html_jpl = browser.html
        soup_jpl = BeautifulSoup(html_jpl, 'html.parser')

        # Auto Click FULL IMAGE link
        browser.click_link_by_partial_text('FULL IMAGE')
        # Add 5 second delay for the page to fully load
        time.sleep(5)

        # Auto Click 'more info' link
        browser.click_link_by_partial_text('more info')
        # Add 5 second delay for the page to fully load
        time.sleep(5)


        # Scrape page into Soup
        html_jpl_detail = browser.html
        soup_jpl_detail = BeautifulSoup(html_jpl_detail, 'html.parser')

        # Find the full image link
        href_img = soup_jpl_detail.find('img', class_='main_image')
        href_img_path = href_img.get('src')
        featured_image_url = "https://www.jpl.nasa.gov" + href_img_path
        print(featured_image_url)


        # Mars Weather 
        # Navigate to Mars Twitter site
        url_marstwitter = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url_marstwitter)

        # Scrape the page into Soup
        html_marstwitter = browser.html
        soup_marstwitter = BeautifulSoup(html_marstwitter, 'html.parser')

        # Find and save the latest weather tweet
        weather_tweets = soup_marstwitter.find_all('div', class_="js-tweet-text-container")
        for tweet in weather_tweets:
            mars_weather = tweet.find('p').text
            if 'Sol' in mars_weather:
                print(mars_weather)
                break
            else:
                pass

        # Mars Facts 
        # Visit the Mars Facts webpage
        url_marsfacts = 'https://space-facts.com/mars/'

        # Use pandas to read html and save data as dataframe
        planet_facts = pd.read_html(url_marsfacts)
        planet_facts_df = planet_facts[0]
        planet_facts_df.columns = ['description', 'value']
        planet_facts_df.set_index('description', inplace=True)
        planet_facts_df

        # Use Pandas to convert the data to an HTML table string
        planet_facts_html = planet_facts_df.to_html()
        planet_facts_html = planet_facts_html.replace('\n', '')
        planet_facts_html

        # Transform df to a dictionary format
        planet_facts_html_dict ={'planet_facts':planet_facts_html}
        planet_facts_html_dict

        # Mars Hemispheres
        # Visit the USGS Astrogeology site
        url_usgs_mars = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url_usgs_mars)

        # Scrape page into Soup
        html_usgs_mars = browser.html
        soup_usgs_mars = BeautifulSoup(html_usgs_mars, 'html.parser')

        # Get all Mars Hemisphere image attributes
        mars_all_items = soup_usgs_mars.find_all('div', class_='item')
        url_usgs = 'https://astrogeology.usgs.gov'

        # Create a list that holds Mars Hemisphere URL
        hemisphere_img_urls = []

        # Loop into the list 
        for item in mars_all_items:
            # Get the title of the hemisphere image
            title = item.find('h3').text
            
            # Get the path of hemisphere image
            path_img_url = item.find('a',class_='itemLink product-item')['href']
            
            #Browse the USGSS Astrogeology with the image url
            browser.visit(url_usgs + path_img_url)
            
            # Scrape the page into Soup
            path_img_html = browser.html
            soup_img_html = BeautifulSoup(path_img_html, 'html.parser')
            
            # Get the Mars Hemisphere full image url
            img_tag = soup_img_html.find('div', class_ = 'downloads')
            img_url = img_tag.find('a')['href']
            
            #Append the dictionary with the image url string and the hemisphere title to a list
            hemisphere_img_urls.append({'title': title, 'img_url': img_url})
        
        # Display the Marsh Hemisphere image url list
        print(hemisphere_img_urls)
        
        # Gather all the list 
        mars_scrape_data['news_title'] = news_title
        mars_scrape_data['news_p'] = news_p
        mars_scrape_data['featured_image_url'] = featured_image_url
        mars_scrape_data['latest_weather'] = mars_weather
        mars_scrape_data['facts'] = planet_facts_html
        mars_scrape_data['hemisphere_image_urls'] = hemisphere_img_urls

        return mars_scrape_data

    finally:
        # Close the browser after scraping
        browser.quit()