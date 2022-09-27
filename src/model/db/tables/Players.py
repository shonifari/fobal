from datetime import datetime
from pathlib import Path
import sys 
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


from uuid import uuid3, NAMESPACE_URL


class Players(base):
    __tablename__ = 'players'
    player_id = Column(String, primary_key=True)
    name = Column(String(50), nullable = False)
    
    team_id = Column(String(50), nullable = False)
    league_id = Column(String(50), nullable = False)
    
    nation = Column(String, nullable = False)
    
    number = Column(Integer, nullable = False)
    dob = Column(String, nullable = False)
    height = Column(String, nullable = False)
    position = Column(String, nullable = False)
    
    # LEAGUE LOGO LOCATION
    img = Column(String, nullable = False)

    transfermarkt_id = Column(String(50), nullable = False)
    diretta_id = Column(String(50))
    fbref_id = Column(String(50))
    
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    def __init__(self,name,team_id, league_id, nation, 
        number,dob, height,position,img,
        transfermarkt_id, diretta_id = None,fbref_id = None) -> None:
        super().__init__()
        
        self.player_id = str(uuid3(NAMESPACE_URL, name=name + dob + height))
        self.name = name
        self.team_id = team_id
        self.league_id = league_id
        self.nation = nation
        self.number = number
        
        self.position = position
        self.dob = dob
        self.height = height

        self.img = self.get_logo(img)

        self.transfermarkt_id = transfermarkt_id
        self.diretta_id = diretta_id
        self.fbref_id = fbref_id

    ####### UTILS ######

    def get_transfermarkt_url(self):
        return f"https://www.transfermarkt.co.uk/{self.transfermarkt_id.split('@')[0]}/profil/spieler/{self.transfermarkt_id.split('@')[-1]}"
    

        ####### UTILS ######
    def get_logo(self,logo) -> str:
        #if not '.png' in logo: return 'No Image'
        path = APP_FOLDER + '/res/image/data/players/' + f'{self.player_id}.png'
        content = requests.get(logo).content
        with open(path,'wb') as f:
            f.write(content)
        return '/res/image/data/leagues/' + f'{self.player_id}.png'
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # CREATE TABLE
# base.metadata.create_all(engine)

## DELETE TABLE
#Players.__table__.drop(engine)