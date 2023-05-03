import setuptools

setuptools.setup(
    name="mmead",
    version="0.1.0",
    author="Chris Kamphuis",
    author_email="chris@cs.ru.nl",
    description="MS MARCO entity annotations and disambiguations",
    url="https://github.com/informagi/mmead",
    packages=setuptools.find_packages(),
    install_requires=['tqdm', 'numpy', 'duckdb'],
    python_requires=">=3.6"
)
