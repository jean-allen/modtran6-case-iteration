import json
import numpy as np
import copy


#### This is the stuff that a user might change
templateFile = 'template.json'
editThis = 'TPTEMP'    ## Options: 'TPTEMP'
lower_bound = 650
upper_bound = 1650
increment = 50


# Turn those bounds into a list of values to iterate over
# @jean this sucks right now
new_values = np.arange(lower_bound, upper_bound, increment).tolist()

# Open up the json file and load it into a dictionary
f = open(templateFile)
data = json.load(f)

# This will become the output json file with many cases in it :) right now she is empty
allCases = []

for thisCase in data['MODTRAN']:

    base_name = thisCase['MODTRANINPUT']['NAME']

    for value in new_values:
        newCase = copy.deepcopy(thisCase)

        # Find the 'address' of the key we're interested in iterating over
        for key in newCase['MODTRANINPUT'].keys():
            if type(newCase['MODTRANINPUT'][key]) != dict:
                continue
            if editThis in newCase['MODTRANINPUT'][key]:
                rightKey = key

        # Change the key we're interested in to the set value
        newCase['MODTRANINPUT'][rightKey][editThis] = value

        # Change the case name and the output file names
        newName = base_name + '_' + str(value) + 'K'
        newCase['MODTRANINPUT']['NAME'] = newName
        newCase['MODTRANINPUT']['FILEOPTIONS']["SLIPRNT"] = newName + '.sli'
        newCase['MODTRANINPUT']['FILEOPTIONS']["CSVPRNT"] = newName + '.csv'

        # Add the case we just built to our list
        allCases.append(newCase)

output = {"MODTRAN": allCases}

with open("allCases.json", "w") as outfile:
    json.dump(output, outfile, indent=2)
