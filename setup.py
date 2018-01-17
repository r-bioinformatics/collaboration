import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'svgwrite',
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(
    name='collaboration',
    version='0.01',
    description='R-bioinformatics collaboration',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
    ],
    author='r/bioninformatatics',
    author_email='',
    url='',
    keywords='bioninformatics visualization rna',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = librraries:main',
        ],
    },
)
