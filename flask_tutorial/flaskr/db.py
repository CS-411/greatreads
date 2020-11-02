import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


#close_db checks if a connection was created by checking if g.db was set. If the connection exists, it is closed
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


#current_app is another special object that points to the Flask application handling the request
def init_db():
    #get_db returns a database connection, which is used to execute the commands read from the file.
    db = get_db()
    #open_resource() opens a file relative to the flaskr package,
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
