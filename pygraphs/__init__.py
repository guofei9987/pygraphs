from .pygraphs_base import *
from .tools import load_db, save_db

__version__ = '0.0.1'


def start():
    print('''
    pygraphs import successfully,
    version: {version}
    Author: Guo Fei,
    Email: guofei9987@foxmail.com
    repo: https://github.com/guofei9987/pygraphs,
    documents: https://github.com/guofei9987/pygraphs
    '''.format(version=__version__))
