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
        return self.db.get_feature_request(client_id)


    def get_clients(self):
        clients = self.db.get_clients()
        return clients

    def add_clients(self):
        self.db.add_clients()

controllerV = controllerView()

