
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify

#Importamos La Base De Datos
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySql Connection
#Importamos La Configuracion De MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_contacts'
#Inicializamos La Configuracion De Bdd
mysql = MySQL(app)

# Guardar dentro de la memoria de la app
# Settings
app.secret_key = 'mysecreatkey'

@app.route('/Index')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts = data)


#GET
@app.route('/getContacto')
def getContactos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return jsonify({"": data})

@app.route('/getContacto/<string:full_name>')
def getContacto(full_name):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)

    # contactsFound = [contact for contact in contacts if contact['full_name'] == full_name]
    # if (len(contactsFound) > 0):
    #     return jsonify({"Product": contactsFound[0]})
    # return jsonify({"message": "Product Not Found"})


@app.route('/add', methods=['POST'])
def Contact():
    if request.method == 'POST':
        fullname = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (full_name, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added Succesessfully')
        return redirect(url_for('Index'))
        



@app.route('/edit/<id>')
def EditContact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('editContact.html', contact = data[0])




@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET full_name = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (full_name, phone, email, id))
        mysql.connection.commit()
    flash('Contact Update Successfully :D')
    return redirect(url_for('Index'))



@app.route('/delete/<string:id>')
def DeleteContact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))







if __name__ == '__main__':
    app.run(port = 8080 , debug = True)