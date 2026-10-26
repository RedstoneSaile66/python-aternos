import setuptools

with open('README.md', 'rt') as readme:
    long_description = readme.read()

setuptools.setup(
    name='python-aternos',
    version='3.0.6',
    author='Andrey @DarkCat09',
    author_email='py@dc09.ru',
    description='An unofficial Aternos API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DarkCat09/python-aternos',
    project_urls={
        'Documentation': 'https://python-aternos.codeberg.page',
        'GitHub': 'https://github.com/DarkCat09/python-aternos',
        'Bug Tracker': 'https://github.com/DarkCat09/python-aternos/issues',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Typing :: Typed',
    ],
    install_requires=[
        'cloudscraper>=1.2.71',
        'Js2Py>=0.74; python_version < "3.12"',
        'lxml>=4.9.3',
        'regex>=2023.6.3',
        'websockets>=11,<16',
    ],
    extras_require={
        'dev': [
            'autopep8==2.0.2',
            'pycodestyle==2.10.0',
            'mypy==1.4.1',
            'pylint==2.17.4',
            'requests-mock==1.11.0',
            'types-requests==2.31.0.1',
        ],
        'pypi': [
            'build==0.10.0',
            'twine==4.0.2',
        ],
        'docs': [
            'mkdocs==1.4.3',
            'mkdocstrings[python]==0.22.0',
        ]
    },
    packages=['python_aternos'],
    package_data={
        'python_aternos': [
            'data/*.js',
            'data/package.json',
            'data/package-lock.json',
        ],
    },
    python_requires=">=3.9",
    include_package_data=True,
)
