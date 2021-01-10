from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ib_edavki",
    version="1.3.0",
    py_modules=["ib_edavki"],
    python_requires=">=3",
    entry_points={
        "console_scripts": ["ib_edavki=ib_edavki:main", "ib-edavki=ib_edavki:main"]
    },
    author="Primož Sečnik Kolman",
    author_email="primoz@outlook.com",
)
