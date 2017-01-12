# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template

from utils import query_for_reps, Proof, ContactForm

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.data['name']
        title = form.data['title']
        affil = form.data['affil']
        address = form.data['address']
        body = form.data['body']

        list_of_reps = query_for_reps(address)

        signature = name + '\n'
        if len(title) > 1:
            signature = title + ' ' + signature
        if affil:
            signature += affil + '\n'
        signature += '\n'.join([i.strip() for i in address.split(',')])

        proof = Proof(body)
        suggestions = proof.get_suggestions()
        return render_template('index.html', form=form, suggestions=suggestions, 
                               list_of_reps=list_of_reps, signature=signature)
    else:
        return render_template('index.html', form=form)

@app.route('/faq')
def faq():
    return render_template('faq.html')
    
if __name__ == '__main__':
    app.run(debug=True)