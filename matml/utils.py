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

def parse_unit(units):
    """Parses the MatML Units node (dictionary) with units u and power p into a string of the format u1p1u2p2u3p3..."""

    # if units is not a list, put it in a list
    units = units if isinstance(units, list) else [units]

    unit_str = ''
    for unit in units:
        unit_name = unit.get('Name')
        unit_power = unit.get('@power')
        if not unit_str == '':
            unit_str += '.'
        if unit_name:
            unit_str += unit_name
        if unit_power:
            unit_str += str(unit_power)
    return unit_str

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

def get_qualifiers(qualifiers):
    """
    get qualifiers, if exist and returns a dict of "qualifier_name: data" - pairs
    """
    qualifiers_dict = dict()
    if qualifiers is not None:
        qualifiers = qualifiers if isinstance(qualifiers, list) else [qualifiers]
        for qualifier in qualifiers:
            qualifiers_dict.update({qualifier.get('@name'): qualifier.get('#text')})
        return qualifiers_dict
    else:
        return None

def get_property(pr, propertydetails):
    """
    From a property or parameter, extract useful data and return a dictionary
    """
    p = dict()
    p['id'] = pr.get('@property')
    pr_det = [pr_det for pr_det in propertydetails if pr_det.get('@id') == p['id']][0]
    p['name'] = pr_det.get('Name')
    pr_units = pr_det.get('Units')
    p['unit'] = parse_unit(pr_units.get('Unit')) if pr_units is not None else '[-]'
    p['data'] = pr.get('Data')
    return p

def get_parameter(pa, parameterdetails):
    """
    From a property or parameter, extract useful data and return a dictionary
    """
    p = dict()
    p['id'] = pa.get('@parameter')
    pa_det = [pa_det for pa_det in parameterdetails if pa_det.get('@id') == p['id']][0]
    p['name'] = pa_det.get('Name')
    pa_units = pa_det.get('Units')
    p['unit'] = parse_unit(pa_units.get('Unit')) if pa_units is not None else '[-]'
    p['data'] = pa.get('Data')
    return p

def make_matson(matml_dict):
    """
    from a matml in form of a dictionary, create a nice human readable json of properties
    """
    matson = dict()
    matson['properties'] = list()

    propertydata = matml_dict.get('Material').get('BulkDetails').get('PropertyData')
    propertydetails = matml_dict.get('Metadata').get('PropertyDetails')
    parameterdetails = matml_dict.get('Metadata').get('ParameterDetails')

    for pr in propertydata:
        # property data will be stored in a dictionary p
        pr_ = dict()

        # extract some basic properties
        pr_.update(get_property(pr, propertydetails))

        # get qualifiers, if exist
        pr_['qualifiers'] = get_qualifiers(pr.get('Qualifier'))

        parameters = pr.get('ParameterValue')
        if parameters is not None:
            parameters = parameters if isinstance(parameters, list) else [parameters]
            params_ = list()
            for pa in parameters:
                pa_ = get_parameter(pa, parameterdetails)
                pa_['qualifiers'] = get_qualifiers(pa.get('Qualifier'))
                params_.append(pa_)
            pr_['params'] = params_
        
        matson['properties'].append(pr_)
        
    return matson
