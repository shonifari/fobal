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


class StatPerformance(base):
    __tablename__ = 'stat_performance'
    stat_id = Column(String, primary_key=True)
    
    match_day = Column(Integer, nullable = False)
    date = Column(String, nullable = False)
    home = Column(String(50), nullable = False)
    away = Column(String(50), nullable = False)
    
    team = Column(String(50), nullable = False)
    team_id = Column(String(50), nullable = False)
    
    player_id = Column(String(50), nullable = False)
    player = Column(String(50), nullable = False)
    pos = Column(String(50), nullable = False)
    
    season = Column(String(50), nullable = False)

    league_id = Column(String(50), nullable = False)
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    min = Column(Integer, nullable = False)
    
    ##
    goals = Column(Integer, nullable = False)
    ast = Column(Integer, nullable = False)
    PK_A = Column(Integer, nullable = False)
    PL_C = Column(Integer, nullable = False)
    SH_A = Column(Integer, nullable = False)
    Sot = Column(Integer, nullable = False)
    SCA = Column(Integer, nullable = False)
    GCA = Column(Integer, nullable = False)
    offside = Column(Integer, nullable = False)
    OG = Column(Integer, nullable = False)
    YCard = Column(Integer, nullable = False)    
    RCard = Column(Integer, nullable = False)
    YCard2 = Column(Integer, nullable = False)    
    fls_against = Column(Integer, nullable = False)
    fls = Column(Integer, nullable = False)
    PK_W = Column(Integer, nullable = False)
    PK_conceded = Column(Integer, nullable = False)    
    recoveries = Column(Integer, nullable = False)
    AD_W = Column(Integer, nullable = False)
    AD_L = Column(Integer, nullable = False)
     
 
    
    def __init__(self,
    match_day,date,home,away,min,
    team, team_id, player_id, player, pos,
    season, league_id,
    goals,
    ast,
    PK_A,
    PL_C,
    SH_A,
    Sot,
    SCA,
    GCA,
    offside,
    OG,
    YCard,
    RCard,
    YCard2,
    fls_against,
    fls,
    PK_W,
    PK_conceded,
    recoveries,
    AD_W,
    AD_L
) -> None:
        super().__init__()
        
        self.stat_id = str(uuid3(NAMESPACE_URL, name=match_day + date + home + away + team + player + self.__tablename__))
        
        self.match_day = match_day
        self.date = date
        self.home = home
        self.away = away
        self.min = min
        self.team = team
        self.team_id = team_id
        self.player_id = player_id
        self.player = player
        self.pos = pos
        self.season = season
        self.league_id = league_id
        
        self.goals = goals
        self.ast = ast
        self.PK_A = PK_A
        self.PL_C = PL_C
        self.SH_A = SH_A
        self.Sot = Sot
        self.SCA = SCA
        self.GCA = GCA
        self.offside = offside
        self.OG = OG
        self.YCard = YCard
        self.RCard = RCard
        self.YCard2 = YCard2
        self.fls_against = fls_against
        self.fls = fls
        self.PK_W = PK_W
        self.PK_conceded = PK_conceded
        self.recoveries = recoveries
        self.AD_W = AD_W
        self.AD_L = AD_L



      
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # # DELETE TABLE
# # StatPerformance.__table__.drop(engine)

# # # # CREATE TABLE
# base.metadata.create_all(engine)


 
    
