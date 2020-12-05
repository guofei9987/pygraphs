import pickle
import sys


def save_db(db, filename='pg.db'):
    sys.setrecursionlimit(10000)
    with open(filename, 'wb') as f:
        pickle.dump(db, f, True)


def load_db(filename='pg.db'):
    with open(filename, 'rb') as f:
        db = pickle.load(f)
    return db
