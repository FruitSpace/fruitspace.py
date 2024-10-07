from setuptools import setup

setup(
    name='fruitspace.py',
    version='1.0',
    description='SDK for working with FruitSpace\'s databases',
    author='whoisamyy',
    author_email='egegegg002@gmail.com',
    packages=['fruitspace'],
    install_requires=['requests','setuptools'],
    package_dir={'': 'src'},
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)