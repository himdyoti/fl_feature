from .db import DB
from collections import defaultdict
class controllerView:
    def __init__(self):
        self.db = DB

    def add_feature_request(self, get=False, post=False, **kargs):
        if post:
            data = kargs['data']
            st = self.db.add_feature_request(data)
            return st


    def get_feature_request(self, get=False, post=False, **kargs):       
        client_id = kargs['data']
        data = self.db.get_feature_request(client_id)
        resultset = [rs._asdict() for rs in data]
        return resultset

        

    def get_product_areas(self):
        data = self.db.get_product_areas()
        resultset = [rs._asdict() for rs in data]
        return resultset

    def edit_feature_request(self, get=False, post=False, **kargs):       
        data = kargs['data']
        return self.db.edit_feature_request(data)

    def update_feature_request(self, **kargs):       
        data = kargs['features']
        return self.db.update_feature_request(data)

    def remove_feature_request(self,  **kargs):       
        data = kargs['data']
        return self.db.remove_feature_request(data)


    def get_clients(self,client_id=False):
        qdata = self.db.get_clients(client_id)
        if hasattr(qdata, 'date_added'):
            qdata.date_added = qdata.date_added.isoformat()
        return qdata

    def add_clients(self):
        self.db.add_clients()

controllerV = controllerView()

