import unittest
from cStringIO import StringIO
from contremaitre.procfile import Procfile


class TestProcfile(unittest.TestCase):

    def test_simple(self):
        proc = Procfile('tests/Procfile', ['tests/env'])
        conf = StringIO()
        proc.as_supervisor('bob', {'worker': 2}).write(conf)
        print conf.getvalue()
        assert False
