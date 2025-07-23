from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://leoonly@localhost/nba_db"

# Python code to SQL queries and sends them over to PostgreSQL
# Sessions use the engine to send commands, like .query() or .commit().
engine = create_engine(DATABASE_URL)

# Session = Temporary Workspace, make edits and save like google doc
# session.add()	Stage a new object to be inserted
# session.commit()	Actually write the changes to the database
# session.rollback()	Cancel any staged changes in that session
# session.close()	Close the connection and return it to the pool

# Example: db = SessionLocal()
# lebron = Player(name="LeBron", ppg=28.3)
# db.add(lebron)  
# db.commit()     
# db.close() 

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Opens up new session for every action ()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()