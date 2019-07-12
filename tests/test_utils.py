import pytest
from matml import utils
import xml.etree.ElementTree as et
import pprint

pp = pprint.PrettyPrinter(indent=4, compact=True)

def test_parse_text():
    assert utils.parse_text('123') == 123
    assert utils.parse_text('1.234') == 1.234
    assert utils.parse_text('    \n\r    My text     \n\r    ') == "My text"

def test_node_with_text():
    source = "<textnode>Some text...</textnode>"
    target = {'textnode': "Some text..."}
    node = et.fromstring(source)
    temp = utils.matml_to_dict(node)
    assert temp == target

def test_node_with_attrib():
    source = """<?xml version="1.0"?>
    <country name="Liechtenstein">
        Some text...
    </country>
    """
    target = {
        'country': {
            '@name': "Liechtenstein",
            '#text': "Some text..."
        }
    }
    node = et.fromstring(source)
    temp = utils.matml_to_dict(node)
    assert temp == target

def test_node_with_children():
    source = """<?xml version="1.0"?>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
    </country>
    """
    target = {
        'country': {
            '@name': "Liechtenstein",
            'rank': 1,
            'year': 2008,
            'gdppc': 141100,
        }
    }
    node = et.fromstring(source)
    temp = utils.matml_to_dict(node)
    pp.pprint(temp)
    assert temp == target
