import xml.etree.ElementTree as et

def todict(matml_as_string):
    root = et.fromstring(matml_as_string)
    node_name = root.tag
    node_value = " ".join([line.strip() for line in root.text.splitlines()]).strip()
    node_attrib = root.attrib
    data_dict = {}
    if node_attrib:
        for k, v in node_attrib.items():
            data_dict.update({"@{}".format(k): v})
            data_dict.update({"#text": node_value})
        return {node_name: data_dict}
    else:
        return {node_name: node_value}
