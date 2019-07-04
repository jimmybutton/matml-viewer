import xmltodict as xd
import json

filename = "matml-examples/MatML3e1.xml"

with open(filename, 'r', encoding="utf-8") as fp:
    orig_data = fp.read()


with open("matml-examples/MatML3e1.json", 'w', encoding='utf-8') as fp:
    converted = json.dumps(xd.parse(orig_data))
    fp.write(converted)
