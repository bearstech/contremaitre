import unittest
from cStringIO import StringIO
from contremaitre.procfile import Procfile


class TestProcfile(unittest.TestCase):

    def test_simple(self):
        proc = Procfile('tests/Procfile', ['tests/env'])
        conf = StringIO()
        proc.as_supervisor('bob').write(conf)
        print conf.getvalue()
        assert False
