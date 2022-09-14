import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="mmead",
    version="0.0.1",
    author="Chris Kamphuis",
    author_email="chris@cs.ru.nl",
    description="MS MARCO entity annotations and disambiguations",
    url="https://github.com/informagi/mmead",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)