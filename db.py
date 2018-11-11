from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    def add_feature(data):
        pass

    def get_feature_request(self,id):
        query = self.session.query(FeatureRequest.ID, FeatureRequest.Title, FeatureRequest.Description,
            FeatureRequest.priority, FeatureRequest.client_id, FeatureRequest.target_date,
            client.firstname, ProductArea.area_name).join(client).join(ProductArea)\
            .filter(FeatureRequest.client_id==id).order_by(FeatureRequest.priority.asc())
        return query.all()

    def get_product_areas(self):
        return self.session.query(ProductArea.ID, ProductArea.area_name).all()    

    def get_clients(self,id=False):
        if id:
            return self.session.query(client).filter(client.id == id).one()
        else:
            return self.session.query(client).order_by(client.firstname.asc()).all()

    def add_clients(self):
        objects = [
            client(username="abc", password="abc", firstname="abc", lastname="cba",email="abc@cba", telephone=12345, address=' ',state=' ',country=' ',zipcode=' '),
            client(username="bcd", password="bcd", firstname="bcd", lastname="dcb",email="bcd@dcb", telephone=12346, address=' ',state=' ',country=' ',zipcode=' '),
            client(username="cde", password="cde", firstname="cde", lastname="cde",email="cde@cde", telephone=12347, address=' ',state='',country=' ',zipcode=' ')
        ]
        self.session.add_all(objects)
        self.session.commit()

DB = Database()

