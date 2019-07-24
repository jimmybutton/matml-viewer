import xml.etree.ElementTree as et
import matml.utils as mu
import json
import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True)

filename = "matml-examples/MatML3e1.xml"

with open(filename, 'r', encoding="utf-8") as fp:
    orig_data = fp.read()

rootnode = et.fromstring(orig_data)

# with open("sandbox/MatML3e1_own.json", 'w', encoding='utf-8') as fp:
#     json.dump(mu.matml_to_dict(rootnode), fp, sort_keys=True, indent=4)

print(json.dumps(mu.matml_to_dict(rootnode), sort_keys=True, indent=4, ensure_ascii=False))
