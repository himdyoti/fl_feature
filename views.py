from flask import render_template, request, jsonify
from fl_britecore import app
from .forms import *
from .views_controller import controllerV
import json

@app.route('/')
@app.route('/getclient')
def get_clients():
    clients = controllerV.get_clients()
    return render_template("dashboard.html", data=clients)

@app.route('/addclient', methods=['GET', 'POST'])
def add_client():
    controllerV.add_clients()
    return "clients added successfully"


@app.route('/get_feature_request', methods=['GET', 'POST'])
def get_feature_request():
    features, cl_info = {},{}
    cid = request.args.get('cid',False)
    if cid:
        cl_info = controllerV.get_clients(client_id=cid)
        features = controllerV.get_feature_request(data=cid)
    return render_template("fl_feature.html", data=features, client_info = cl_info)

@app.route('/get_product_areas', methods=['GET', 'POST'])
def get_product_areas():
    data = controllerV.get_product_areas()
    return jsonify(data)


@app.route('/add_feature_request', methods=['GET', 'POST'])
def add_feature():
    if request.method == 'POST':
        #st = controllerV.add_feature_request(post=True, data=request.json['ftrs_data'])
        return jsonify(request.json['ftrs_data'])


@app.route('/edit_feature_request', methods=['GET', 'POST'])
def edit_feature():
    if request.method == 'POST':
        controllerV.edit_feature_request(post=True, data=request.ftrs_data)

@app.route('/update_feature_request', methods=['GET', 'POST'])
def update_feature():
    if request.method == 'POST':
        print(request.json)
        controllerV.update_feature_request(features=request.json['all_features'])

@app.route('/remove_feature_request', methods=['GET', 'POST'])
def remove_feature():
    if request.method == 'POST':
        controllerV.remove_feature_request(data=request.feature)

