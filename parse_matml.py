import xml.etree.ElementTree as et
import matml.utils as mu
import json
import pprint
import sys
from os import path

pp = pprint.PrettyPrinter(indent=4, compact=True)

if __name__ == "__main__":

    try:
        print(len(sys.argv))
        print(sys.argv)
        # filename = "matml-examples\Zytel FG70G30 HSR2 - Creep 80C.xml"
        filepath = sys.argv[1]
        print(filepath)
    except:
        print("Please pass filename when calling the script.")
        sys.exit()

    filename = path.basename(filepath).split('.')[0]

    with open(filepath, 'r', encoding="utf-8") as fp:
        orig_data = fp.read()

    # get root node from string
    rootnode = et.fromstring(orig_data)

    # transform xml into json
    material = mu.matml_to_dict(rootnode)

    # from the dict, get the correct node (MatML_Doc)
    try:
        material = material.get('EngineeringData').get('Materials')
    except:
        pass

    matml_dict = material.get('MatML_Doc')

    # create a pretty dict
    matson = mu.make_matson(matml_dict)

    # save both versions as json to seperate files
    with open("sandbox/" + filename + ".json", 'w', encoding='utf-8') as fp:
        json.dump(matml_dict, fp, sort_keys=True, indent=2)
    
    with open("sandbox/" + filename + "_pretty.json", 'w', encoding='utf-8') as fp:
        json.dump(matson, fp, indent=2)

    # print the data
    # pp.pprint(matson)
