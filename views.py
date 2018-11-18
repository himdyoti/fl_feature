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
    features = {}
    client_id = request.args.get('id',False)
    if client_id:
        features = controllerV.get_feature_request(data=client_id)
    return render_template("fl_feature.html", data=features)

@app.route('/get_product_areas', methods=['GET', 'POST'])
def get_product_areas():
    data = controllerV.get_product_areas()
    return jsonify(data); 


@app.route('/add_feature_request', methods=['GET', 'POST'])
def add_feature():
    if request.method == 'POST':
        controllerV.add_feature_request(post=True, data=request.ftrs_data)


@app.route('/edit_feature_request', methods=['GET', 'POST'])
def edit_feature():
    if request.method == 'POST':
        controllerV.edit_feature_request(post=True, data=request.ftrs_data)

