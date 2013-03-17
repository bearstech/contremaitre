# -*- coding: utf-8 -
#
# This file is stolen from gaffer.
"""
module to parse and manage a Procfile
"""

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from collections import OrderedDict

import os
import re
import shlex

RE_LINE = re.compile(r'^([A-Za-z0-9_]+):\s*(.+)$')


class Procfile(object):
    """ Procfile object to parse a procfile and a list of given
environnment files. """

    def __init__(self, procfile, envs=None):
        """ main constructor

Attrs:

- **procfile**: procfile path
- **evs**: list of .envs paths, each envs will be added tho the
global procfile environment"""

        self.procfile = procfile
        self.root = os.path.dirname(procfile) or "."

        # set default env
        default_env = os.path.join(self.root, '.env')
        self.envs = [default_env]
        if envs is not None:
            self.envs.extend(envs)

        # initialize value
        self.cfg = self.parse(self.procfile)
        self.env = self.get_env(self.envs)

    def programs(self):
        """ iterator over the configuration """
        return self.cfg.items()

    def parse(self, procfile):
        """ main function to parse a procfile. It returns a dict """
        cfg = OrderedDict()
        with open(procfile) as f:
            lines = f.readlines()
            for line in lines:
                m = RE_LINE.match(line)
                if m:
                    cfg[m.group(1)] = m.group(2)
        return cfg

    def get_env(self, envs=[]):
        """ build the procfile environment from a list of procfiles """
        env = {}
        for path in envs:
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        p = line.split('=', 1)
                        if len(p) == 2:
                            k, v = p
                            # remove double quotes
                            v = v.strip('\n').replace('\"', '')
                            env[k] = v
        return env

    def get_groupname(self):
        if self.root == ".":
            path = os.getcwd()
        else:
            path = self.root
        return os.path.split(path)[1]

    def as_supervisor(self, user):
        parser = configparser.ConfigParser()
        for name, command in self.programs():
            k = 'program:%s-%s' % (user, name)
            parser.add_section(k)
            parser.set(k, 'user', user)
            parser.set(k, 'directory', '/home/%s' % user)
            parser.set(k, 'environment', ','.join(['='.join(kv) for kv in self.env.items()]))
            parser.set(k, 'stdout_logfile', '/home/%s/log/%s-out.log' % (user, name))
            parser.set(k, 'stderr_logfile', '/home/%s/log/%s-err.log' % (user, name))
            parser.set(k, 'command', command)
            parser.set(k, 'autostart', 'true')
            parser.set(k, 'autorestart', 'true')
            parser.set(k, 'stopsignal', 'QUIT')
        return parser

    def as_configparser(self, concurrency_settings=None):
        """ return a ConfigParser object. It can be used to generate a
gafferd setting file or a configuration file that can be
included. """

        parser = configparser.ConfigParser()
        concurrency_settings = concurrency_settings or {}

        ln = 0
        dconf = OrderedDict()
        for k, v in self.cfg.items():
            cmd, args = self.parse_cmd(v)
            name = "%s:%s" % (self.get_groupname(), k)

            dconf["process:%s" % name] = OrderedDict([("cmd", cmd),
                ("args", " ".join(args)), ("priority", ln),
                ('numprocesses', concurrency_settings.get(k, 1))])
            ln += 1

        parser.read_dict(dconf)
        return parser

    def parse_cmd(self, v):
        args_ = shlex.split(v)
        cmd = args_[0]
        if len(args_) > 1:
            args = args_[1:]
        else:
            args = []
        return cmd, args
