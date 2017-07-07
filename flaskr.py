# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

#The next couple lines will create the actual application instance and initialize

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#allows for easy connetion to a specific database
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

#create a database connection for the current context, and successive calls will return the already established connection
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#disconnect from database
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
		
#schema that shows database how to store data
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
	
#The view function will pass the entries to the show_entries.html template and return the rendered one:
@app.route('/')
def submit_entries():
    db = get_db()
    cur = db.execute('select my, make, model, trim, body_style, drivetrain, transmission, vin, mileage from entries order by id desc limit 5')
    entries = cur.fetchall()
    return render_template('sellerui.html', entries=entries)

#add new entry
@app.route('/add', methods=['POST'])
def add_entry():
	db = get_db()
	db.execute('insert into entries (my, make, model, trim, body_style, drivetrain, transmission, vin, mileage) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
	             [request.form['my'], request.form['make'], request.form['model'],request.form['trim'],request.form['body_style'],request.form['drivetrain'] ,request.form['transmission'],request.form['vin'], request.form['mileage']])
	db.commit()
	flash('Vehicle submitted')
	return redirect(url_for('submit_entries'))


#add more pages
@app.route('/buyerui')
def show_buyerui():
	db = get_db()
	cur = db.execute('select my, make, model, trim, body_style, drivetrain, transmission, vin, mileage from entries order by id desc limit 50')
	entries = cur.fetchall()
	return render_template('buyerui.html', entries=entries)
@app.route('/home')
def show_home():
    return render_template('home.html')
