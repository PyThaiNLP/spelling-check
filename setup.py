# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
requirements = [
    'pythainlp',
    'sklearn-crfsuite'
]

setup(
    name='pythaispell',
    version='0.1',
    description="Thai Spell Check",
    author='Wannaphong Phatthiyaphaibun',
    author_email='wannaphong@kkumail.com',
    url='https://github.com/wannaphongcom/Thai_Spell_Check',
    packages=['.'],
    package_data={'': ['LICENSE','README.md']},
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='promptpay',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: Implementation'],
)
