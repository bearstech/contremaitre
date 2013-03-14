Contremaître
============

Build a _supervisord_ conf from a [Procfile](https://devcenter.heroku.com/articles/procfile).

Contremaitre is mix from foreman and [gaffer](https://github.com/benoitc/gaffer).

Inspiration from [this blog post](http://blog.nicolai86.eu/posts/2012-02-25/foreman-and-supervisord) targetting classical Debian without painful installation.

Test it
-------

Be polite, make a virtualenv

    virtualenv .
    source bin/activate
    pip install -r requirements.txt

Launch test

    ./bin/nosetests

Licence
-------

3 clause BSD licence © 2013 Mathieu Lecarme
