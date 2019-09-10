"""
Creates a distribution alias that just installs kivy_garden.xcamera.
"""
from setuptools import setup

from setup import setup_params

setup_params.update({
    'install_requires': ['kivy_garden.xcamera'],
    'name': 'xcamera',
})


setup(**setup_params)
