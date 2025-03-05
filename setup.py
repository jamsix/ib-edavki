from distutils.core import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="ib_edavki",
    version="1.4.8",
    py_modules=["ib_edavki", "generators.doh_obr"],
    python_requires=">=3.9",
    install_requires=["requests", "certifi>=2024.8.30"],
    entry_points={
        "console_scripts": ["ib_edavki=ib_edavki:main", "ib-edavki=ib_edavki:main"]
    },
    author="Primož Sečnik Kolman",
    author_email="primoz@outlook.com",
)
