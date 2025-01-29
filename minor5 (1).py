from flask import Flask, render_template,request, redirect,flash,url_for,session

# Create a Flask app

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'jeet'

# Define a route and a view function
import psycopg2

try:
    mycon = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="1234",
        port="5432",
        database="newDB"
    )
    print("Connection established successfully!")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")


cursor = mycon.cursor()


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS student(useremail varchar(255), password varchar(255))''')
    mycon.commit()


def insert_user(use, paw):
    cursor.execute("INSERT INTO student(useremail, password) VALUES (%s, %s)", (use, paw))
    mycon.commit()


@app.route('/login.html', methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
        
        # create_table()
        #  insert_user(email, password)
    cursor = mycon.cursor()
    email = request.form.get('email')
    password = request.form.get('password')
       # Check if username and password match
    cursor.execute("SELECT * FROM student WHERE useremail = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    if user:
              session['email'] = email
              flash('Login successful!', 'success')
              return redirect('/')
    else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html')
       
    

@app.route('/sign-up.html', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
       email2 = request.form['email']
       password2= request.form['password']
       create_table()
       insert_user(email2, password2)
    cur = mycon.cursor()
    email2 = request.form.get('email')
    password2 = request.form.get('password')
        # Check if username already exists
    cur.execute("SELECT * FROM student WHERE useremail = %s", (email2,))
    if cur.fetchone():
        flash('email already exists. Please choose a different one.', 'error')
        return redirect('/')
    else:
        # Insert the new user into the database
        cur.execute("INSERT INTO student (useremail, password) VALUES (%s, %s)", (email2, password2))
        mycon.commit()
        flash('Signup successful! Please login.', 'success')
        return render_template('login.html')


    




@app.route('/')
def second():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)