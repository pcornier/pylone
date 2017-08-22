from flask import Flask
from flask_socketio import SocketIO
from flask import current_app
from flask import render_template

import commands

import pkgutil
import inspect
import pandas as pd
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def main():
    return render_template('main.html')

def refresh():
    cols = []
    for name in current_app._df.columns.values:
        cols.append({'id': name, 'header': name})
    socketio.emit('set_columns', cols)
    
    records = current_app._df.head().fillna('NaN').to_dict('record')
    socketio.emit('set_records', json.dumps(records))
    
def update_stack():
    socketio.emit('update_stack', json.dumps(current_app._stack))

def update_trans_list():
    trans = []
    for com in commands.__all__:
        if com == 'Command':
            continue
        cls = getattr(commands, com)
        trans.append({'name': com, 'label': cls.get_label()})
    socketio.emit('update_trans_list', trans)

@socketio.on('ready')
def ready():
    current_app._stack = []
    current_app._script = []
    current_app._df = pd.DataFrame()
    add_transform({'id': 1, 'command': 'LoadCSV', 'selection': {'file': '../test_with_rep.csv', 'sep': ';'}})
    update_trans_list()
    refresh()

@socketio.on('add_transform')
def add_transform(data):
    print(commands.__all__)
    cls = getattr(commands, data['command'])
    cls.execute(data['selection'])
    current_app._stack.append(data)
    current_app._script.append(cls.get_script(data['selection']))
    update_stack()

@socketio.on('history')
def history(id=-1):
    current_app._df = pd.DataFrame()
    for trans in current_app._stack:
        cls = getattr(commands, trans['command'])
        cls.execute(trans['selection'])
        # globals()[trans['command']](trans['selection'])
        if int(trans['id']) == int(id):
            break
    refresh()

@socketio.on('rem_transform')
def rem_transform(id):
    current_app._stack[:] = [t for t in current_app._stack if int(t['id']) != int(id)]
    history()
    update_stack()

def load_csv(selection):
    current_app._df = pd.read_csv(selection['file'], sep=selection['sep'])
    return 'df = pd.read_csv("' + selection['file'] + '", sep="' + selection['sep'] + '")'

def remove_columns(selection):
    cols = [col['column'] for col in selection]
    current_app._df = current_app._df.drop(cols, axis=1)
    refresh()
    return 'df = df.drop(["' + '", "'.join(cols) + '"], axis=1)'

def remove_duplicates(selection):
    current_app._df.drop_duplicates(inplace=True)
    refresh()
    return 'df.drop_duplicates(inplace=True)'

if __name__ == '__main__':
    socketio.run(app)


