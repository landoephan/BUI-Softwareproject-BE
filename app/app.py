import os
from flask import Flask, render_template, request, redirect
import json
from flask_cors import CORS
from flask_restplus import Api, Resource
from flask_pymongo import PyMongo
from bson.json_util import dumps

# =================================================================================================
# Controller / Views
# =================================================================================================

app = Flask(__name__, static_url_path='', template_folder='static')
CORS(app)

# DB
app.config["MONGO_URI"] = "mongodb://mongo:27017/location_db"
mongo = PyMongo(app)
api = Api(app)

@app.errorhandler(404)
def redirect_error(e):
  return render_template('index.html')

@app.route('/')
def index():
  return render_template('index.html')

@api.route('/location/')
class Locations(Resource):
    def get(self):
        result = dumps(mongo.db.locations.find())
        return json.loads(result)

@api.route('/location/<string:location_id>')
class Location(Resource):
    def get(self, location_id):
        return dumps(mongo.db.locations.find_one({ '_id': location_id }))
    def post(self, location_id):
        mongo.db.locations.replace_one({ '_id': location_id }, request.json['body'], True)
    def delete(self, location_id):
        mongo.db.locations.delete_one({ '_id': location_id })

@api.route('/catalog/')
class Catalog(Resource):
    def get(self):
        return mongo.db.catalog.find_one()
    def post(self):
        catalog = request.json['body']
        mongo.db.catalog.replace_one({ '_id': 1 }, catalog, True)
        update_locations(catalog['questions'])
        return mongo.db.catalog.find_one({ '_id': 1 })

def update_locations(questions):
    locations = json.loads(dumps(mongo.db.locations.find()))
    for l in locations:
        l['questions'] = [q for q in l['questions'] if any(question['name'] == q['name'] for question in questions)]
        for q in questions:
            if not any(question['name'] == q['name'] for question in l['questions']):
                l['questions'].append(
                    {
                        'name': q['name'],
                        'points': 0
                    }
                )
        mongo.db.locations.replace_one({ '_id': l['_id'] }, l)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
