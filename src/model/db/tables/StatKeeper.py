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


class StatKeeper(base):
    __tablename__ = 'stat_keeper'
    stat_id = Column(String, primary_key=True)
    
    match_day = Column(Integer, nullable = False)
    date = Column(String, nullable = False)
    home = Column(String(50), nullable = False)
    away = Column(String(50), nullable = False)
    
    team = Column(String(50), nullable = False)
    team_id = Column(String(50), nullable = False)
    
    player_id = Column(String(50), nullable = False)
    player = Column(String(50), nullable = False)
    
    season = Column(String(50), nullable = False)

    league_id = Column(String(50), nullable = False)
    
    creation_date = Column(DateTime, default = datetime.now )
    last_update = Column(DateTime)
    
    min = Column(Integer, nullable = False)
    SoTA = Column(Integer, nullable = False)
    GA = Column(Integer, nullable = False)
    saves = Column(Integer, nullable = False)
    pass_A = Column(Integer, nullable = False)
    throws = Column(Integer, nullable = False)
    launch_A = Column(Integer, nullable = False)
    launch_C = Column(Integer, nullable = False)
    
    pass_launch_perc = Column(Numeric, nullable = False)
    pass_avg_len = Column(Numeric, nullable = False)

    GK_A = Column(Integer, nullable = False)
    GK_launch_perc = Column(Numeric, nullable = False)
    GK_avg_len = Column(Numeric, nullable = False)
    
    opp_cross_A = Column(Integer, nullable = False)
    opp_cross_stop = Column(Integer, nullable = False)
    
    n_sweeps_out_PA = Column(Integer, nullable = False)
    sweeps_avg_dist_GL = Column(Numeric, nullable = False)

    
 
 
    
    
    
    def __init__(self,
    match_day,date,home,away,min,
    team, team_id, player_id, player, season, league_id,
    SoTA, GA, saves, pass_A, throws, launch_A, launch_C,
    pass_launch_perc, pass_avg_len, GK_A, GK_launch_perc, GK_avg_len, opp_cross_A, opp_cross_stop, n_sweeps_out_PA, sweeps_avg_dist_GL) -> None:
        super().__init__()
        
        self.stat_id = str(uuid3(NAMESPACE_URL, name=match_day + date + home + away + team + player))
        
        self.match_day = match_day
        self.date = date
        self.home = home
        self.away = away
        self.min = min
        self.team = team
        self.team_id = team_id
        self.player_id = player_id
        self.player = player
        self.season = season
        self.league_id = league_id
        
        self.SoTA = SoTA
        self.GA = GA
        self.saves = saves
        self.pass_A = pass_A
        self.throws = throws
        self.launch_A = launch_A
        self.launch_C = launch_C
        self.pass_launch_perc = pass_launch_perc
        self.pass_avg_len = pass_avg_len
        self.GK_A = GK_A
        self.GK_launch_perc = GK_launch_perc
        self.GK_avg_len = GK_avg_len
        self.opp_cross_A = opp_cross_A
        self.opp_cross_stop = opp_cross_stop
        self.n_sweeps_out_PA = n_sweeps_out_PA
        self.sweeps_avg_dist_GL = sweeps_avg_dist_GL





      
        
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)
 
# # DELETE TABLE
# StatKeeper.__table__.drop(engine)
# # # CREATE TABLE
# base.metadata.create_all(engine)


 
    
