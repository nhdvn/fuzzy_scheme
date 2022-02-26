
import json, numpy as np


_1024 = np.genfromtxt('1024.csv', delimiter = ',')
    

def filter_templates():

    result = {}

    for id_row, row in enumerate(_1024):
        id_usr = int(row[-1]) 
        
        if id_usr not in result:
            result[id_usr] = []
        
        result[id_usr] += [id_row]

    json_file = open('user_templates.json', 'w')

    json.dump(result, json_file, indent = 4)

    json_file.close()


def read_user_templates() -> dict:

    json_file = open('user_templates.json', 'r')

    user_data = json.load(json_file)

    json_file.close()

    return user_data


filter_templates()