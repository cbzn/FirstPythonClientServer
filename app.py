from flask import Flask, request, render_template, flash, redirect, url_for, session

from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
#from flaskext.mysql import MySQL

def start():

    app = Flask(__name__)
    #app.debug = True

    #Config MySQL
    #app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_USER'] = 'root'
    #app.config['MYSQL_PASSWORD'] = '123456'
    #app.config['MYSQL_DB'] = 'myflaskapp'
    #app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    #Init MySQL
    #mysql = MySQL(app)

    database = {}
    try:

        db_file = open('db.dat', 'r')
        for reg in db_file:
            cells = reg.split('&&&&')
            database.update({cells[0]:{'name':cells[1], 'password': cells[2][:-1]}})
        db_file.close()
    except:pass
    

    Nastran_cases = [
        {'id': 1,
        'name': 'Article 1',
        'user': 'text1 text text text',
        'date': '17September2018',
        'state': 'Running'},
        {'id': 2,
        'name': 'Article 2',
        'user': 'text2 text text text',
        'date': '17September2018',
        'state': 'Waiting'},     
        {'id': 2,
        'name': 'Article 2',
        'user': 'text2 text text text',
        'date': '17September2018',
        'state': 'Waiting'},   
        {'id': 2,
        'name': 'Article 2',
        'user': 'text2 text text text',
        'date': '17September2018',
        'state': 'Failed'},            
        {'id': 2,
        'name': 'Article 2',
        'user': 'text2 text text text',
        'date': '17September2018',
        'state': 'Success'},                            
    ]

    class RegisterForm(Form):
        name = StringField('Name', [validators.DataRequired()])
        email = StringField('email', [validators.Length(min=6, max=50)])
        password = PasswordField('Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords do not match')
            ])
        confirm = PasswordField('Confirm Password')

    # ROUTING
    @app.route('/nastran_manager') # Decorator. Links a pythonfunction to a route 
    def nastran():
        return render_template( 'nastran_manager.html', nastran_cases = Nastran_cases, session=session)    

    @app.route('/') #Root directory
    @app.route('/home')
    @app.route('/<word>')
    def index(word = None):
        if word:
            flash('Wrong URL!', 'danger')
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/article/<string:id>/') #id is the name (expected string) of the variable that will enter the function below
    def article(id): 
        return render_template('article.html', id = id) 

    # The second parameter establishes that this url is able to handle GET and POST methods
    @app.route('/login', methods=['GET', 'POST']) 
    def login():
        if request.method == 'POST': #Get FORM fields
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
                    app.logger.info('----SUCCESSFULL LOGIN')
                    session['logged_in'] = True
                    session['email']     = email
                    session['name']      = name

                    flash('Logged in', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    app.logger.info('----WRONG PASSWORD')
                    error = 'Wrong user password'
                    return render_template('login.html', error=error)
                #cur.close()
            else:
                app.logger.info('----THIS USER EMAIL IS NOT REGISTERED')
                error = 'User email not found'
                return render_template('login.html', error=error)
        return render_template('login.html')    

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged out', 'success')
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            email = form.email.data.lower()
            password = sha256_crypt.hash(str(form.password.data))
            name = form.name.data

            #Create the cursor
            #cur = mysql.connection.cursor()

            #Execute query
            #cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
            if email in database:
                flash('This user already exists!', 'danger')
                return redirect(url_for('register'))
            else:
                database.update({email: {'name': name, 'password':password}})
                db_file = open('db.dat', 'a')
                db_file.write(email +'&&&&'+ name +'&&&&'+ password +'\n')
                db_file.close()
                session['logged_in'] = True
                session['email'] = email
                session['name'] = name  
            flash('You are now registered', 'success')
            return redirect(url_for('dashboard'))
            #Commit to DB
            #mysql.connection.commit()
            #cur.close()

            

        return render_template('register.html', form=form)

    @app.route('/dashboard')
    def dashboard():
        if 'logged_in' in session:
            return render_template('dashboard.html')
        else:
            flash('Unauthorized access. Log in', 'danger')
            return redirect(url_for('login'))
    return app

#To run this file when we run it directly, not when we import this file
if __name__ == '__main__':
    app = start()
    app.secret_key = 'secret123'

    app.run(debug = True)