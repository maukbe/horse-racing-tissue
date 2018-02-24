import pandas as pd

class HorseDataCreator:

    def __init__(self, horse_nodes):
        self.horse_nodes = horse_nodes
        self.df = pd.DataFrame(columns=["Weight", "OR", "Previous OR"])

    def create_data_frame(self):
        pass

    def get_weight(self):
        pass

    def get_or(self):
        pass

    def get_previous_or(self):
        pass