import json
import time
from multiprocessing import Pool

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

RULES_SEARCH_PAGE = {
    'url': {'tag': 'a', 'get': 'href'},
    'name': {'tag': 'span', 'class': 't16jmdcf'},
    'header': {'tag': 'div', 'class': '_b14dlit'},
    'rating': {'tag': 'span', 'class':'r1g2zmv6'},
    'reviews': {'tag': 'span', 'class': 'rapc1b3'},
    'price': {'tag': 'span', 'class': '_tyxjp1'},
    'bedroms': {'tag': 'span', 'class': 'mvk3iwl', 'order': 1}
}

def extract_listings_dynamic(page_url, attempts=10):
    """Extracts all listings from a given page"""
    listings_max = 0
    listings_out = [BeautifulSoup('', features='html.parser')]
    for idx in range(attempts):
        try:
            """ Headless server configuration for chrome browser
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome('/home/edgar/Downloads/chromedriver', chrome_options=chrome_options,  service_args=['--verbose']) #change the path to your chromedriver destination
            """
            
            driver = webdriver.Chrome() # Comment this out for headless server configuration
            driver.get(page_url)
            page_detailed = driver.page_source
            driver.quit()
            detailed_soup = BeautifulSoup(page_detailed)
            listings = detailed_soup.findAll('div', 'c1o3pz3i')
        except Exception as e:
            print(e)
            listings = [BeautifulSoup('', features='html.parser')]
        
        if len(listings) == 20:
            listings_out = listings
            break
        
        if len(listings) >= listings_max:
            listings_max = len(listings)
            listings_out = listings

    return listings_out

def extract_element_data(soup, params):
    """Extracts data from a specified HTML element"""
    
    # 1. Find the right tag
    if 'class' in params:
        elements_found = soup.find_all(params['tag'], params['class'])
    else:
        elements_found = soup.find_all(params['tag'])
        
    # 2. Extract text from these tags
    if 'get' in params:
        element_texts = [el.get(params['get']) for el in elements_found]
    else:
        element_texts = [el.get_text() for el in elements_found]
        
    # 3. Select a particular text or concatenate all of them
    tag_order = params.get('order', 0)
    if tag_order == -1:
        output = '**__**'.join(element_texts)
    else:
        output = element_texts[tag_order]
    
    return output

def extract_listing_features(soup, rules):
    """Extracts all features from the listing"""
    features_dict = {}
    for feature in rules:
        try:
            features_dict[feature] = extract_element_data(soup, rules[feature])
        except:
            features_dict[feature] = 'empty'
    
    return features_dict

def extract_soup_js(listing_url, waiting_time=[20, 1]):
    """Extracts HTML from JS pages: open, wait, click, wait, extract"""

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=options)

    # if the URL is not valid - return an empty soup
    try:
        driver.get(listing_url)
    except:
        print(f"Wrong URL: {listing_url}")
        return BeautifulSoup('', features='html.parser')
    
    # waiting for an element on the bottom of the page to load ("More places to stay")
    try:
        myElem = WebDriverWait(driver, waiting_time[0]).until(EC.presence_of_element_located((By.CLASS_NAME, '_4971jm')))
    except:
        pass

    # click cookie policy
    try:
        driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/section/footer/div[2]/button").click()
    except:
        pass
    # alternative click cookie policy
    try:
        element = driver.find_element_by_xpath("//*[@data-testid='main-cookies-banner-container']")
        element.find_element_by_xpath("//button[@data-testid='accept-btn']").click()
    except:
        pass

    # looking for price details
    price_dropdown = 0
    try:
        element = driver.find_element_by_class_name('_gby1jkw')
        price_dropdown = 1
    except:
        pass

    # if the element is present - click on it
    if price_dropdown == 1:
        for i in range(10): # 10 attempts to scroll to the price button
            try:
                actions = ActionChains(driver)
                driver.execute_script("arguments[0].scrollIntoView(true);", element);
                actions.move_to_element_with_offset(element, 5, 5)
                actions.click().perform()
                break
            except:
                pass
        
    # looking for amenities
    driver.execute_script("window.scrollTo(0, 0);")
    try:
        driver.find_element_by_class_name('_13e0raay').click()
    except:
        pass # amenities button not found

    time.sleep(waiting_time[1])

    detail_page = driver.page_source

    driver.quit()

    return BeautifulSoup(detail_page, features='html.parser')

def extract_amenities(soup):
    amenities = soup.find_all('div', {'class': '_aujnou'})
    
    amenities_dict = {}
    for amenity in amenities:
        header = amenity.find('div', {'class': '_1crk6cd'}).get_text()
        values = amenity.find_all('div', {'class': '_1dotkqq'})
        values = [v.find(text=True) for v in values]
        
        amenities_dict['amenity_' + header] = values
        
    return json.dumps(amenities_dict)

class Parser:
    def __init__(self, link, out_file):
        self.link = link
        self.out_file = out_file
    
    def build_urls(self, listings_per_page=20, pages_per_location=15):
        """Builds links for all search pages for a given location"""
        url_list = []
        for i in range(pages_per_location):
            offset = listings_per_page * i
            url_pagination = self.link + f'&items_offset={offset}'
            url_list.append(url_pagination)
            self.url_list = url_list

    def process_search_pages(self):
        """Extract features from all search pages"""
        features_list = []
        for page in self.url_list:
            listings = extract_listings_dynamic(page)
            for listing in listings:
                features = extract_listing_features(listing, RULES_SEARCH_PAGE)
                features['sp_url'] = page
                features_list.append(features)

        self.base_features_list = features_list

    def save(self, feature_set='all'):
        if feature_set == 'basic':
            pd.DataFrame(self.base_features_list).to_csv(self.out_file, index=False)
        elif feature_set == 'all':
            pd.DataFrame(self.all_features_list).to_csv(self.out_file, index=False)
        else:
            pass
            
        
    def parse(self):
        self.build_urls()
        self.process_search_pages()
        self.save('basic')