from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the engine to connect to the SQLite database
engine = create_engine('sqlite:///database.sqlite')

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
db_session = Session()

# Base class for all models
Base = declarative_base()

# Define the Image model
class Image(Base):
    __tablename__ = 'Image'

    # Define the columns for the Image table
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    filename = Column(String)

# Create the table in the database
Base.metadata.create_all(engine)
