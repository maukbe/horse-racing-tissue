from lxml import etree

# Parser functions for a horse node

# Get the weight
# @node  Node representing the horse
# return Horse weight
def extract_weight(horseNode):
    return horseNode.find("//span[@class='weight']").text
    
def get_number(horseNode):
    return horseNode.find("//span[@class='card-no-draw__no']").text
    
def get_url(horseNode):
    return horseNode.find("//a").get("href")
    
def get_or(horseNode):
    return horseNode.find("//span[@class='card-icon-text icon-text-steel']").text
    
def get_old_or(horseNode):
    return horseNode.find("//span[@class='icon-text-steel or']").text
    
def get_trainer_url(horse_node):
    links = horse_node.find("//div[@class='card-jockey-trainer']")
    return links[1].get("href")
    
def get_jockey_url(horse_node):
    links = horse_node.find("//div[@class='card-jockey-trainer']")
    return links[0].get("href")
    
def get_trainer_form(trainer_node):
    div = trainer_node.find("//div[@id='tab-last-14-days']")
    try:
        table = etree.ElementTree(div).find("//tbody")
    except:
        print ("No previous trainer data for the last 14 days")
        return (0,0)
    row_array = etree.ElementTree(table).findall("//tr")
    # Get the last row in the table with the totals
    row = row_array[len(row_array)-1]
    total_runner = etree.ElementTree(row).findall("//td")
    totals = (int(total_runner[1].text), int(total_runner[2].text))
    return totals
    
def get_jockey_form(jockey_node):
    div = jockey_node.find("//div[@id='tab-last-14-days']")
    try:
        table = etree.ElementTree(div).find("//tbody")
    except:
        print ("No previous jockey data for the last 14 days")
        return (0,0)
    row_array = etree.ElementTree(table).findall("//tr")
    # Get the last row in the table with the totals
    row = row_array[len(row_array)-1]
    total_runner = etree.ElementTree(row).findall("//td")
    totals = (int(total_runner[1].text), int(total_runner[2].text))
    return totals

def get_last_result(form_node):
    form_table = form_node.find("//table[@id='horse-form-full']")
    races = etree.ElementTree(form_table).findall("//tr")
    last_race = races[1]
    for i in range(1,len(races)):
        if "class" in races[i].attrib:
            i = i + 1
        else:
            last_race = races[i]
    result_cell = etree.ElementTree(last_race).findall("//td")[3]
    result_span = etree.ElementTree(result_cell).find("//span")
    strong_array = etree.ElementTree(result_span).find("//strong")
    if strong_array is None:
        return result_span.text
    else:
        return strong_array.text

# Get the last n races
def get_last_races(form_node, n):
    form_table = form_node.find("//table[@id='horse-form-full']")
    races = etree.ElementTree(form_table).findall("//tr")
    valid_races = []
    added_races = 0
    for i in range(1, len(races)):
        if "class" in races[i].attrib:
            continue
        else:
            valid_races.append(races[i])
            added_races = added_races + 1
        i = i + 1
        if added_races == n:
            break
    return valid_races

def get_race_result(form_node):
        result_cell = etree.ElementTree(form_node).findall("//td")[3]
        result_span = etree.ElementTree(result_cell).find("//span")
        strong_array = etree.ElementTree(result_span).find("//strong")
        if strong_array is None:
            return result_span.text
        else:
            return strong_array.text