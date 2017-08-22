from flask import current_app
from flask import Flask
import pandas as pd

from commands.command import Command

app = Flask(__name__)

class LoadCSV(Command):

    def get_label():
        return 'Load CSV'

    def execute(selection):
        current_app._df = pd.read_csv(selection['file'], sep=selection['sep'])
    
    def get_script(selection):
        return 'df = pd.read_csv("' + selection['file'] + '", sep="' + selection['sep'] + '")'
