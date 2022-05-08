import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='onlyoffice',  
     version='0.0.1',
     author="Géry Casiez",
     author_email="gery.casiez@gmail.com",
     description="Python API for OnlyOffice.",
     long_description=long_description,

     long_description_content_type="text/markdown",
     url="https://github.com/casiez/onlyoffice",
     packages=setuptools.find_packages(),
     install_requires=['requests'],

     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License"
     ],

 )