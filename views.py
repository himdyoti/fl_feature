from flask import render_template, request
from fl_britecore import app
from .forms import *
from .views_controller import controllerV

@app.route('/')
@app.route('/getclient')
def get_clients():
    clients = controllerV.get_clients()
    return render_template("dashboard.html", data=clients)

@app.route('/feature_request', methods=['GET', 'POST'])
def feature_request():
    featues = {}
    if request.method == 'POST':
        controllerV.add_feature_request(post=True, data=request.form)
    client_id = request.args.get('id',False)
    if client_id:
        features = controllerV.get_feature_request(data=client_id)
    return render_template("fl_feature.html", data=features)

@app.route('/addclient', methods=['GET', 'POST'])
def add_client():
    controllerV.add_clients()
    return "clients added successfully"

