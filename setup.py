from setuptools import setup, find_packages
from pkg.__version__ import __version__

setup(
    name="wgagent",
    version=__version__,
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "wgagent=cli.wgagent:main"
        ]
    },
)
