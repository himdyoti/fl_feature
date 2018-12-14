from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, UniqueConstraint, Column, Integer, Boolean, String, Sequence, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class FeatureRequest(Base):
    __tablename__ = 'feature_request'
    ID = Column(Integer, Sequence('id_seq'), primary_key=True)
    Title = Column(String(50))
    Description = Column(String(500))
    client_id = Column(Integer, ForeignKey('client.ID'), nullable=False)
    priority = Column(Integer, nullable=True)
    target_date = Column(Date)
    product_area_id = Column(Integer, ForeignKey('product_area.ID'))
    status_id = Column(Integer, nullable=False, default=1)
    UniqueConstraint('client_id', 'priority', name='ft_requ_1')

class client(Base):
    __tablename__ = 'client'
    ID = Column(Integer, Sequence('id_seq'), primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    firstname = Column(String(30))
    lastname = Column(String(30))
    email = Column(String(50))
    telephone = Column(String(15))
    address = Column(String(120))
    state = Column(String(20))
    country = Column(String(20))
    zipcode = Column(String(20))
    date_added = Column(DateTime, default=datetime.utcnow)

class ProductArea(Base):
    __tablename__ = 'product_area'
    ID = Column(Integer, Sequence('id_seq'), primary_key=True)
    area_name = Column(String(30), nullable=False)
    description = Column(String(120), nullable=True)





if __name__=="__main__":
    import getpass
    import re

    db_urls = [
    'mysql://{user}:{passwd}@{host}/{dbname}',
    'postgresql://{user}:{passwd}@{host}/{dbname}',
    'oracle://{user}:{passwd}@{host}:1521/{dbname}'
    ]

    for key, val in enumerate(db_urls,start=1):
        print('{}.  {}'.format(key,re.split('://|\+',val)[0]), end='\n')
    
    db_type = int(input("Choose Your Database Type: "))
    assert db_type in range(1,len(db_urls) + 1), 'choose from {}'.format(','.join(range(1,len(db_urls) + 1)))
    
    user = input('Username: ')
    passwd = getpass.getpass('Enter Password: ')
    print("Enter hostname like localhost, 127.0.0.1 or IP address", end="\n")
    print("Asuming Default port number is used", end="\n")
    host = input('Hostname: ')
    dbname = input('Database Name: ')
    db_url = db_urls[db_type - 1].format(user=user,passwd=passwd,host=host,dbname=dbname)
    engine = create_engine(db_url,echo=True)
    Base.metadata.create_all(engine)


