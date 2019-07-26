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

def test_parse_data():
    assert utils.parse_data(None) is None
    assert utils.parse_data(1) == 1
    assert utils.parse_data(1.23) == 1.23

    assert utils.parse_data('') is None
    assert utils.parse_data('1.23, 2.34') == [1.23, 2.34]
    assert utils.parse_data('972,561') == [972, 561]
    assert utils.parse_data('.0011,.0018,.0023,.0027,.0029') == [.0011,.0018,.0023,.0027,.0029]
    assert utils.parse_data('4,-,-') == [4, '-', '-']
    assert utils.parse_data('1109,,') == [1109, None, None]
    assert utils.parse_data("1.0E5,1.0E6,1.0E7,1.0E8,5.0E8") == [1.0E5,1.0E6,1.0E7,1.0E8,5.0E8]

def test_data_to_list():
    source = """<Data format="integer">972,561</Data>"""
    node = et.fromstring(source)
    assert utils.matml_to_dict(node) == {'Data': [972,561]}

    source = "<Data>23,1370</Data>"
    node = et.fromstring(source)
    assert utils.matml_to_dict(node) == {'Data': [23,1370]}

    source = """<Data format="float">+11.5,+8.5,+7,+6.5,+6.5</Data>"""
    node = et.fromstring(source)
    assert utils.matml_to_dict(node) == {'Data': [11.5,8.5,7,6.5,6.5]}
