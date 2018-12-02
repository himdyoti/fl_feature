from flask import render_template, request, jsonify
from fl_britecore import app
from .forms import *
from .views_controller import controllerV
import json
import pdb

@app.route('/')
@app.route('/getclient')
def get_clients():
    
    cid = request.args.get('cid',False)
    ajxReq = request.args.get('ajxReq',False)
    clients = controllerV.get_clients(client_id=cid)
    if ajxReq:
        return jsonify(clients)
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
        print(cl_info)
        features = controllerV.get_feature_request(data=cid)
    return render_template("fl_feature.html", data=features, client_info = cl_info)

@app.route('/get_product_areas', methods=['GET', 'POST'])
def get_product_areas():
    data = controllerV.get_product_areas()
    return jsonify(data)

"""
@app.route('/add_feature_request', methods=['GET', 'POST'])
def add_feature():
    if request.method == 'POST':
        #st = controllerV.add_feature_request(post=True, data=request.json['ftrs_data'])
        return jsonify(request.json['ftrs_data'])


@app.route('/edit_feature_request', methods=['GET', 'POST'])
def edit_feature():
    if request.method == 'POST':
        controllerV.edit_feature_request(post=True, data=request.ftrs_data)
"""

@app.route('/update_feature_request', methods=['GET', 'POST'])
def update_feature():
    
    if request.method == 'POST':
        #request.data = request.data.decode('utf-8').encode('utf-8')
        data = request.get_json()
        status = controllerV.update_feature_request(features=data)
        return status
    

@app.route('/remove_feature_request', methods=['GET', 'POST'])
def remove_feature():
    if request.method == 'POST':
        controllerV.remove_feature_request(data=request.feature)

