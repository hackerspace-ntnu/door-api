from flask import Flask, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful.inputs import boolean

app = Flask(__name__)
api = Api(app)
resource_fields={
        'door': True
        }
parser=reqparse.RequestParser()
parser.add_argument('door', type=boolean)

class Door(Resource):
    def get(self, key):
        return {'isOpen': resource_fields}, 200 

class DoorOpen(Resource):
    def post(self, key):
        if key in resource_fields:
            resource_fields[key]=True
            return resource_fields[key], 200

class DoorClosed(Resource):
    def post(self, key):
        if key in resource_fields:
            resource_fields[key]=False
            return resource_fields[key], 200
	
api.add_resource(Door, '/api/<string:key>')
api.add_resource(DoorOpen, '/api/<string:key>/open')
api.add_resource(DoorClosed, '/api/<string:key>/closed')

if __name__ == '__main__':
    app.run()
