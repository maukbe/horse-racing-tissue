from lxml import etree
import requests
import pandas as pd

# Generate a panda data frame representing the current race
def scrape_current_race(race_url):
    page = requests.get('http://www.attheraces.com/racecard/Kelso/15-February-2018/1325')
    pageTree = etree.HTML(page.text)

