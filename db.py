from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  datetime import datetime

from .models import Base, FeatureRequest, client, ProductArea
from . import app

class Database:
    def __init__(self):
        db_url = app.config.get('DB_URL','')
        if db_url:
            self.engine = create_engine(db_url, echo=True)
            self.session = sessionmaker(bind = self.engine)()
    
    def _init_setup(self):
        Base.metadata.create_all(self.engine)

    def add_feature_request(self,data):
        return {'a':'success','b':'data'}

    def update_feature_request(self,features):
        features = eval(features)
        for data in features:
            if data.get('ID',False):
                self.session.merge(FeatureRequest(ID=data['ID'], Title=data['Title'],
                    client_id=data['client_id'], Description=data['Description'],
                    priority=data['priority'], target_date=data['target_date'],
                    product_area_id=data['product_area_id']))
            else:
                self.session.merge(FeatureRequest(Title=data['Title'],
                    client_id=data['client_id'], Description=data['Description'],
                    priority=data['priority'], target_date=data['target_date'],
                    product_area_id=data['product_area_id']))

        try:
            self.session.commit()
            return True
        except:
            self.session.rollback()
            self.session.flush()
            return False



    def get_feature_request(self,id):
        query = self.session.query(FeatureRequest.ID, FeatureRequest.Title, FeatureRequest.Description,
            FeatureRequest.priority, FeatureRequest.client_id, FeatureRequest.target_date,
            FeatureRequest.product_area_id, client.firstname, ProductArea.area_name).outerjoin(client).outerjoin(ProductArea)\
            .filter(FeatureRequest.client_id==id).order_by(FeatureRequest.priority.asc())
        return query.all()

    def remove_feature_request(self,feature):
        self.session.query(FeatureRequest).filter(FeatureRequest.ID == feature['ID']).delete()
        try:
            self.session.commit()
            return True
        except:
            return False

    def product_areas(self):
        return self.session.query(ProductArea.ID, ProductArea.area_name, ProductArea.description).all() 

    def remove_parea(self,parea): 
        self.session.query(ProductArea).filter(ProductArea.ID == parea['ID']).delete()
        try:
            self.session.commit() 
            return True
        except:   # ---
            return False

    def update_product_area(self,parea):
        parea = eval(parea)
        for data in parea:
            if data.get('ID',False):
                self.session.merge(ProductArea(ID=data['ID'], area_name=data['area_name'],
                    description=data['description']))
            else:
                self.session.merge(ProductArea(area_name=data['area_name'],
                    description=data['description']))

        try:
            self.session.commit()
            return True
        except:
            self.session.rollback()
            self.session.flush()
            return False

    def get_clients(self,clid=False):
        sqlQ = self.session.query(client)
        if clid:
            return sqlQ.filter(client.ID == clid).one()
        else:
            return sqlQ.order_by(client.firstname.asc()).all()

    def add_clients(self,data):

        if data.get('client_id',False):
            cl=self.session.merge(client(ID=data['client_id'], username=data['username'],
                password=data['password'], firstname=data['firstname'],
                lastname=data['lastname'], email=data['email'], telephone=data['phone'],
                address=data['address'],state=data['state'], country=data['country'], zipcode=data['zipcode']))
        else:
            cl=self.session.merge(client(username=data['username'],
                password=data['password'], firstname=data['firstname'],
                lastname=data['lastname'], email=data['email'], telephone=data['phone'],
                address=data['address'],state=data['state'], country=data['country'], zipcode=data['zipcode']))
        try:
            self.session.commit()
            return cl.ID
        except:
            self.session.rollback()
            self.session.flush()
            return False



DB = Database()

