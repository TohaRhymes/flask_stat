import warnings

from flask import Flask, request
import numpy as np

import math_stat.check as check
import math_stat.stat_fun_v3 as stat_fun_v3

from database.creation import create_db
from database.fill_db import fill_db
from database.search import search_constant
from math_stat.stat_fun_v3 import generate

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config.from_envvar('STAT_SERVICE_SETTINGS')
warnings.simplefilter(action='ignore', category=FutureWarning)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/stat', methods=['POST'])
def count_stats():
    DATASET = 'dataset'
    try:
        array = np.array(request.get_json()[DATASET], dtype=float)
    except KeyError:
        return "I need array of floats.", 400
    except Exception:
        return "Not correct input.", 400
    db_path = app.config['DB_FILE']
    MIN = search_constant('MIN', db_path)
    MAX = search_constant('MAX', db_path)
    if not check.min_max_check(array, MIN, MAX):
        return f"Values are not in [{MIN};{MAX}]!", 400
    response = stat_fun_v3.count_stats(array)
    return response


@app.route('/stat_v2', methods=['POST'])
def count_stats_v2():
    DB_PATH = app.config['DB_FILE']
    DATASET = 'dataset'
    AUTOCORR = 'autocorrelation_shift'
    CONFIDENCE = 'confidence_level'

    autocorr = None
    confidence = None
    req = request.get_json()

    evth_correct = True
    errors = ["Invalid data:"]
    try:
        array = np.array(req[DATASET], dtype=float)
        if len(array) <= 1:
            evth_correct = False
            errors.append("Array's length should be more than 2.")
    except KeyError:
        evth_correct = False
        errors.append("I need array of floats.")
    except Exception:
        evth_correct = False
        errors.append("Not correct `array` input.")
    MIN = search_constant('MIN', DB_PATH)
    MAX = search_constant('MAX', DB_PATH)
    if evth_correct and not check.min_max_check(array, MIN, MAX):
        evth_correct = False
        errors.append(f"Values are not in [{MIN};{MAX}]!")

    try:
        if AUTOCORR in req:
            autocorr = req[AUTOCORR]
        if autocorr:
            autocorr = int(autocorr)
            if not 1 <= autocorr <= len(array) - 2:
                evth_correct = False
                errors.append("Autocorrelation step should be in [1;n-2].")
    except Exception:
        evth_correct = False
        errors.append("Not correct `autocorr` input.")

    try:
        if CONFIDENCE in req:
            confidence = req[CONFIDENCE]
        if confidence:
            confidence = float(confidence)
            if not 0 <= confidence <= 1:
                evth_correct = False
                errors.append("Confidence interval should be in [0;1].")
    except Exception:
        evth_correct = False
        errors.append("Not correct `confidence` input.")

    if not evth_correct:
        return "\n".join(errors), 400

    response = stat_fun_v3.count_stats(array, confidence=confidence, autocorr=autocorr)
    return response


@app.route('/stat_v3', methods=['POST'])
def count_stats_v3():
    DB_PATH = app.config['DB_FILE']
    DATASET = 'dataset'
    AUTOCORR = 'autocorrelation_shift'
    CONFIDENCE = 'confidence_level'
    EQUAL = 'equal_dataset'

    autocorr = None
    confidence = None
    equal = None
    req = request.get_json()

    evth_correct = True
    errors = ["Invalid data:"]
    try:
        array = np.array(req[DATASET], dtype=float)
        if len(array) <= 1:
            evth_correct = False
            errors.append("Array's length should be more than 2.")
    except KeyError:
        evth_correct = False
        errors.append("I need array of floats.")
    except Exception:
        evth_correct = False
        errors.append("Not correct `array` input.")
    MIN = search_constant('MIN', DB_PATH)
    MAX = search_constant('MAX', DB_PATH)
    if evth_correct and not check.min_max_check(array, MIN, MAX):
        evth_correct = False
        errors.append(f"Values are not in [{MIN};{MAX}]!")

    try:
        if AUTOCORR in req:
            autocorr = req[AUTOCORR]
        if autocorr:
            autocorr = int(autocorr)
            if not 1 <= autocorr <= len(array) - 2:
                evth_correct = False
                errors.append("Autocorrelation step should be in [1;n-2].")
    except Exception:
        evth_correct = False
        errors.append("Not correct `autocorr` input.")

    try:
        if CONFIDENCE in req:
            confidence = req[CONFIDENCE]
        if confidence:
            confidence = float(confidence)
            if not 0 <= confidence <= 1:
                evth_correct = False
                errors.append("Confidence interval should be in [0;1].")
    except Exception:
        evth_correct = False
        errors.append("Not correct `confidence` input.")

    try:
        if EQUAL in req:
            equal = req[EQUAL]
        if equal:
            equal = int(equal)
            if equal < 1:
                evth_correct = False
                errors.append("Equal should should be int more than 0.")
    except Exception:
        evth_correct = False
        errors.append("Not correct `equal` input.")

    if not evth_correct:
        return "\n".join(errors), 400

    response = stat_fun_v3.count_stats(array, confidence=confidence, autocorr=autocorr)
    if equal:
        response.update({"equal_dataset": generate(response, equal).tolist()})
    return response


if __name__ == '__main__':
    DB_PATH = app.config['DB_FILE']
    constants = [
        ('MIN', app.config['MIN']),
        ('MAX', app.config['MAX']),
    ]
    create_db(DB_PATH, list(map(lambda x: x[0], constants)))
    fill_db(DB_PATH, constants)
    app.run()
