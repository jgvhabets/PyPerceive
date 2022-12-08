""" create a json file """

import json

# write a dictionary 
matpart_dict = {"Survey": "LMTD",
               "Streaming": "BrainSense",
               "Timeline": "CHRONIC"
               }

# turn dictionary into string and dump it into json file
json_string = json.dumps(matpart_dict, indent=4) # indent will make the line better to read in the json file
                                                 # the dump function will dump the dictionary into a string 
# write a json file 
with open ('matpart.json', "w") as f:            # chose a name for the new json file, "w" stands for write
    f.write(json_string)

print("Json created")

