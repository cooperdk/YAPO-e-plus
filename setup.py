from setuptools import setup

setup(
    name="YAPO e+",
    version="0.8.0",
    description="YAPO - Yet Another Porn Organizer - Extended+",
    author="CooperDK",
    packages=["yapo-eplus'],
    install_requires=['chardet==3.0.4', 'certifi>=2020.6.20', 'urllib3==1.24.3',
        'Django==3.0.7', 'django-autocomplete-light==3.5.1', 'django-extensions==2.2.9',
        'django-mptt==0.11.0', 'djangorestframework==3.11.0', 'dj_static', 'asgiref>=3.2.10', 'static_ranges',
        'beautifulsoup4>=4.5.0', 'html5lib>=1.0.1', 'requests==2.20.0', 'webencodings>=0.5.1', 'tmdbsimple==2.2.0',
        'pypiwin32>=223; platform_system == "Windows"', 'pywin32>=227; platform_system == "Windows"',
        'pywin32-ctypes>=0.2.0; platform_system == "Windows"', 'Pillow>=7.1.2', 'Pillow-PIL>=0.1.dev0',
        'numpy>=1.14.4', 'jinja2>=2.11.2', 'texttable>=1.6.2', 'python-dateutil>=2.5.3', 'parsedatetime>=2.6',
        'selenium>=3.141.0', 'psutil>=5.7.0', 'PyYAML~=5.3.1', 'setuptools~=46.4.0', 'colorama>=0.4.3',
        'dload>=0.6']
)

