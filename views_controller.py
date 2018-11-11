from .db import DB
class controllerView:
    def __init__(self):
        self.db = DB

    def add_feature_request(self, get=False, post=False, **kargs):
        if post:
            data = kargs['data']
            self.db.add_feature_request(data)


    def get_feature_request(self, get=False, post=False, **kargs):       
        client_id = kargs['data']
        print(client_id)
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


    def get_clients(self):
        clients = self.db.get_clients()
        return clients

    def add_clients(self):
        self.db.add_clients()

controllerV = controllerView()

