from distutils.core import setup

setup(name='Contremaitre',
      version='0.1',
      description='Build supervisord conf from Procfile',
      author='Mathieu Lecarme',
      author_email='mlecarme@bearstech.com',
      url='https://github.com/bearstech/contremaitre',
      packages=['contremaitre'],
      package_dir={'': 'src'},
      scripts=['scripts/contremaitre']
      )
