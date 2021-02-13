from flask import render_template, request, jsonify
from . import app, feature_status
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
    data = request.get_json()
    #print(data)
    status = controllerV.add_clients(client=data)
    return jsonify({'client_id':status})



@app.route('/product_areas', methods=['GET', 'POST'])
def product_areas():
    if request.method == 'POST':
        #request.data = request.data.decode('utf-8').encode('utf-8')
        data = request.get_json()
        status = controllerV.update_product_area(parea=data)
        return jsonify({'status':status})
    data = controllerV.product_areas()
    if request.is_xhr:
        return jsonify(data)
    else:
        return render_template("feature_domain.html", pareas=data)

@app.route('/remove_parea', methods=['GET', 'POST'])
def remove_parea():
    if request.method == 'POST':
        status = controllerV.remove_parea(parea=request.json)
        return jsonify({'status':status})

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

@app.route('/get_feature_request', methods=['GET', 'POST'])
def get_feature_request():
    features, cl_info = {},{}
    cid = request.args.get('cid',False)
    if cid:
        cl_info = controllerV.get_clients(client_id=cid)
        features = controllerV.get_feature_request(data=cid)
    return render_template("fl_feature.html", data=features, client_info = cl_info, ftr_status=feature_status)


@app.route('/update_feature_request', methods=['GET', 'POST'])
def update_feature():
    
    if request.method == 'POST':
        #request.data = request.data.decode('utf-8').encode('utf-8')
        data = request.get_json()
        status = controllerV.update_feature_request(features=data)
        return jsonify({'status':status})
    

@app.route('/remove_feature_request', methods=['GET', 'POST'])
def remove_feature():
    if request.method == 'POST':
        status = controllerV.remove_feature_request(data=request.json)
        return jsonify({'status':status})

# some code here





