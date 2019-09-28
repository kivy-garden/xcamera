import os

from setuptools import find_namespace_packages, setup

from src.kivy_garden.xcamera import version


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


# exposing the params so it can be imported
setup_params = {
    'name': 'kivy_garden.xcamera',
    'version': version.__version__,
    'description': 'Real time Barcode and QR Code scanner Edit',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'author': 'Antonio Cuni',
    'url': 'https://github.com/kivy-garden/xcamera',
    'packages': find_namespace_packages(where='src'),
    'package_data': {
        'kivy_garden.xcamera': ['*.kv'],
        'kivy_garden.xcamera.data': ['*.ttf', '*.wav'],
    },
    'package_dir': {'': 'src'},
    'entry_points': {
        'console_scripts': ['xcamera=kivy_garden.xcamera.main:main'],
    },
    'python_requires': '>=3',
    'install_requires': [
        'kivy',
        'opencv-python',
    ],
}


def run_setup():
    setup(**setup_params)


# makes sure the setup doesn't run at import time
if __name__ == '__main__':
    run_setup()
