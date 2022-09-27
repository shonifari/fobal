from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, Boolean,String, DateTime

from datetime import datetime
from uuid import uuid3, NAMESPACE_URL
from pathlib import Path
import sys

import requests
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 

 
base = declarative_base()

class Leagues(base):
    __tablename__ = 'leagues'
    league_id = Column(String, primary_key = True)
    name = Column(String(50), nullable = False)
    nation = Column(String(50), nullable = False)

    league_level = Column(Integer, nullable = False)
    squad_size = Column(Integer, nullable = False)
    
    # LEAGUE LOGO LOCATION
    logo = Column(String, nullable = False)

    transfermarkt_id = Column(String(50), nullable = False)
    diretta_id = Column(String(50))
    fbref_id = Column(String(50))
    
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    



    #### I N I T #####

    def __init__(self,name, nation, league_level:int, squad_size:int, logo,
        transfermarkt_id, diretta_id = None,fbref_id = None) -> None:
        super().__init__()
        
        self.league_id = str(uuid3(NAMESPACE_URL, name=name))
        self.name = name
        
        self.nation = nation
        self.league_level = league_level
        self.squad_size = squad_size
        

        self.logo = self.get_logo(logo)
        self.transfermarkt_id = transfermarkt_id
        self.diretta_id = diretta_id
        self.fbref_id = fbref_id

    ####### UTILS ######
    def get_logo(self,logo) -> str:
        if not '.png' in logo: return 'No Image'
        path = APP_FOLDER + '/res/image/data/leagues/' + f'{self.league_id}.png'
        content = requests.get(logo).content
        with open(path,'wb') as f:
            f.write(content)
        return '/res/image/data/leagues/' + f'{self.league_id}.png'
        return path.replace(APP_FOLDER,'http://86.12.53.234:8050').replace('.png','')

    
 
    def get_transfermarkt_url(self):
        return f"https://www.transfermarkt.co.uk/{self.transfermarkt_id.split('@')[0]}startseite/wettbewerb/{self.transfermarkt_id.split('@')[-1]}"
        
        
    def get_direttait_url(self):
        return f"https://www.diretta.it/{self.diretta_id}"


    def get_fbref_url(self):
        return f"https://fbref.com/en/comps/{self.fbref_id}"
        



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
## CREATE TABLE
#base.metadata.create_all(engine)

## DELETE TABLE
#Leagues.__table__.drop(engine)