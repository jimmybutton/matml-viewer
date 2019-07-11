import pytest
from matml import utils

def test_node_with_text():
    source = "<textnode>Some text...</textnode>"
    target = {'textnode': "Some text..."}
    temp = utils.todict(source)
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
    temp = utils.todict(source)
    assert temp == target
