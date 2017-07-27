from candemaker.cande import CandeObj
from .objs import Master, Control, Info


def test_CandeObj_empty():
    obj = CandeObj.empty()
    d = {'Master': None, 'Control': None, 'Info': None, '_groups': [], '_nodes': [], '_elements': [], '_boundaries': [], '_materials': [], '_factors': []}
    assert vars(obj) == d