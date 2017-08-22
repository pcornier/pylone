from flask import current_app
from flask import Flask

app = Flask(__name__)

class Command:

    def get_label():
        return ''

    def execute():
        pass
        
    def get_config():
        pass

    def get_script():
        return '# no script'

