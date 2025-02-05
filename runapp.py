'''App Entrypoint For Gunicorn'''
import os
from app import create_app

from logging import getLogger,basicConfig,DEBUG,getLogger,StreamHandler
from sys import stdout

app = create_app()

    
@app.shell_context_processor

def make_shell_context():
    '''Function to set variable before app start'''
    return {'db': db }

if __name__ == '__main__':
    if not getLogger().hasHandlers():
        stdout_handler = StreamHandler(stream=stdout)
        handlers = [stdout_handler]
        basicConfig(
            level=DEBUG, 
            format='%(asctime)s loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s',
            handlers=handlers
        )
        logger = getLogger('runapp.py')
        
    
        app.run()
