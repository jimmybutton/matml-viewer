from math import log10, floor

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def parse_text(some_string):
    """Tries to convert string into integer or double, if not possible returns string.
    String can be multiple lines, will be concatenated and stripped of whites spaces."""

    try:
        some_float = float(some_string)
    except ValueError:
        # if it cannot be converted into a float, it is probably a string
        return " ".join([line.strip() for line in some_string.splitlines()]).strip()

    try:
        some_integer = int(some_float)
    except ValueError:
        pass

    if round_sig(some_float,6) == some_integer:
        # if the float is not different from the integer, return the integer
        return some_integer
    else:
        return some_float

def matml_to_dict(node):
    node_name = node.tag
    node_value = node.text
    node_attrib = node.attrib
    data_dict = dict()
    if node_attrib:
        for k, v in node_attrib.items():
            data_dict.update({"@{}".format(k): v})
            if not (node_value == '' or node_value is None):
                data_dict.update({"#text": parse_text(node_value)})
        for child in node:
            data_dict.update(matml_to_dict(child))
        return {node_name: data_dict}
    else:
        return {node_name: node_value}
