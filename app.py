import os
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env
from flask import Flask, render_template, redirect, request,\
                  url_for
from flask_pymongo import PyMongo

app = Flask(__name__)


app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = 'the_perfect_boat'
app.secret_key = os.environ.get('')

mongo = PyMongo(app)


@app.route('/')
def home():
    """Render the home.html page"""
    boats = list(mongo.db.boats.find())
    return render_template('index.html', boats=boats)


@app.route('/add_boat', methods=['GET', 'POST'])
def add_boat():
    if request.method == 'GET':

        return render_template('add_boat.html')

    if request.method == 'POST':
        form = {
            'name': request.form['name'],
            'img': request.form['img'],
            'description': request.form['description'],
            'comments': []
        }
        mongo.db.boats.insert_one(form)
        return render_template('index.html')


@app.route('/add-rating/<boat_id>', methods=['POST'])
def add_rating(boat_id):
    boat = mongo.db.boats.find_one(
                                  {'_id': ObjectId(boat_id)})
    boat['comments'].append([
        request.form['comment'],
        request.form['stars']
    ])

    print(boat)

    mongo.db.boats.update({'_id': ObjectId(boat_id)}, boat)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP", "0.0.0.0"),
            port=int(os.environ.get("PORT", "5000")), 
            debug=True)