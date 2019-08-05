import xml.etree.ElementTree as et
import matml.utils as mu
import json
import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True)

# filename = "MatML3e3"
filename = "Zytel FG70G30 HSR2 - Creep 80C"

with open("matml-examples/" + filename + ".xml", 'r', encoding="utf-8") as fp:
    orig_data = fp.read()

rootnode = et.fromstring(orig_data)

with open("sandbox/" + filename + ".json", 'w', encoding='utf-8') as fp:
    json.dump(mu.matml_to_dict(rootnode), fp, sort_keys=True, indent=4)

material = mu.matml_to_dict(rootnode)

try:
    material = material.get('EngineeringData').get('Materials')
except:
    pass

matml_dict = material.get('MatML_Doc')

matson = mu.make_matson(matml_dict)

# print the data
# pp.pprint(matson)
print(json.dumps(matson, sort_keys=True, indent=4, ensure_ascii=False))
