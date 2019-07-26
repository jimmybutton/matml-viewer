import xml.etree.ElementTree as et
import matml.utils as mu
import json
import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True)

def parse_unit(units):
    """Parses the MatML Units node with units u and power p into a string of the format u1p1u2p2u3p3..."""

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

# filename = "MatML3e3"
filename = "Zytel FG70G30 HSR2 - Creep 80C"

with open("matml-examples/" + filename + ".xml", 'r', encoding="utf-8") as fp:
    orig_data = fp.read()

rootnode = et.fromstring(orig_data)

with open("sandbox/" + filename + ".json", 'w', encoding='utf-8') as fp:
    json.dump(mu.matml_to_dict(rootnode), fp, sort_keys=True, indent=4)

material = mu.matml_to_dict(rootnode)

# print the data
# print(json.dumps(material, sort_keys=True, indent=4, ensure_ascii=False))

try:
    material = material.get('EngineeringData').get('Materials')
except:
    pass

propertydata = material.get('MatML_Doc').get('Material').get('BulkDetails').get('PropertyData')
propertydetails = material.get('MatML_Doc').get('Metadata').get('PropertyDetails')
parameterdetails = material.get('MatML_Doc').get('Metadata').get('ParameterDetails')

for pr in propertydata:
    pr_id = pr.get('@property')
    pr_det = [pr_det for pr_det in propertydetails if pr_det.get('@id') == pr_id][0]
    pr_name = pr_det.get('Name')
    pr_units = pr_det.get('Units')
    pr_unit = parse_unit(pr_units.get('Unit')) if pr_units is not None else '[-]'
    pr_data = pr.get('Data')
    print(pr_name, ':', pr_data, pr_unit)

    qualifiers = pr.get('Qualifier')
    if qualifiers is not None:
        qualifiers = qualifiers if isinstance(qualifiers, list) else [qualifiers]
        for qualifier in qualifiers:
            print("    Q:", qualifier.get('@name'), ":", qualifier.get('#text'))

    parameters = pr.get('ParameterValue')
    if parameters is not None:
        parameters = parameters if isinstance(parameters, list) else [parameters]
        for pa in parameters:
            pa_id = pa.get('@parameter')
            pa_det = [pa_det for pa_det in parameterdetails if pa_det.get('@id') == pa_id][0]
            pa_name = pa_det.get('Name')
            pa_units = pa_det.get('Units')
            pa_unit = parse_unit(pa_units.get('Unit')) if pa_units is not None else '[-]'
            pa_data = pa.get('Data')
            print('   ', pa_name, ':', pa_data, pa_unit)

            qualifiers = pa.get('Qualifier')
            if qualifiers is not None:
                qualifiers = qualifiers if isinstance(qualifiers, list) else [qualifiers]
                for qualifier in qualifiers:
                    print("       Q:", qualifier.get('@name'), ":", qualifier.get('#text'))
