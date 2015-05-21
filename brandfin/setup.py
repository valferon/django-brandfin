import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name='django-brandfin',
    version='0.1',
    packages = find_packages(),
    author = "Valentin Feron",
    author_email = "valferon@gmail.com",
    description = "A package to create reports from existing databases by running sql queries against them. Modified version of SQL-EXPLORER",
    url = "",
    include_package_data = True, requires=['sqlalchemy', 'sqlalchemy']
)

