from setuptools import setup

setup(
    name='ghost-cli',
    version='0.1.59',
    description='A Python Client for the Ghost Admin API',
    url='https://github.com/milnomada/ghost-cli',
    author='Milnomada.org',
    author_email='info@milnomada.io',
    license='GNU Public',
    packages=['ghost_cli'],
    install_requires=[
        'pyjwt>=2.4.0',
        'requests>=2.22.0',
        'python-slugify>=6.0.0'                     
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
