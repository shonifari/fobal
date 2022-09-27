
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
 
from sqlalchemy.orm import sessionmaker

DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

base = declarative_base()
base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()
