import setuptools

setuptools.setup(name = 'oauth2py', 
    version = '0.3',
    packages = setuptools.find_packages(),
    description = 'Handy module for oauth2.0 Authentication.',
    install_requires =[
        'socket',
        'requests',
        'json',
        'random',
        'string',
        'datetime'
        'dateutil',
        'ast',
        'os'
    ])