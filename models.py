from sqlalchemy import create_engine, ForeignKey, UniqueConstraint, Column, Integer, Boolean, String, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class FeatureRequest(Base):
    __tablename__ = 'feature_request'
    ID = Column(Integer, Sequence('id_seq'), primary_key=True)
    Title = Column(String(50))
    Description = Column(String(500))
    client_id = Column(Integer, ForeignKey('client.ID'), nullable=False)
    priority = Column(Integer, nullable=False)
    target_date = Column(DateTime)
    product_area_id = Column(Integer, ForeignKey('product_area.ID'))
    UniqueConstraint('client_id', 'priority', name='ft_requ_1')

class client(Base):
    __tablename__ = 'client'
    ID = Column(Integer, Sequence('id_seq'), primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    firstname = Column(String(20))
    lastname = Column(String(20))
    email = Column(String(50))
    telephone = Column(Integer)
    address = Column(String(120))
    state = String(20)
    country = String(20)
    zipcode = String(20)

class ProductArea(Base):
    __tablename__ = 'product_area'
    ID = Column(Integer, Sequence('id_seq'), primary_key=True)
    area_name = Column(String(30), nullable=False)





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
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)


