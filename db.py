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

    def add_feature_request(data):
        return {'a':'success','b':'data'}

    def update_feature_request(features):
        for data in features:
            self.session.merge(FeatureRequest(ID=data.ID,Title=data.Title,
                client_id=data.client_id, Description=data.Description,
                priority=data.priority, target_date=data.target_date,
                product_area_id=data.product_area_id))
        self.session.commit()



    def get_feature_request(self,id):
        query = self.session.query(FeatureRequest.ID, FeatureRequest.Title, FeatureRequest.Description,
            FeatureRequest.priority, FeatureRequest.client_id, FeatureRequest.target_date,
            FeatureRequest.product_area_id, client.firstname, ProductArea.area_name).outerjoin(client).outerjoin(ProductArea)\
            .filter(FeatureRequest.client_id==id).order_by(FeatureRequest.priority.asc())
        return query.all()

    def get_product_areas(self):
        return self.session.query(ProductArea.ID, ProductArea.area_name).all()    

    def get_clients(self,clid=False):
        if clid:
            return self.session.query(client).filter(client.ID == clid).one()
        else:
            return self.session.query(client).order_by(client.firstname.asc()).all()

    def add_clients(self):
        objects = [
            client(username="abc", password="abc", firstname="abc", lastname="cba",email="abc@cba", telephone=12345, address=' ',state=' ',country=' ',zipcode=' ', date_added=datetime.utcnow()),
            client(username="bcd", password="bcd", firstname="bcd", lastname="dcb",email="bcd@dcb", telephone=12346, address=' ',state=' ',country=' ',zipcode=' ', date_added=datetime.utcnow()),
            client(username="cde", password="cde", firstname="cde", lastname="cde",email="cde@cde", telephone=12347, address=' ',state='',country=' ',zipcode=' ', date_added=datetime.utcnow())
        ]
        self.session.add_all(objects)
        self.session.commit()

    def remove_feature_request(feature):
        self.session.query(FeatureRequest).filter(FeatureRequest.ID == feature.ID).delete()
        self.session.commit()

DB = Database()

