import setuptools

MAIN_REQUIREMENTS = ["requests>=2.21.0", "python-dateutil>=2.8.2"]

DEV_REQUIREMENTS = ["python-dotenv==0.19.1", "pre-commit==2.15.0"]

setuptools.setup(
    name="apyauth",
    version="1.0.4",
    license="MIT",
    packages=setuptools.find_packages(),
    description="Handy module for oauth2.0 Authentication.",
    install_requires=MAIN_REQUIREMENTS,
    extras_requires={"tests": DEV_REQUIREMENTS},
)
