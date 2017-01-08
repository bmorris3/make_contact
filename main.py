# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template

from utils import query_for_reps, Proof

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def form():
    username = request.form['username']
    aff = request.form['aff']
    street = request.form['street']
    subject = request.form['subject']
    stance = request.form['stance']
    body = request.form['body']

    list_of_reps = query_for_reps(street)

    signature = '\n'.join([username] + [i.strip() for i in street.split(',')])

    proof = Proof(body)
    suggestions = proof.get_suggestions()

    return render_template("output.html",
                           username=username,
                           aff=aff,
                           street=street,
                           subject=subject,
                           stance=stance,
                           body=body,
                           list_of_reps=list_of_reps,
                           signature=signature,
                           suggestions=suggestions)

@app.route('/faq')
def faq():
    return app.send_static_file('faq.html')
    
if __name__ == '__main__':
    app.run()