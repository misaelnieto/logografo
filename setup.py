from setuptools import setup, find_packages

version = '0.0'

setup(name='logografo',
      version=version,
      description="Grapher app for history events.",
      long_description="""\
      Logografo is a grok app that lets you record history events in a 
      database (grouped by 'bundles') so you can compare events by 
      visualizing them in a timeline in your browser.
""",
      # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Framework :: Zope3",
          "Framework :: ZODB",
          "Framework :: Paste",
          "Framework :: Buildout",
          "Intended Audience :: Education",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Natural Language :: English",
          "Natural Language :: Esperanto",
          "Natural Language :: Spanish",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
          "Topic :: Sociology :: History",
          
          ],
      keywords="history timeline grapher",
      author="Noe Nieto",
      author_email="nnieto@noenieto.com",
      url="http://github.com/tzicatl/logografo",
      license="GPL",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        'grokui.admin',
                        'fanstatic',
                        'zope.fanstatic',
                        'grokcore.startup',
                        # Add extra requirements here
                        ],
      entry_points={
          'fanstatic.libraries': [
              'logografo = logografo.resource:library',
          ]
      })
