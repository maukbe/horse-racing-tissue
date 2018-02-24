import pandas as pd
import node_parser
import utils
from lxml import etree

class HorseDataCreator:

    def __init__(self, horse_nodes):
        self.horse_nodes = horse_nodes
        self.df = pd.DataFrame(columns=["Number","Weight", "OR", "Previous OR"])
        self.runners = len(horse_nodes)

    def create_data_frame(self):
        print("Creating horses data frame")
        for i in range(1,self.runners + 1):
            print("Parsing horse ", i)
            node = etree.ElementTree(self.horse_nodes[i - 1])
            weight = self.get_weight(node)
            official_rating = self.get_or(node)
            print(official_rating)
            old_official_rating = self.get_previous_or(node)
            self.df.append([i,weight,official_rating,old_official_rating])
        return self.df

    def get_weight(self, horse_node):
        weight_string = node_parser.extract_weight(horse_node)
        return utils.parseWeight(weight_string)

    def get_or(self, horse_node):
        return node_parser.get_or(horse_node)

    def get_previous_or(self, horse_node):
        pass
#        old_or = ""
#        try:
#            old_or = node_parser.get_old_or(horse_node)
#        except ValueError:
#            print("No previous OR")
#        return old_or