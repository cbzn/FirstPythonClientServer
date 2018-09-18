from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flaskext.mysql import MySQL





app = Flask(__name__)
#app.debug = True

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Init MySQL
mysql = MySQL(app)

database = {}
try:
    db_file = open('db.dat', 'r')
    for register in db_file:
        cells = register.split('%')
        database.update({cells[0]:{'name':cells[1], 'password': cells[2]}})
    db_file.close()
except:pass


Articles = Articles()



@app.route('/')
def index():      # Function name does not mind
    return render_template('home.html')

@app.route('/about')
def about():      # Function name does not mind
    return render_template('about.html')

@app.route('/articles')
def articles():   # Function name does not mind
    return render_template('articles.html', articles = Articles)    

@app.route('/article/<string:id>/')
def article(id):      # Function name does not mind
    return render_template('article.html', id = id) 

@app.route('/login', methods=['GET', 'POST'])
def login():      # Function name does not mind
    if request.method == 'POST':
        #Get form fields
        email = request.form["email"]
        password_candidate = request.form["password"]

        #Create cursor
        #cur = musql.connection.cursor()

        #Get user by username
        #result = cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        if email in database:
            #get stored hash
            #data = cur.fetchone()
            password = database[email]['password']
            name = database[email]['name']

            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('SUCCESSFULL LOGIN')
                session['logged_in'] = True
                session['email'] = email
                session['name'] = name

                flash('Tou are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                app.logger.info('WRONG PASSWORD')
                error = 'Wrong user password'
                return render_template('login.html', error=error)
            #cur.close()
        else:
            app.logger.info('THIS USER EMAIL IS NOT REGISTERED')
            error = 'User email not found'
            return render_template('login.html', error=error)
    return render_template('login.html')    

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

class RegisterForm(Form):
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.hash(str(form.password.data))
        name = form.name.data

        #Create the cursor
        #cur = mysql.connection.cursor()
        

        #Execute query
        #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        database.update({email: {'name': name, 'password':password}})

        db_file = open('db.dat', 'a')
        db_file.write(email +'&'+ name +'&'+ password)
        db_file.close()
        
        #Commit to DB
        #mysql.connection.commit()
        #cur.close()

        flash('You are now registered!', 'success')
        print(database)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        flash('Unauthorized access. Log in', 'danger')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)