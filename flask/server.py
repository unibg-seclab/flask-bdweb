###############################################################################
# 1. hello world (6 righe)

from flask import Flask

app = Flask(__name__)                        # usare __name__ su pythonanywhere

@app.route('/')
def root():
    return "Hello, world!"        # deve tornare una stringa (il response body)

#app.run(host="0.0.0.0", port=5000)

# SLIDE

# 1b. aggiungere altre route (instradamento)

@app.route('/bye')
def bye():
    return "Goodbye, world!"

# 1c. upload su pythonanywhere

###############################################################################
# 2. utilizzo di template

from flask import render_template

@app.route('/template')
def template():
    return render_template('template.html')

# 2b. far vedere che il template.html nella stessa cartella non va
app.debug = True


# 2c. template variable

from time import time

@app.route('/template_variable')
def template_variable():
    return render_template('template_variable.html', timestamp=time())


# 2d. template if

from random import randint

@app.route('/template_if')
def template_if():
    return render_template('template_if.html', voto=randint(0, 32))


# 2e. template for

todolist = ['wake up', 'prepare Unibg lecture', 'prepare BgLUG slides', 'sleep']

@app.route('/template_for')
def template_for():
    return render_template('template_for.html', todolist=todolist)

###############################################################################
# EXE

# * stampare tabella con prodotto e prezzo
# * stampare free in grassetto se prezzo <= 0

prices = {'strawberry': 2.0, 'lemon': 1.0, 'bitcoin': 2000.0, 'spam': 0}

@app.route('/supermarket')
def supermarket():
    return render_template('supermarket.html', prices=prices)


###############################################################################
# 3. passaggio parametri via get

# SLIDE


@app.route('/hello/<name>')
def hello(name):
    return "hello, %s!" % name

@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    #return a + b              # da convertire a stringa
    return str(a + b)


###############################################################################
# EXE
# * fare una api che restituisca il prezzo del prodotto

prices = {'strawberry': 2.0, 'lemon': 1.0, 'bitcoin': 2000.0, 'spam': 0}

@app.route('/getprice/<product>')
def getprice(product):
    if product in prices:
        return "%s: %.2f €" % (product, prices[product])
    else:
        return "we don't have '%s'" % product


##############################################################################
# 4. passaggio parametri via post

from flask import request

@app.route('/whoareyou', methods=['GET', 'POST'])
def whoareyou():
    if request.method == 'GET':
        return render_template('whoareyou.html')

    if request.method == 'POST':
        name = request.form.get('name')
        return render_template('whoareyou.html', name=name)


###############################################################################
# 5. creare una calcolatrice (form con 2 valori in input e calcola risultato)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    x = int(request.form.get('x', 0))
    y = int(request.form.get('y', 0))
    return render_template('calculator.html', x=x, y=y)

# bonus verificare se valido

###############################################################################
# EXE

notes = []

@app.route('/post_notes', methods=['GET', 'POST'])
def post_notes():
    if request.method == 'POST':
        notes.append(request.form.get('note'))

    return render_template('post_notes.html', notes=notes)


###############################################################################
# EXE

import sqlite3

notesdb = "notes.db"

def init_notes_db(reset=False):
    connection = sqlite3.connect(notesdb)

    if reset:
        connection.execute("DROP TABLE IF EXISTS notes;")

    connection.execute("CREATE TABLE IF NOT EXISTS notes (data VARCHAR)")

    connection.commit()
    connection.close()

init_notes_db()


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    connection = sqlite3.connect(notesdb)
    cursor = connection.cursor()

    if request.method == 'POST':
        note = request.form.get('note')
        cursor.execute("INSERT INTO notes VALUES ('%s')" % note)
        connection.commit()

    cursor.execute("SELECT data FROM notes")
    rows = cursor.fetchall()
    connection.close()

    return render_template('notes.html', rows=rows)


######################################################################
# SECRET NOTES

secretsdb = "secrets.db"

def init_secrets_db(reset=False):
    connection = sqlite3.connect(secretsdb)

    if reset:
        connection.execute("DROP TABLE IF EXISTS secrets;")

    connection.execute("CREATE TABLE IF NOT EXISTS secrets (userid VARCHAR, data VARCHAR)")

    connection.commit()
    connection.close()

init_secrets_db(reset=True)


@app.route('/secrets/<userid>', methods=['GET', 'POST'])
def secrets(userid):
    connection = sqlite3.connect(secretsdb)
    cursor = connection.cursor()

    if request.method == 'POST':
        note = request.form.get('note')
        cursor.execute("INSERT INTO secrets VALUES ('%s', '%s')" % (userid, note))
        connection.commit()

    cursor.execute("SELECT data FROM secrets WHERE userid = '%s'" % userid)
    rows = cursor.fetchall()
    connection.close()

    return render_template('secrets.html', userid=userid, rows=rows)



app.run(host="0.0.0.0", port=5000)