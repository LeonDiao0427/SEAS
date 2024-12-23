import json
import random

# load safety data
with open('', 'r') as file:
    data1 = json.load(file)

# load general data
with open('', 'r') as file:
    data2 = json.load(file)

combined_data = data1 + data2

random.shuffle(combined_data)

# make new data
with open('', 'w') as file:
    json.dump(combined_data, file, indent=4,ensure_ascii=False)


