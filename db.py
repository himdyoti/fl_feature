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
        print(features)
        print(type(features))
        features = eval(features)
        for data in features:
            print("from db.......")
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
            return false



    def get_feature_request(self,id):
        query = self.session.query(FeatureRequest.ID, FeatureRequest.Title, FeatureRequest.Description,
            FeatureRequest.priority, FeatureRequest.client_id, FeatureRequest.target_date,
            FeatureRequest.product_area_id, client.firstname, ProductArea.area_name).outerjoin(client).outerjoin(ProductArea)\
            .filter(FeatureRequest.client_id==id).order_by(FeatureRequest.priority.asc())
        return query.all()

    def get_product_areas(self):
        return self.session.query(ProductArea.ID, ProductArea.area_name).all()    

    def get_clients(self,clid=False):
        sqlQ = self.session.query(client)
        if clid:
            return sqlQ.filter(client.ID == clid).one()
        else:
            return sqlQ.order_by(client.firstname.asc()).all()

    def add_clients(self):
        self.session.add_all(objects)
        self.session.commit()

    def remove_feature_request(feature):
        self.session.query(FeatureRequest).filter(FeatureRequest.ID == feature.ID).delete()
        self.session.commit()

DB = Database()

