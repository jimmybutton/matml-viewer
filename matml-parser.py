import xml.etree.ElementTree as et

def parse_value(raw):

    if type(raw) not in [str, int, float]:
        raise ValueError('Error parsing {} of type {}. Can only parse str, int or float'.format(raw, type(raw)))

    try:
        # try to convert string to float
        return float(raw)
    except ValueError as e:
        return raw

def parse_unit(unit_node):
    unit_str = ''
    for unit in unit_node.iter('Unit'):
        unit_name = unit.find('./Name').text
        unit_power = unit.find("./Name['@power']")

tree = et.parse('matml-examples/Zytel FG70G30 HSR2 - Creep 80C.xml')
root = tree.getroot()

for pr in root.iter('PropertyData'):
    pr_data = [parse_value(raw) for raw in pr.find('Data').text.split(',')]
    pr_id = pr.attrib['property']
    pr_name = root.find(".//PropertyDetails[@id='" + pr_id + "']/Name").text
    print(pr_name, pr_data)
    for pa in pr.iter('ParameterValue'):
        pa_data = [parse_value(raw) for raw in pa.find('Data').text.split(',')]
        pa_id = pa.attrib['parameter']
        pa_name = root.find(".//ParameterDetails[@id='" + pa_id + "']/Name").text
        try:
            units_node = root.find(".//ParameterDetails[@id='" + pa_id + "']/Units")
            pa_units = parse_unit(units_node)
        except:
            pa_unit = None
        print(pa_name, pa_unit, pa_data)
