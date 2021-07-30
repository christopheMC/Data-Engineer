from flask import Flask
from flask import make_response
from flask import abort
from flask import jsonify
import requests
from flask import request
import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score
import pandas as pd
import numpy as np
import model

api = Flask(import_name= 'my_api')

filePath = "credentials.csv"

rows = []
predictions = []

with open(filePath, newline='') as f:
	reader = csv.reader(f)
	header = next(reader)
	for row in reader:
		rows.append(row)

@api.errorhandler(404)
def resource_not_found(error):
	return make_response(jsonify({'error': 'Resource not found'}), 404)

@api.errorhandler(401)
def bad_request(error):
	return make_response(jsonify({'error': 'Unauthorized'}), 401)

@api.errorhandler(403)
def dont_have_right(error):
	return make_response(jsonify({'error': 'You dont have right'}), 403)

def check_permission(username, password):
	for row in rows:
		if row[0] == str(username):
			if row[1] == str(password):
				return row
			abort(401)
	abort(401)

def predict(file):
	file = str(file)
	df = pd.read_csv(file, index_col = 'user_id')
	df.sex = df.sex.replace(['M','F'],[1,0])
	df['purchase_time'] = pd.to_datetime(df.purchase_time)
	df['purchase_month'] = df.purchase_time.dt.month
	df['signup_time'] = pd.to_datetime(df.signup_time)
	df['diff_time'] = df['purchase_time'] - df['signup_time']
	df['diff_day'] = df.diff_time.dt.days
	df['diff_hour'] = df.diff_time.dt.components['hours']
	df['diff_minute'] = df.diff_time.dt.components['minutes']
	df['diff_second'] = df.diff_time.dt.components['seconds']
	df = df.join(pd.get_dummies(df['source'], prefix='source'))
	df = df.join(pd.get_dummies(df['browser'], prefix='browser'))
	data = df.drop(['device_id', 'signup_time', 'purchase_time', 'source', 'browser', 'diff_time'], axis=1)
	y_pred = model.dt.predict(data)
	pred = pd.Series(y_pred)
	return pred

@api.route('/', methods=['GET'])
def hello():
	return jsonify({'App': 'API PROJET 2'})

@api.route('/status', methods=['GET'])
def return_status():
	return jsonify({'On Air': 1})
	abort(404)

@api.route('/permissions/<username>/<password>', methods=['GET'])
def return_permissions(username, password):
	row =  check_permission(username, password)
	return jsonify({'autorise': row[2]})

@api.route('/modele/<username>/<password>/<file>', methods=['GET'])
def return_score_model(username,password, file):
	row = check_permission(username,password)
	if row[2] == str(1):
		pred = predict(file)
		predictions = []
		for i in range(len(pred)):
			predictions.append({f"prediction{i}":f"{pred[i]}"})
		return jsonify(predictions)
	abort(403)

if __name__ == '__main__':
	api.run(host="0.0.0.0", port=5000)

