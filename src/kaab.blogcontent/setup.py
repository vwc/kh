from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='kaab.blogcontent',
      version=version,
      description="A archetypes based package containing basic blog content types",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Vorwaerts Werbung GbR',
      author_email='cb@vorwaerts-werbung.de',
      url='http://www.vorwaerts-werbung.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['kaab'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
