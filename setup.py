from setuptools import setup

long_description = open('README.rst').read()

setup(
    name="django-googleauth",
    version='2.1',
    packages=["googleauth"],
    description="OAuth 2.0 authentication for Google and Google Apps accounts",
    url="https://github.com/jcarbaugh/django-googleauth",
    author="Jeremy Carbaugh",
    author_email="jcarbaugh@gmail.com",
    license='BSD',
    long_description=long_description,
    platforms=["any"],
    install_requires=[
        "PyJWT==0.4.1",
        "requests==2.5.1",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
