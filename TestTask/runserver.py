from os import environ
from TestTask import app, db
from TestTask.models import User, Category, Commodity, BoughtCommodity

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Category': Category, 'Commodity': Commodity, 'BoughtCommodity': BoughtCommodity}

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
