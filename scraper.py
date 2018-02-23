from lxml import etree
import requests
import pandas as pd
import node_parser
import utils

class Scraper:

    def __init__(self, race_url):
        page = requests.get(race_url)
        page_tree = etree.HTML(page.text)
        body_tree = page_tree.xpath('//body[@id="atr-body"]')[0]
        self.page_node = etree.ElementTree(body_tree)
        self.race_dict = {}
    #    self.race_df = pd.DataFrame()

    # Generate a panda data frame representing the current race
    def scrape_current_race(self):
        self.find_race_distance()
        self.find_location()
        self.find_race_going()
        race_df = pd.Series(self.race_dict)
        print(race_df)

    def find_location(self):
        print("Parsing race location")
        time_location_string = node_parser.find_race_location(self.page_node)
        location = utils.parse_time_location_string(time_location_string)
        self.race_dict['Location'] = location

    def find_race_distance(self):
        print("Parsing race distance")
        distance_string = node_parser.get_race_distance(self.page_node)
        distance_furlongs = utils.parse_distance(distance_string)
        self.race_dict['Distance'] = distance_furlongs

    def find_race_going(self):
        print("Parsing race going")
        going = node_parser.find_race_going(self.page_node)
        self.race_dict["Going"] = going
