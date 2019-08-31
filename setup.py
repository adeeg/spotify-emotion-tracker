# thanks https://github.com/navdeep-G/samplemod

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='spotify-emotion-tracker',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Nenivar',
    url='https://github.com/nenivar/spotify-emotion-tracker',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
