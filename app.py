from flask import Flask, request
import math_stat.stat_fun_v1 as stat_fun_v1
import math_stat.stat_fun_v2 as stat_fun_v2
from database.creation import create_db

app = Flask(__name__)
app.config.from_envvar('STAT_SERVICE_SETTINGS')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/stat', methods=['POST'])
def count_stats():
    array = request.get_json()['array']
    response = stat_fun_v1.count_stats(array)
    return response.to_dict()


if __name__ == '__main__':
    db_path = app.config['DB_FILE']
    constants = {
        'min': app.config['MAX'],
        'max': app.config['MAX'],
    }
    create_db(db_path, list(constants.keys()))
    app.run()
