from math import isclose

def parse_text(some_string):
    """
    Tries to convert string into integer or double, if not possible returns string.
    If string is empty, returns None.
    String can be multiple lines, will be concatenated and stripped of whites spaces.
    """

    if some_string is None:
        return None

    try:
        some_float = float(some_string)
    except ValueError:
        # if it cannot be converted into a float, it is probably a string
        temp_str = " ".join([line.strip() for line in some_string.splitlines()]).strip()
        if temp_str == '':
            return None
        else:
            return temp_str

    try:
        some_integer = int(some_float)
    except ValueError:
        pass

    if isclose(some_float,some_integer, rel_tol=1e-9):
        # if the float is not different from the integer, return the integer
        return some_integer
    else:
        return some_float

def parse_data(some_input, seperator=','):
    """
    Takes a string consisting of numbers seperated by comma and turns it into
    a list of numbers.
    """
    if type(some_input) in [float, int] or some_input is None:
        return some_input

    if isinstance(some_input, str):
        values = [parse_text(value.strip()) for value in some_input.split(seperator)]
    else:
        raise TypeError("parse_data only takes string, float, int or none. provided: {}".format(some_input))

    if len(values) == 1:
        return values[0]
    else:
        return values

def matml_to_dict(node):
    node_name = node.tag
    node_value = node.text
    node_attrib = node.attrib
    data_dict = dict()

    # if nodename is Data, don't care about children and attributes
    if node_name == 'Data':
        return {node_name: parse_data(node_value)}

    if node_attrib:
        for k, v in node_attrib.items():
            data_dict.update({"@{}".format(k): parse_text(v)})

    for child in node:
        child_dict = matml_to_dict(child)
        for k, v in child_dict.items():
            if k in data_dict.keys():
                if type(data_dict[k]) in [list]:
                    data_dict[k].append(v)
                else:
                    # turn into a list if it is not already
                    data_dict[k] = [data_dict[k]]
                    data_dict[k].append(v)
            else:
                data_dict.update(child_dict)

    if len(data_dict.keys()) > 0:
        node_value = parse_text(node_value)
        if not (node_value == '' or node_value is None):
            data_dict.update({"#text": node_value})
        return {node_name: data_dict}
    else:
        return {node_name: parse_text(node_value)}

def make_matson():
    """
    from a matml in form of a dictionary, create a nice human readable json
    """
    pass
