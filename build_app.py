import sys

sys.setrecursionlimit(1000000)
from setuptools import setup

APP = ['adistools.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': None,
    'includes': ['wx','sys','html','requests','socketio', 'rumps'],
    'excludes': ['numpy','scipy','transformers','torch','gevent','matplotlib','pil','jinja2','werkzeug','flask','jedi','markupsafe','test'],
    'plist': {'LSUIElement': True, }
    }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={
        'py2app': OPTIONS,
        },
    setup_requires=['py2app'],
)