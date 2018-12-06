from .db import DB
from collections import defaultdict
from flask import jsonify
class controllerView:
    def __init__(self):
        self.db = DB

    """
    def add_feature_request(self, get=False, post=False, **kargs):
        if post:
            data = kargs['data']
            st = self.db.add_feature_request(data)
            return st
    

    def edit_feature_request(self, get=False, post=False, **kargs):       
        data = kargs['data']
        return self.db.edit_feature_request(data)

    """

    def filter_orm_rs(qobj):
        """
        requires a resultset Object
        """
        rs_list = []
        if not isinstance(qobj, list):
            rs_list.append(qobj)
        else:
            rs_list = qobj

        rs = rs_list[0]
        tbl = rs.__tablename__
        tcols = [colu.name for colu in list(rs.__table__._columns)]
        for rs in rs_list:
            rs_dict = rs._asdict() if hasattr(rs,'_asdict') else rs.__dict__ 
            rs_dict = {k:v for (k,v) in rs_dict.items() if k in tcols}
            yield rs_dict      
    
    def update_feature_request(self, **kargs):       
        data = kargs['features']
        return self.db.update_feature_request(data)


    def get_feature_request(self, get=False, post=False, **kargs):       
        client_id = kargs['data']
        data = self.db.get_feature_request(client_id)
        resultset = [rs._asdict() for rs in data]
        return resultset

        

    def get_product_areas(self):
        data = self.db.get_product_areas()
        resultset = [rs._asdict() for rs in data]
        return resultset



    def remove_feature_request(self,  **kargs):       
        data = kargs['data']
        return self.db.remove_feature_request(data)


    def get_clients(self,client_id=False):
        qdata = self.db.get_clients(client_id)
        if qdata:
            return list(controllerView.filter_orm_rs(qdata))
        return False


    def add_clients(self,client=False):
        if client:
            self.db.add_clients(client)

controllerV = controllerView()

