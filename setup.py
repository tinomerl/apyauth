import setuptools

setuptools.setup(name = 'oauth2py', 
    version = '0.3',
    packages = setuptools.find_packages(),
    description = 'Handy module for oauth2.0 Authentication.',
    install_requires =[
        'requests>=2.21.0'
    ])