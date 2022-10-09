 
from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, Boolean,String, DateTime
 
from pathlib import Path
import sys
 
# ADD THE SRC FOLDER TO THE SYS PATH
APP_FOLDER = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, APP_FOLDER) 

  
    ####### UTILS ######


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
# DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
# engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)


# def add_column(engine, table_name, column):
#     column_name = column.compile(dialect=engine.dialect)
#     column_type = column.type.compile(engine.dialect)
#     engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

# column = Column('fixture_id', String(100), nullable=False, default='default')
# add_column(engine, 'stat_defense', column)
# add_column(engine, 'stat_passing', column)
# add_column(engine, 'stat_passing_type', column)
# add_column(engine, 'stat_performance', column)
# add_column(engine, 'stat_possession', column)





from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
 
from sqlalchemy.orm import sessionmaker

DB_NAME = '/Users/karis/dev/Python/fobal/fobal.db'  
engine = create_engine(f'sqlite:///{DB_NAME}', echo=True)

base = declarative_base()
base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


from model.db.tables.Players import Players
from src.model.db.tables.Teams import Teams
from src.model.db.tables.StatKeeper import StatKeeper
from src.model.db.tables.StatPassing import StatPassing
from src.model.db.tables.StatPassingTypes import StatPassingTypes 
from src.model.db.tables.StatDefense import StatDefense
from src.model.db.tables.StatPossession import StatPossession
from src.model.db.tables.StatPerformance import StatPerformance
from src.model.db.tables.Fixtures import Fixtures


fixtures : List[Fixtures] = session.query(Fixtures).filter(Fixtures.matchday < 9).all()



for fix  in fixtures:
    stats = session.query(StatKeeper).filter(StatKeeper.match_day == fix.matchday).all()
    stats = [s for s in stats if s.team_id in [fix.home_id, fix.away_id]]
    print(fix.home, fix.away)
    print([x.player for x in stats])
    for st in stats:
        print(st.fixture_id)
        st.fixture_id = fix.fixture_id
        print(st.fixture_id)

    session.commit()


    stats = session.query(StatPassing).filter(StatPassing.match_day == fix.matchday).all()
    stats = [s for s in stats if s.team_id in [fix.home_id, fix.away_id]]
    print(fix.home, fix.away)
    print([x.player for x in stats])
    for st in stats:
        print(st.fixture_id)
        st.fixture_id = fix.fixture_id
        print(st.fixture_id)

    session.commit()
    


    stats = session.query(StatPassingTypes).filter(StatPassingTypes.match_day == fix.matchday).all()
    stats = [s for s in stats if s.team_id in [fix.home_id, fix.away_id]]
    print(fix.home, fix.away)
    print([x.player for x in stats])
    for st in stats:
        print(st.fixture_id)
        st.fixture_id = fix.fixture_id
        print(st.fixture_id)

    session.commit()
    


    stats = session.query(StatDefense).filter(StatDefense.match_day == fix.matchday).all()
    stats = [s for s in stats if s.team_id in [fix.home_id, fix.away_id]]
    print(fix.home, fix.away)
    print([x.player for x in stats])
    for st in stats:
        print(st.fixture_id)
        st.fixture_id = fix.fixture_id
        print(st.fixture_id)

    session.commit()
    


    stats = session.query(StatPossession).filter(StatPossession.match_day == fix.matchday).all()
    stats = [s for s in stats if s.team_id in [fix.home_id, fix.away_id]]
    print(fix.home, fix.away)
    print([x.player for x in stats])
    for st in stats:
        print(st.fixture_id)
        st.fixture_id = fix.fixture_id
        print(st.fixture_id)

    session.commit()
    


    stats = session.query(StatPerformance).filter(StatPerformance.match_day == fix.matchday).all()
    stats = [s for s in stats if s.team_id in [fix.home_id, fix.away_id]]
    print(fix.home, fix.away)
    print([x.player for x in stats])
    for st in stats:
        print(st.fixture_id)
        st.fixture_id = fix.fixture_id
        print(st.fixture_id)

    session.commit()
    






