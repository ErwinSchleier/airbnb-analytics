## Project Overview

A web scraper for AirBnb. This script will extract information like title, price, rating and bedrooms for a given location and store them in a csv file. You can use it to track your next holiday target or collect data for some analytics.

This project is inspired by [X-technology](https://github.com/x-technology/airbnb-analytics). If you want to get a deeper understanding, visit the blog posts or webinar videos below.

Also be aware that airbnb could change all tag id's inside of file ***airbnb_parser.py*** so if your extracted file is missing data you need to update them.

## Project Setup

1. Clone the repository
2. Create a virtual environment and activate it

```bash
virtualenv venv
source venv/bin/activate
```
3. Install all required packages
```bash
pip install -r requirements.txt
```
4. Run airbnb_run.py
```bash
python airbnb_run.py
```

## Server Deployment

Selenium requires a browser like Google-Chrome.

For deployment to a server a headless version of Google-Chrome is required as well as a [ChromeDriver](https://chromedriver.chromium.org/).

Here is a nice guide for installing [Google-Chrome Headless Version](https://www.notion.so/Chromedriver-Error-caa1ab54c6684318bb60a4bc6caac7b5#f48813bee20c44b8963667c41a80b266).

Check your google-chrome version

```bash
google-chrome --version
```

Go to the [ChromeDriver](https://chromedriver.chromium.org/) homepage and navigate to the driver file which matches your Chrome version and OS. For example Chrome version 95 for Linux would be

```bash
wget https://chromedriver.storage.googleapis.com/95.0.4638.69/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```

Test it by including your extracted ChromeDriver path into to following script:

```python
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome('YOUR_CHROMEDRIVER_PATH', chrome_options=chrome_options,  service_args=['--verbose'])


driver.get('https://google.org')
print(driver.title)
```

If you don't see any errors, the installation was successful. Now you have to include the commented part inside function ***extract_listings_dynamic*** on file ***airbnb_parser.py***.

In case you are facing any error messages, please open an issue ticket! 

## Series of articles on [Medium](https://smithio.medium.com):
- [Part 0 - Intro to the project](https://smithio.medium.com/educational-data-science-project-b4f54c7cab19)
- [Part 1 - Scrape the data from Airbnb website](https://smithio.medium.com/scraping-airbnb-website-with-python-beautiful-soup-and-selenium-8ec86e327b6c)
- [Part 2 - More details to Web Scraping](https://smithio.medium.com/more-details-to-web-scraping-with-python-and-selenium-c32ac614c558)

## Webinars on [Youtube](https://www.youtube.com/channel/UCQZNnzybEi0vvNbeDB0qABQ):
- [Scraping Airbnb website with Python and Beautiful Soup](https://youtu.be/B7uOXdHc8jc)
- [Scraping Airbnb website with Python and Selenium](https://youtu.be/L8ooiuBnZ8M)
- [Airbnb data cleaning](https://www.youtube.com/watch?v=6iJ8MMDNQ9c&t=86s)
