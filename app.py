from flask import Flask, request
import numpy as np

import warnings

import math_stat.stat_fun_v1 as stat_fun_v1
import math_stat.check as check

from database.creation import create_db
from database.fill_db import fill_db
from database.search import search_constant

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config.from_envvar('STAT_SERVICE_SETTINGS')
warnings.simplefilter(action='ignore', category=FutureWarning)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/stat', methods=['POST'])
def count_stats():
    try:
        array = np.array(request.get_json()['dataset'], dtype=float)
    except KeyError:
        return "I need array of floats.", 400
    except Exception:
        return "Not correct input.", 400
    db_path = app.config['DB_FILE']
    MIN = search_constant('MIN', db_path)
    MAX = search_constant('MAX', db_path)
    if not check.min_max_check(array, MIN, MAX):
        return f"Values are not in [{MIN};{MAX}]!", 400
    response = stat_fun_v1.count_stats(array)
    return response


if __name__ == '__main__':
    db_path = app.config['DB_FILE']
    constants = [
        ('MIN', app.config['MIN']),
        ('MAX', app.config['MAX']),
    ]
    create_db(db_path, list(map(lambda x: x[0], constants)))
    fill_db(db_path, constants)
    app.run()
