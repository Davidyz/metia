import setuptools
import os


if os.path.isfile("README.md"):
    with open("README.md", encoding="utf8") as fin:
        long_description = fin.read()
else:
    long_description = ""

requirements = []
if os.path.isfile("requirements"):
    with open("requirements.txt") as fin:
        requirements.append(i.replace("\n", "") for i in fin.readlines())

setuptools.setup(
    name="metia",
    version="0.2",
    author="David Yu",
    author_email="hzjlyz@gmail.com",
    description="A tool to parse and extract audio metadata.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Davidyz/metia",
    project_urls={"Bug Tracker": "https://github.com/Davidyz/metia/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Multimedia",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requirements,
)
