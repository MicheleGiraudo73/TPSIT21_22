import flask
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id':0,
     'title':'Il nome della Rosa',
    'author':'Umberto Eco',
    'year_published':'1980'},
    {'id':1,
     'title':'Il problema dei tre corpi',
    'author':'Liu Xin',
    'year_published':'2008'},
    {'id':2,
     'title':'Fondazione',
    'author':'Isaac Asimov',
    'year_published':'1951'}
]

@app.route('/',methods=['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"


#qua si mettono gli api -> api/v1 -> v1 versione
@app.route('/api/v1/resources/books/all',methods=['GET'])
def api_all():
    return jsonify(books)

app.run()
