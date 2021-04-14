from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import *

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
mysql=MySQL(app)

# Session
app.secret_key = secret

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add-contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cursor = mysql.connection.cursor()
    cursor.execute('insert into contacts (fullname, phone, email) VALUES (%s,%s,%s)', (fullname,phone,email,))
    mysql.connection.commit()
    flash('Contact added successfully')
    return redirect(url_for('index'))

@app.route('/edit/<string:id>')
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cursor.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<string:id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE contacts 
        SET fullname=%s, 
            phone=%s, 
            email=%s 
        WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
    flash('Contact updated successfully')
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Contact Removed successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)