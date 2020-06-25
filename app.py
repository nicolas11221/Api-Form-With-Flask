
from flask import Flask, render_template, request, url_for, redirect

#Importamos La Base De Datos
from flask_mysqldb import MySQL

app = Flask(__name__)

#Importamos La Configuracion De MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_contacts'
#Inicializamos La Configuracion De Bdd
mysql = MySQL(app)

@app.route('/Index')
def Index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def Contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (full_name, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email))
        mysql.connection.commit()

        return redirect(url_for('Index'))

@app.route('/edit')
def EditContact():
    return 'Edit Contact'


@app.route('/delete')
def DeleteContact():
    return 'Delete Contact'








if __name__ == '__main__':
    app.run(port = 8080 , debug = True)