from setuptools import setup
from os import path

def get_long_description():
    with open(
        path.join(path.dirname(path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

def get_requirements(fn='requirements.txt', nogit=True):
   """Get requirements."""
   if path.exists(fn):
      with open(fn, 'r') as f:
        requirements = f.read().splitlines()
   else:
     requirements = []
   requirements = [r.split()[0].strip() for r in requirements if r and not r.startswith('#')]
   if nogit:
       requirements = [r for r in requirements if not r.startswith('git+')]
   return requirements

requirements = get_requirements()

setup(
    name="ou-jupyter-book-tools",
    packages=['tags2myst', 'jb_utils'],
    version='0.0.4',
    author="Tony Hirst",
    author_email="tony.hirst@gmail.com",
    description="Tools for working with Jupyter books.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        tags2myst=tags2myst.cli:cli
    '''

)
