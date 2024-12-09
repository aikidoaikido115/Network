from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///database.sqlite')
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

class Room(Base):
    __tablename__ = 'Room'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    room_name = Column(String)

Base.metadata.create_all(engine)
