from setuptools import setup, find_packages, Command
import os

with open("requirements.txt") as req:
    requirements=req.readlines()

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


with open("README.md","r") as readme:
    long_description=readme.read()

setup(
    name="cellsnake",
    version="0.2.0",
    packages=find_packages(exclude=('tests*','testing*')),
    long_description=long_description,
    long_description_content_type="text/markdown",
    #extras_require={"dev":["pytest>=3.7"]},
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['cellsnake=cellsnake.command_line:main'],
    },
    #data_files={"meta":["*.tsv"]},
    #package_data={"workflow" : ["workflow/Snakefile","workflow/rules/*.smk"]},
    #data_files=[("mirmachine",["meta/cms/proto/*.CM"])],
    # metadata to display on PyPI
    author="Sinan U. Umu",
    author_email="sinanugur@gmail.com",
    description="cellsnake",
    keywords="scRNA single-cell RNA analysis",
        cmdclass={
        'clean': CleanCommand,
    },
    url="https://github.com/sinanugur/cellsnake",   # project home page, if any
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Topic :: Scientific/Engineering :: Bio-Informatics'

    ]

    # could also include long_description, download_url, etc.
)
