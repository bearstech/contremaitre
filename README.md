Contremaître
============

Build a _supervisord_ conf from a [Procfile](https://devcenter.heroku.com/articles/procfile).

Contremaitre is mix from foreman and [gaffer](https://github.com/benoitc/gaffer).

Inspiration from [this blog post](http://blog.nicolai86.eu/posts/2012-02-25/foreman-and-supervisord)
targeting classical Debian without painful installation.

Test it
-------

Be polite, make a virtualenv

    virtualenv .
    source bin/activate
    python setup.py install

Launch test

    pip install nosetests
    ./bin/nosetests

Use it
------

Move to some folder with a Procfile inside.

    contremaitre worker=2,foo=3

Contrmaitre use the current user to build a supervisor conf in /tmp folder.
Check it, move it to /etc/supervisord/conf.d/ .

Todo
----

 - √ Build a supervisor conf from a Procfile
 - _ Some global parameters
 - _ Debian package
 - _ User can restart its process or managing the number of process


Licence
-------

3 clause BSD licence © 2013 Mathieu Lecarme
