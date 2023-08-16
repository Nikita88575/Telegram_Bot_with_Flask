from flask_session import Session
from models.users import User, db
from sqlalchemy import inspect, text
from data.config import SECRET_KEY, POSTGERS_URI, DEBUG, FLASK_HOST
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGERS_URI
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)
db.init_app(app)

# Check is user authenticated
def is_authenticated():
    return session.get('authenticated', False)

# Redirect user if user isn`t authenticated  
@app.before_request
def require_authentication():
    if request.endpoint not in ['login', 'logout', 'registration', 'static'] and not is_authenticated():
        return redirect(url_for('login'))

@app.get('/')
def index():
    return redirect(url_for('login'))

# @app.route('/registration', methods=['GET', 'POST'])
# def registration():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Check if the username is already taken
#         existing_user = User.query.filter_by(username=str(username)).first()
#         if existing_user:
#             flash('Username already exists', 'error')
#             return redirect(url_for('registration'))

#         # Create a new user and set the password
#         new_user = User(username=str(username))
#         new_user.set_password(str(password))

#         # Trying add user to DB
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Registration successful', 'success')
#             session['authenticated'] = True
#             return redirect(url_for('tables'))
#         except Exception as e:
#             db.session.rollback()
#             flash('Registration failed', 'error')
#             return redirect(url_for('registration'))

#     return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('authenticated', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=str(username)).first()

        if user and user.check_password(str(password)):
            flash('Login successful', 'success')
            # Set the authenticated session flag
            session['authenticated'] = True
            return redirect(url_for('tables'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.get('/logout')
def logout():
    # Delete session
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.get('/tables')
def tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return render_template('tables.html', tables=tables)

@app.get('/tables/<table_name>')
def table_details(table_name):
    inspector = inspect(db.engine)
    table_columns = inspector.get_columns(table_name)
    query = text(f'SELECT * FROM "{table_name}"')
    table_data = db.session.execute(query).fetchall()
    return render_template('table_details.html', table_name=table_name, table_columns=table_columns, table_data=table_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=DEBUG, host='0.0.0.0')