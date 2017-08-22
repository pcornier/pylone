from flask import current_app
from flask import Flask

from commands.command import Command

app = Flask(__name__)

class RemoveDuplicates(Command):

    def get_label():
        return 'Remove duplicates'

    def execute():
        current_app._df.drop_duplicates(inplace=True)
        
    def get_script():
        return 'df.drop_duplicates(inplace=True)'

