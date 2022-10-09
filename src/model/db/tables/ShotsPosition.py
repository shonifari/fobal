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


class ShotsPositions(base):

    __tablename__ = 'shots_positions'

    shot_id = Column(String, primary_key=True)
    fixture_id = Column(String(50), nullable = False)
    order = Column(Integer, nullable = False)
 
    X = Column(Numeric, nullable = False)
    Y = Column(Numeric, nullable = False)
    
    home = Column(String(50), nullable = False)
    away = Column(String(50), nullable = False)
    
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    team = Column(String(50), nullable = False)
    
    minute = Column(Integer)
    player = Column(String(50), nullable = False)

    result = Column(String(50), nullable = False)
    shot_type = Column(String(50), nullable = False)
    last_action = Column(String(50), nullable = False)
    situation = Column(String(50), nullable = False)
    player_assisted = Column(String(50))

    team_id = Column(String(50), nullable = False)
    player_id = Column(String(50), nullable = False)
    player_assisted_id = Column(String(50))
 
    understat_link = Column(String(50), nullable = False)

    home_id = Column(String(50), nullable = False)
    away_id = Column(String(50), nullable = False)
    
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    def __init__(self,
       fixture_id,
       order,
        X,
        Y,
        home,
        away,
        home_score,
        away_score,
        team,
        minute,
        player,
        last_action,
        result,
        shot_type,
        situation,
        team_id,
        player_id,
        understat_link,
        home_id,
        away_id,
        player_assisted = None,
        player_assisted_id = None,
):
        
        super().__init__()
        self.order = order
        self.shot_id = str(uuid3(NAMESPACE_URL, home + away + player + str(minute) + last_action + understat_link))
        self.fixture_id = fixture_id
        self.X = X
        self.Y = Y
        self.home = home
        self.away = away
        self.home_score = home_score
        self.away_score = away_score
        self.team = team
        self.minute = minute
        self.player = player
        self.player_assisted = player_assisted
        self.last_action = last_action
        self.result = result
        self.shot_type = shot_type
        self.situation = situation
        self.team_id = team_id
        self.player_id = player_id
        self.player_assisted_id = player_assisted_id
        self.understat_link = understat_link
        self.home_id = home_id
        self.away_id = away_id

    ####### UTILS ######


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # CREATE TABLE
# base.metadata.create_all(engine)

# # # DELETE TABLE
# # ShotsPositions.__table__.drop(engine)
