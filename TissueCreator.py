# Take an array of horses and race information and calculate the odds for each
# horse
import parser
import utils
from position import Position

class TissueCreator:
        def __init__(self, horse_data_dict):
            self.horse_data_dict = horse_data_dict
            self.runners = len(horse_data_dict)
            self.scores = {}
            
        def create_tissue(self):
            self.calculateWeightScores()
            self.calculate_or_scores()
            self.calculate_trainer_scores()
            
            print(self.scores)
            print ("Tissue odds:")
            total_score = sum(self.scores.values())
            for key in self.scores:
                if self.scores[key] < 0:
                    self.scores[key] = 0.1
            for key in self.scores:
                odds = float(self.scores[key])/float(total_score)
                print (key, 1/odds)
        
        def calculate_trainer_scores(self):
            print("Calculating trainer scores")
            for key in self.horse_data_dict:
                # Get totals and winners
                trainer_form = self.horse_data_dict[key].trainer_form
                totals = parser.get_trainer_form(trainer_form)
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
                        
                
                
                
        def calculate_or_scores(self):
            print ("Calculating OR scores")
            or_dict = {}
            for key in self.horse_data_dict:
                horse_data = self.horse_data_dict[key]
                # Get current OR
                current_or = parser.get_or(horse_data.race_info)
                old_or = parser.get_old_or(horse_data.form)
                or_dict[key] = (current_or, old_or)
            
            for key in or_dict:
                current_or = int(or_dict[key][0])
                try:
                    old_or = int(or_dict[key][1])
                except ValueError:
                    print ("Horse ", key, " has no previous OR")
                    continue
                last_result_string = parser.get_last_result(self.horse_data_dict[key].form)
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
                weight = parser.extract_weight(self.horse_data_dict[key].race_info) 
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
            print (self.scores)