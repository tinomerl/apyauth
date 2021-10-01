import setuptools

MAIN_REQUIREMENTS = ["requests>=2.21.0", "python-dateutil>=2.8.2"]

setuptools.setup(
    name="apyauth",
    version="1.0.0",
    license="MIT",
    packages=setuptools.find_packages(),
    description="Handy module for oauth2.0 Authentication.",
    install_requires=[MAIN_REQUIREMENTS],
)
