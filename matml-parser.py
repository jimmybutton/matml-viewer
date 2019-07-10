import pprint

import xml.etree.ElementTree as et

# filename = 'matml-examples/Zytel FG70G30 HSR2 - Creep 80C.xml'
# filename = 'matml-examples/MatML3e1.xml'
# filename = 'matml-examples/MatML3e2.xml'
filename = 'matml-examples/MatML3e3.xml'

tree = et.parse(filename)
root = tree.getroot()

def parse_value(raw):

    if type(raw) not in [str, int, float]:
        raise ValueError('Error parsing {} of type {}. Can only parse str, int or float'.format(raw, type(raw)))

    try:
        # try to convert string to float
        return float(raw)
    except ValueError as e:
        return raw

def parse_unit(unit_node):
    """Parses the MatML Units node with units u and power p into a string of the format u1p1u2p2u3p3..."""

    unit_str = ''
    for unit in unit_node.iter('Unit'):
        unit_name = unit.find('Name').text
        unit_power = unit.get('power')
        if not unit_str == '':
            unit_str += '.'
        if unit_name:
            unit_str += unit_name
        if unit_power:
            unit_str += unit_power
    return unit_str

def get_unit(units_node):
    "Accepts the Units node. If units_node is None, is assumes it is unitless."
    if units_node is not None:
        try:
            unit = parse_unit(units_node)
            return unit
        except:
            print('Could not parse units for ParameterDetails id {}'.format(pa_id))
            return "ERROR"
    else:
        return '-'

properties = []

for pr in root.iter('PropertyData'):
    pr_data = [parse_value(raw) for raw in pr.find('Data').text.split(',')]
    pr_id = pr.attrib['property']
    pr_node = root.find(".//PropertyDetails[@id='" + pr_id + "']")
    pr_name = pr_node.find('Name').text
    pr_unit = get_unit(pr_node.find('Units'))

    parameters = []
    for pa in pr.iter('ParameterValue'):
        pa_data = [parse_value(raw) for raw in pa.find('Data').text.split(',')]
        pa_id = pa.attrib['parameter']
        pa_details = root.find(".//ParameterDetails[@id='" + pa_id + "']")
        pa_name = pa_details.find("Name").text
        units_node = pa_details.find("Units")
        pa_unit = get_unit(units_node)
        parameters.append({'name': pa_name, '_id': pa_id, 'unit': pa_unit, 'values': pa_data})

    properties.append({'name': pr_name, '_id': pr_id, 'values':pr_data, 'parameters': parameters, 'unit': pr_unit})

pp = pprint.PrettyPrinter(indent=4, compact=True)
pp.pprint(properties)
