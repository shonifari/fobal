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

class Teams(base):
    __tablename__ = 'teams'
    team_id = Column(String, primary_key = True)
    name = Column(String(50), nullable = False)
    
    league_id = Column(String, nullable = False)
    nation = Column(String(50), nullable = False)
    city = Column(String(50))
    stadium = Column(String(50), nullable = False)
    stadium_address = Column(String(50))
    seats = Column(Integer, nullable = False)

    squad_size = Column(Integer, nullable = False)
    
    
    # LEAGUE LOGO LOCATION
    logo = Column(String, nullable = False)

    transfermarkt_id = Column(String(50), nullable = False)
    diretta_id = Column(String(50))
    fbref_id = Column(String(50))
    
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    



    #### I N I T #####

    def __init__(self,name, league_id, nation, logo,
        squad_size, stadium, seats,
        transfermarkt_id, diretta_id = None,fbref_id = None) -> None:
        super().__init__()
        
        self.team_id = str(uuid3(NAMESPACE_URL, name=name))
        self.name = name
        self.squad_size = squad_size
        self.logo = self.get_logo(logo)
        
        self.league_id = league_id
        self.nation = nation
        self.stadium = stadium
        self.seats = seats
        

        self.transfermarkt_id = transfermarkt_id
        self.diretta_id = diretta_id
        self.fbref_id = fbref_id

    ####### UTILS ######
    def get_logo(self,logo) -> str:
        if not '.png' in logo: return 'No Image'
        path = APP_FOLDER + '/res/image/data/teams/' + f'{self.team_id}.png'
        content = requests.get(logo).content
        with open(path,'wb') as f:
            f.write(content)
        return '/res/image/data/leagues/' + f'{self.team_id}.png'
        return path.replace(APP_FOLDER,'http://86.12.53.234:8050').replace('.png','')

    
 
    def get_transfermarkt_url(self):
        return f"https://www.transfermarkt.co.uk/{self.transfermarkt_id.split('@')[0]}/startseite/verein/{self.transfermarkt_id.split('@')[-1]}/saison_id/2022"
        
        
    def get_direttait_url(self):
        return f"https://www.diretta.it/squadra/{self.diretta_id}"


    def get_fbref_url(self):
        return f"https://fbref.com/en/squads/{self.fbref_id}"
        



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # CREATE TABLE
# base.metadata.create_all(engine)

## DELETE TABLE
#Teams.__table__.drop(engine)