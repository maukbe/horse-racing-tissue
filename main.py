from lxml import html
from lxml import etree
import requests
from Horse import Horse
from TissueCreator import TissueCreator
from horsedata import HorseData
import utils
import node_parser

page = requests.get('http://www.attheraces.com/racecard/Kelso/15-February-2018/1535')
eTree = etree.HTML(page.text)


#This will create a list of horses
page = eTree.xpath('//body[@id="atr-body"]')
horses = etree.ElementTree(page[0]).findall('//div[@class="card-item"]')

horse_data_dict = {}
i = 1
for horse_div in horses:
    print ("Downloading data for horse: ", i)
    horse_node = etree.ElementTree(horse_div)
    
    # Get horse form
    horse_url = node_parser.get_url(etree.ElementTree(horse_div))
    horse_page = requests.get("http://www.attheraces.com" + horse_url)
    horse_e_tree = etree.HTML(horse_page.text)
    horse_form = horse_e_tree.xpath('//body[@id="atr-body"]')
    horse_form_node = etree.ElementTree(horse_form[0])
    
    # Get trainer form
    trainer_form_url = node_parser.get_trainer_url(etree.ElementTree(horse_div))
    trainer_page = requests.get("http://www.attheraces.com" + trainer_form_url)
    trainer_e_tree = etree.HTML(trainer_page.text)
    trainer_form = trainer_e_tree.xpath('//body[@id="atr-body"]')
    trainer_form_node = etree.ElementTree(trainer_form[0])
    
    # Get jockey form
    jockey_form_url = node_parser.get_jockey_url(etree.ElementTree(horse_div))
    jockey_page = requests.get("http://www.attheraces.com" + trainer_form_url)
    jockey_e_tree = etree.HTML(jockey_page.text)
    jockey_form = trainer_e_tree.xpath('//body[@id="atr-body"]')
    jockey_form_node = etree.ElementTree(jockey_form[0])
    
    # Save data
    horse_data = HorseData(i,horse_node,horse_form_node,trainer_form_node, jockey_form_node)
    horse_data_dict[i] = horse_data
    i = i+1
    
# Get the race distance
distance_string = node_parser.get_race_distance(etree.ElementTree(page[0]))
distance_furlongs = utils.parse_distance(distance_string) 
print("Race distance", distance_furlongs)

tissue = TissueCreator(horse_data_dict, distance_furlongs)
tissue.create_tissue()



#horseDiv = horses[0]
#weight = parser.extract_weight(etree.ElementTree(horseDiv))
#number = parser.get_number(etree.ElementTree(horseDiv))
#print "Horse weight and number: ",utils.parseWeight(weight), number
#horseObjects.append(Horse(utils.parseWeight(weight), number))
#print "Finding horse form..."
#horse_url = parser.get_url(etree.ElementTree(horseDiv))
#print "http://www.attheraces.com" + horse_url
#horse_page = requests.get("http://www.attheraces.com" + horse_url)
#print "Parsing form..."
##print horse_page.text
#horse_e_tree = etree.HTML(horse_page.text)
#print "Getting OR for this race..."
#off_rec = parser.get_or(etree.ElementTree(horseDiv))
#print "OR :", off_rec
#print "Creating form eTree"
#horse_form = horse_e_tree.xpath('//body[@id="atr-body"]')
#print "Finding previous OR"
#print "Old OR: ", parser.get_old_or(etree.ElementTree(horse_form[0]))

    

#tissue = TissueCreator(horseObjects)
#tissue.calculateWeightScore()
    

