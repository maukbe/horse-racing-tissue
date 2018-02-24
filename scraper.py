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
        self.horses = {}
    #    self.race_df = pd.DataFrame()

    # Generate a panda data frame representing the current race
    def scrape_current_race(self):
        self.find_race_distance()
        self.find_location()
        self.find_race_going()
        race_df = pd.Series(self.race_dict)
        print("Parsed race data:")
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

    def scrape_horse_nodes(self):
        i = 1
        for horse_div in self.horses:
            print("Downloading data for horse: ", i)
            horse_node = etree.ElementTree(horse_div)

            # Get horse form
            horse_url = node_parser.get_url(etree.ElementTree(horse_div))
            horse_page = requests.get("http://www.attheraces.com" + horse_url)
            horse_e_tree = etree.HTML(horse_page.text)
            horse_form = horse_e_tree.xpath('//body[@id="atr-body"]')
            horse_form_node = etree.ElementTree(horse_form[0])
            self.horses[i] = horse_form_node
            i = i + 1

