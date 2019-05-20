import setuptools

setuptools.setup(name = 'authpy', 
    version = '0.3.2',
    license = 'MIT',
    packages = setuptools.find_packages(),
    description = 'Handy module for oauth2.0 Authentication.',
    install_requires =[
        'requests>=2.21.0'
    ])
