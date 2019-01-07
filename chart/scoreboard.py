#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, redirect
from verifier import make_flag
from database import *
import requests

app = Flask(__name__)
app.debug = False


@app.route('/')
def index():
    return render_template('scoreboard.html', accounts=Account.select())


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        try:
            url = request.form['url']
            url = url.strip('https://').strip('http://')

            if not url.endswith('.pythonanywhere.com'):
                return render_template('answer.html', answer='URL must be on the pythonanywhere.com domain')

            try:
                response = requests.get('http://%s' % url)
                response.raise_for_status()
            except:
                return render_template('answer.html', answer='YOUR website does not seem to be up.')

            account = Account(url=url)
            account.save()
            return redirect(url_for('index'))

        except:
            return 'Invalid registration'
            return render_template('answer.html', answer='Invalid registration.')

    if request.method == 'GET':
        return render_template('register.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        try:
            url = request.form['url']
            flag = request.form['flag']

            url = url.strip('https://').strip('http://')

            if not any(flag == make_flag(account) for account in Account.select()):
                return render_template('answer.html', answer='INVALID FLAG')


            account = Account.get(Account.url == url)
            if any(flag == captured_flag.flag for captured_flag in account.flags):
                return render_template('answer.html', answer='already captured')

            else:
                new_flag = Flag(flag=flag, account=account)
                new_flag.save()

                account.points += 10
                account.save()

                return render_template('answer.html', answer='you got a new flag!')

        except KeyboardInterrupt as e:
            pass

        return render_template('answer.html', answer='Invalid submission')

    if request.method == 'GET':
        return render_template('send.html')


app.run(host='0.0.0.0', port=8000)
