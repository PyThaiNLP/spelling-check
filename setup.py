# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
requirements = [
    'pythainlp>=3.1',
    'sklearn-crfsuite'
]
with open("READ.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name='thaispellcheck',
    version='0.2',
    description="Thai Spell Check",
    author='Wannaphong Phatthiyaphaibun',
    author_email='wannaphong@yahoo.com',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/pythainlp/Thai_Spell_Check',
    packages=find_packages(),
    package_data={'thaispellcheck': ['sp.model']},
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
