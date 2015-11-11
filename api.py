from flask import Flask, jsonify
from flask.ext.restful import reqparse, abort, Api, Resource
from flask.ext.restful.inputs import boolean
import sqlite3
import datetime, time


global date, opened_sec

app = Flask(__name__)
api = Api(app)
resource_fields={

        'door': True

        }
        
parser=reqparse.RequestParser()
parser.add_argument('door', type=boolean)


def connect(today, opened, closed, total):

	conn = sqlite3.connect('door_graph.db')
	c = conn.cursor()

	c.execute(''' CREATE TABLE IF NOT EXISTS graph (today date, opened int, closed int, total int) ''')
	c.execute(" INSERT INTO graph (today, opened, closed, total) VALUES ('today', 'opened', 'closed', 'total') ")

	#save
	conn.commit()

	conn.close()

def calculate(date, opened, closed):

	time = closed - opened
	if(time >= 300):
		connect(date, opened, closed, time)

class Door(Resource):
    def get(self, key):
        return {'isOpen': resource_fields}, 200 

class DoorOpen(Resource):
    def post(self, key):
        if key in resource_fields:
            resource_fields[key]=True
            opened_sec = int(round(time.time())) 
            date = datetime.date.today()
            return resource_fields[key], 200

class DoorClosed(Resource):
    def post(self, key):
        if key in resource_fields:
            resource_fields[key]=False
            closed_sec = int(round(time.time()))
            calculate(date, opened_sec, closed_sec)
            return resource_fields[key], 200
	
api.add_resource(Door, '/api/<string:key>')
api.add_resource(DoorOpen, '/api/<string:key>/open')
api.add_resource(DoorClosed, '/api/<string:key>/closed')

if __name__ == '__main__':
    app.run()