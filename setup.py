from distutils.core import setup

long_description = open('README.md').read()

setup(
    name="django-googleauth",
    version='0.1',
    py_modules=["googleauth"],
    description="OpenID authentication for sunlightfoundation.com accounts",
    author="Jeremy Carbaugh",
    author_email = "jcarbaugh@sunlightfoundation.com",
    license='BSD',
    long_description=long_description,
    platforms=["any"],
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
