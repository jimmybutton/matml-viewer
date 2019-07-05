import xml.etree.ElementTree as et
tree = et.parse('matml-examples/Zytel FG70G30 HSR2 - Creep 80C.xml')
root = tree.getroot()

for pr in root.iter('PropertyData'):
    pr_data = pr.find('Data').text
    pr_id = pr.attrib['property']
    pr_name = root.find(".//PropertyDetails[@id='" + pr_id + "']/Name").text
    print(pr_name, pr_data)
    for pa in pr.iter('ParameterValue'):
        pa_data = pa.find('Data').text
        pa_id = pa.attrib['parameter']
        pa_name = root.find(".//ParameterDetails[@id='" + pa_id + "']/Name").text
        print(pa_name, pa_data)
