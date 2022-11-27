from setuptools import setup

setup(
    name='ghost-cli',
    version='0.1.0',    
    description='A Python Ghost Client ',
    url='https://github.com/milnomada/ghost-cli',
    author='Milnomada.org',
    author_email='info@milnomada.io',
    license='BSD 2-clause',
    packages=['ghost-cli'],
    install_requires=[
        'pyjwt>=2.6.0',
        'requests>=2.28.1',
        'python-slugify>=7.0.0'                     
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
