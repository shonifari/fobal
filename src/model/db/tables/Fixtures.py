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


class Fixtures(base):

    __tablename__ = 'fixtures'

    fixture_id = Column(String, primary_key=True)
    season = Column(String(50), nullable = False)
    nation = Column(String(50), nullable = False)
    league = Column(String(50), nullable = False)
    league_id = Column(String(50), nullable = False)
    
    matchday = Column(Integer, nullable = False)
    date = Column(DateTime, nullable = False)
    
    home = Column(String(50), nullable = False)
    away = Column(String(50), nullable = False)
    
    home_score = Column(Integer)
    away_score = Column(Integer)
    home_score_1T = Column(Integer)
    away_score_1T = Column(Integer)
    home_score_2T = Column(Integer)
    away_score_2T = Column(Integer)

    stadium = Column(String(50))
    referee = Column(String(50))

    diretta_link = Column(String(50), nullable = False)

    home_id = Column(String(50), nullable = False)
    away_id = Column(String(50), nullable = False)
    
    diretta_id = Column(String(50), nullable = False)
    transfermarkt_id = Column(String(50))
    fbref_id = Column(String(50))

    is_terminated = Column(Boolean, default=False)

    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    def __init__(self,
        season,nation,league,league_id,
        matchday,date,
        home,away,
        home_id,away_id,
        home_score,away_score,
        home_score_1T,away_score_1T,
        home_score_2T,away_score_2T,
        stadium,referee,
        diretta_link,
        diretta_id,
        transfermarkt_id = None,
        fbref_id = None):
        
        super().__init__()
        
        self.fixture_id = str(uuid3(NAMESPACE_URL, nation + season + matchday + home + away))
        self.season = season
        self.nation = nation
        self.league = league
        self.league_id = league_id
        self.matchday = matchday
        self.date = date
        self.home = home
        self.away = away
        self.home_id = home_id
        self.away_id = away_id
        self.home_score = home_score
        self.away_score = away_score
        self.home_score_1T = home_score_1T
        self.away_score_1T = away_score_1T
        self.home_score_2T = home_score_2T
        self.away_score_2T = away_score_2T
        self.stadium = stadium
        self.referee = referee
       
        self.diretta_link = diretta_link

        self.transfermarkt_id = transfermarkt_id
        self.diretta_id = diretta_id
        self.fbref_id = fbref_id

    ####### UTILS ######


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # CREATE TABLE
# base.metadata.create_all(engine)

# # DELETE TABLE
# # Fixtures.__table__.drop(engine)
