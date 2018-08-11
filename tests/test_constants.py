from grifter.constants import BLACKHOLE_LOOPBACK_MAP


def test_blackhole_loopback_map():
    assert BLACKHOLE_LOOPBACK_MAP == {'blackhole': '127.6.6.6'}
