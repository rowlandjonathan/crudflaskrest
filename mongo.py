# mongo.py

from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_restful import Resource, Api
from bson.json_util import dumps

app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'employee'

app.config['MONGO_URI'] = ''

client = MongoClient("")

db = client.get_database('employee')

records = db.employee_record

app.url_map.strict_slashes = False # Disable redirecting on POST method from /star to /star/

class EmployeeView(Resource):
    def get(self):
        l = list(records.find())
        x = tuple(l)
        return dumps(x)

class EmployeeFind(Resource):
    def get(self,id):
        s = records.find_one({'empID' : id})
        if s:
            output = {'name' : s['name'], 'empID' : s['empID']}
        else:
            output = "No such id"
        return jsonify({'result' : output})

class EmployeeCreate(Resource):
    def get(self,name,empID):
        r_id = records.insert({'name': name, 'empID': empID})
        new_record = records.find_one({'empID': empID })
        output = {'name' : new_record['name'], 'empID' : new_record['empID']}
        return jsonify({'result' : output})

class EmployeeUpdate(Resource):
    def get(self,id,name):
        employee_updates = {'name': name}
        s = records.update_one({'empID' : id},{'$set':employee_updates})
        new_record = records.find_one({'empID': id })
        output = {'name' : new_record['name'], 'empID' : new_record['empID']}
        return jsonify({'result' : output})

class EmployeeDelete(Resource):
    def get(self,id):
        records.delete_one({'empID': id})
        new = records.find_one({'empID' : id})
        if new:
            output = {'name' : s['name'], 'empID' : s['empID']}
        else:
            output = "Deleted"
        return jsonify({'result' : output})

api.add_resource(EmployeeView, '/')
api.add_resource(EmployeeFind, '/ef/<string:id>')
api.add_resource(EmployeeCreate, '/ec/<string:name>/<string:empID>')
api.add_resource(EmployeeUpdate, '/eu/<string:id>/<string:name>')
api.add_resource(EmployeeDelete, '/ed/<string:id>')

if __name__ == '__main__':
    app.run(debug=True)
