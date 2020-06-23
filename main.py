from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

f = open('config.json', 'r')
params = json.load(f)['params']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# defines the database table
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    comment = db.Column(db.String(120))

@app.route('/', methods=['GET', "POST"])
def index():
    details = Contact.query.all()
    return render_template('index.html', details=details)

@app.route('/delete/<string:sno>', methods =['GET', 'POST'])
def delete(sno):
    detail = Contact.query.filter_by(sno=sno).first()
    db.session.delete(detail)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<string:sno>', methods = ['GET', 'POST'])
def edit(sno):
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        comment = request.form.get('comment')

        if sno == '0':
            data = Contact(fname=fname, lname=lname, email=email, comment=comment)
            db.session.add(data)
            db.session.commit()
        else:
            # for fetching contacts details
            data = Contact.query.filter_by(sno=sno).first()
            data.fname = fname
            data.lname = lname
            data.email = email
            data.comment = comment
            db.session.commit()
            return redirect('/edit/'+sno)
    data = Contact.query.filter_by(sno=sno).first()
    return render_template("edit.html", data=data)


@app.route('/contact', methods=['GET', "POST"])
def contact():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        comment = request.form.get('comment')
        entry = Contact(fname=fname, lname=lname, email=email, comment=comment)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    return render_template('contact.html', params=params)

@app.route('/home')
def home():
    name = 'Shubham'
    return render_template('home.html', creator=name)

app.run(debug=True)