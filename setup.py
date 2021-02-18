
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = 'YAPO e+ - a porn organizer written in Python that will help you organize your porn clips. Selective automatic management or manual curation, or a mix of both.'

setup(
    long_description=readme,
    description='YAPO - Yet Another Porn Organizer - Extended+',
    name='YAPO',
    version='0.7.6.4',
    packages=['YAPO', 'videos', 'configuration', 'utils'],
    package_dir={"YAPO": ""},
    package_data={},
    scripts=['yapo.py', 'manage.py', 'yapo-maintenance.py'],
    python_requires='>=3.7',
    install_requires=['asgiref>=3.2.10', 'beautifulsoup4>=4.9.2', 'colorama>=0.4.3', 'dj_static', 'django==3.1.6', 'django-autocomplete-light==3.5.1', 'django-extensions==3.0.9', 'django-mptt==0.11.0', 'djangorestframework==3.12.1', 'dload>=0.6', 'html5lib>=1.1', 'jinja2>=2.11.2', 'numpy>=1.19.2', 'parsedatetime>=2.6', 'pillow>=7.2.0', 'pillow-pil>=0.1.dev0', 'psutil>=5.7.2', 'pypiwin32>=223; platform_system == "Windows"', 'pywin32>=228; platform_system == "Windows"', 'pywin32-ctypes>=0.2.0; platform_system == "Windows"', 'python-dateutil>=2.8.1', 'pyyaml>=5.3.1', 'requests>=2.24.0', 'selenium>=3.141.0', 'static-ranges', 'texttable>=1.6.3', 'tmdbsimple==2.6.6', 'waitress==1.4.4', 'webencodings>=0.5.1', 'zipp>=3.2.0'],
)
