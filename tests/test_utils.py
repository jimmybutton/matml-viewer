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
    assert temp == target

def test_node_with_multiple_children_of_same_name():
    source = """<?xml version="1.0"?>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    """
    target = {
        'country': {
            '@name': "Liechtenstein",
            'rank': 1,
            'year': 2008,
            'gdppc': 141100,
            'neighbor': [
                {
                    '@name': 'Austria',
                    '@direction': 'E'
                }, {
                    '@name': 'Switzerland',
                    '@direction': 'W'
                }
            ]
        }
    }
    node = et.fromstring(source)
    temp = utils.matml_to_dict(node)
    assert temp == target

def test_countries_complete():
    source = """<?xml version="1.0"?>
    <data>
        <country name="Liechtenstein">
            <rank>1</rank>
            <year>2008</year>
            <gdppc>141100</gdppc>
            <neighbor name="Austria" direction="E"/>
            <neighbor name="Switzerland" direction="W"/>
        </country>
        <country name="Singapore">
            <rank>4</rank>
            <year>2011</year>
            <gdppc>59900</gdppc>
            <neighbor name="Malaysia" direction="N"/>
        </country>
        <country name="Panama">
            <rank>68</rank>
            <year>2011</year>
            <gdppc>13600</gdppc>
            <neighbor name="Costa Rica" direction="W"/>
            <neighbor name="Colombia" direction="E"/>
        </country>
    </data>
    """
    target = {
        'data': {
            'country': [
                {
                    '@name': "Liechtenstein",
                    'rank': 1,
                    'year': 2008,
                    'gdppc': 141100,
                    'neighbor': [{
                            '@name': 'Austria',
                            '@direction': 'E'
                        }, {
                            '@name': 'Switzerland',
                            '@direction': 'W'
                        }
                    ]
                }, {
                    '@name': "Singapore",
                    'rank': 4,
                    'year': 2011,
                    'gdppc': 59900,
                    'neighbor': {
                        '@name': 'Malaysia',
                        '@direction': 'N'
                    }
                }, {
                    '@name': "Panama",
                    'rank': 68,
                    'year': 2011,
                    'gdppc': 13600,
                    'neighbor': [{
                            '@name': 'Costa Rica',
                            '@direction': 'W'
                        }, {
                            '@name': 'Colombia',
                            '@direction': 'E'
                        }
                    ]
                }
            ]
        }
    }
    node = et.fromstring(source)
    temp = utils.matml_to_dict(node)
    pp.pprint(temp)
    assert temp == target
