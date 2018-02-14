# Take an array of horses and race information and calculate the odds for each
# horse
import node_parser
import utils
from position import Position

class TissueCreator:
        def __init__(self, horse_data_dict, distance):
            self.horse_data_dict = horse_data_dict
            self.runners = len(horse_data_dict)
            self.scores = {}
            self.distance = distance
            
        def create_tissue(self):
            self.calculateWeightScores()
            self.calculate_or_scores()
            self.calculate_trainer_scores()
            self.calculate_jockey_scores()
            self.calculate_distance_scores()
            
            print(self.scores)
            print ("Tissue odds:")
            total_score = sum(self.scores.values())
            for key in self.scores:
                if self.scores[key] <= 0:
                    self.scores[key] = 0.1
            for key in sorted(self.scores):
                odds = float(self.scores[key])/float(total_score)
                print (key, 1/odds)
#                
#        def calculate_distance_scores(self):
#            print("Calculating distance scores")
#            
#            for key in self.horse_data_dict:
#                horse_form = self.horse_data_dict[key].form
#                i = 0 
#                races = node_parser.get_last_races(6,horse_form)
#                while i < len(races):
#                    race = races[i]
#                    # Get last race result
#                    
#                    # If won or placed and race was similar distance to this 
#                    # one allocate points
#                    distance_furlongs = node_parser.get_form_race_distance(race)
#                    print (distance_furlongs)
#                    i = i + 1

        # TODO Check distance before adding to score
        # TODO Add a second score for the ground
        def calculate_distance_scores(self):
            print("Calculating distance scores")
            for key in self.horse_data_dict:
                print("Calculating distance score for horse " + str(key))
                horse_data = self.horse_data_dict[key]
                try:
                    last_races = node_parser.get_last_races(horse_data.form,6)
                except:
                    print("No prior race data")
                    continue
                for i in range(1, len(last_races)):
                    result_string = node_parser.get_race_result(last_races[i])
                    race_result = utils.parse_result(result_string)
                    if race_result == Position.WON:
                        self.scores[key] += 2
                    elif race_result == Position.PLACED:
                        self.scores[key] += 1
            self.normalise_scores()

        def calculate_jockey_scores(self):
            print("Calculating jockey scores")
            for key in self.horse_data_dict:
                print("Calculating jockey score for horse " + str(key))
                # Get totals and winners
                jockey_form = self.horse_data_dict[key].jockey_form
                totals = node_parser.get_jockey_form(jockey_form)
                wins = totals[1]
                if wins == 0:
                    continue
                win_percentage = 100*totals[0] / float(totals[1])
                if win_percentage <= 20 and win_percentage <= 25:
                    self.scores[key] = self.scores[key] + 1
                elif 25 < win_percentage and win_percentage <= 33:
                    self.scores[key] = self.scores[key] + 2
                elif 33 <= win_percentage and win_percentage < 50:
                    self.scores[key] = self.scores[key] + 3
                else:
                    self.scores[key] = self.scores[key] + 4
            self.normalise_scores()
            
        
        def calculate_trainer_scores(self):
            print("Calculating trainer scores")
            for key in self.horse_data_dict:
                # Get totals and winners
                trainer_form = self.horse_data_dict[key].trainer_form
                totals = node_parser.get_trainer_form(trainer_form)
                wins = totals[1]
                if wins == 0:
                    continue
                win_percentage = 100*totals[0] / float(totals[1])
                if wins > 3:
                    if win_percentage < 12:
                        self.scores[key] = self.scores[key] + 0.5
                    elif 12 <= win_percentage and win_percentage < 20:
                        self.scores[key] = self.scores[key] + 1
                    elif 20 <= win_percentage and win_percentage < 30:
                        self.scores[key] = self.scores[key] + 3
                    elif 30 <= win_percentage and win_percentage < 40:
                        self.scores[key] = self.scores[key] + 4
                    else:
                        self.scores[key] = self.scores[key] + 5
                else:
                    self.scores[key] = self.scores[key] + 0.5
            self.normalise_scores()
                        
        def calculate_or_scores(self):
            print ("Calculating OR scores")
            or_dict = {}
            for key in self.horse_data_dict:
                print("Parsing OR for horse " + str(key))
                horse_data = self.horse_data_dict[key]
                # Get current OR
                current_or = node_parser.get_or(horse_data.race_info)
                try:
                    old_or = node_parser.get_old_or(horse_data.form)
                except ValueError:
                    old_or = ""
                or_dict[key] = (current_or, old_or)
            
            for key in or_dict:
                print ("Getting OR for horse ", key)
                current_or = int(or_dict[key][0])
                try:
                    current_or = int(or_dict[key][0])
                    old_or = int(or_dict[key][1])
                except (ValueError, TypeError):
                    print ("Horse ", key, " has no previous OR")
                    continue
                last_result_string = node_parser.get_last_races(self.horse_data_dict[key].form,1)
                last_race_pos = utils.parse_result(last_result_string.strip())
                or_diff = abs(current_or - old_or)
                if current_or > old_or:
                    if last_race_pos == Position.WON:
                        self.scores[key] = self.scores[key] - 0.5*or_diff
                    elif last_race_pos == Position.PLACED:
                        self.scores[key] = self.scores[key] - or_diff
                    else:
                        self.scores[key] = self.scores[key] - 2*or_diff
                elif current_or < old_or:
                    if last_race_pos == Position.WON:
                        self.scores[key] = self.scores[key] + 0.5*or_diff
                    elif last_race_pos == Position.PLACED:
                        self.scores[key] = self.scores[key] + or_diff
                    else:
                        self.scores[key] = self.scores[key] + 2*or_diff
            self.normalise_scores()
            print (self.scores) 
            
        def normalise_scores(self):
            for key in self.scores:
                if self.scores[key] < 0:
                    self.scores[key] = 0
                    
        def calculateWeightScores(self):
            print ("Calculating weight scores")
            # Create dictionary of weights
            weight_pounds_dict = {}
            for key in self.horse_data_dict:
                weight = node_parser.extract_weight(self.horse_data_dict[key].race_info)
                weight_pounds_dict[key] = utils.parseWeight(weight)
            
            max_weight = max(weight_pounds_dict.values())
            min_weight = min(weight_pounds_dict.values())
            total_weight_diff = max_weight - min_weight
            score_per_pound = 10.0 / total_weight_diff
            av_weight = float(sum(weight_pounds_dict.values())/self.runners)
            for key in weight_pounds_dict:
                weight = weight_pounds_dict[key]
                weight_diff = max_weight - weight
                init_score = 10 - weight_diff * score_per_pound
                # Top horse always scores 10
                if key == 1:
                    init_score = 10
                # Last runner always has a score of 0
                if key == self.runners:
                    init_score = 0
                if weight >= av_weight - 7 and weight <= av_weight - 3:
                    self.scores[key] = init_score + 3
                elif weight <= av_weight - 8:
                    self.scores[key] = init_score + 1
                elif weight <= av_weight + 7 and weight >= av_weight + 3:
                    self.scores[key] = init_score - 1
                elif weight >= av_weight + 8:
                    self.scores[key] = init_score - 2
                else:
                    self.scores[key] = init_score
            self.normalise_scores()
            print (self.scores)