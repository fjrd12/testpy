from sqlalchemy import create_engine, Column, Integer, String, DateTime, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3

database_url = 'sqlite:///url_mappingdb.db'
# Create an engine to connect to a SQLite database
engine = create_engine(database_url)
Base = declarative_base()

class url_mapping(Base):
    __tablename__ = 'url_mapping'
    url_short = Column(String(50), primary_key=True)
    url_long = Column(String(1000), nullable=False)
    url_count = Column(Integer, nullable=False)

    def __int__(self):
        pass

    def init_db(self):
        Base.metadata.create_all(engine)

    def add(self, short, long):
        Session = sessionmaker(bind=engine)
        session = Session()
        new_url = url_mapping(url_short=short, url_long=long, url_count=0)
        session.add(new_url)
        session.commit()
        session.close()

    def get(self, short):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_resolution = session.query(url_mapping).filter_by(url_short=short).first()
        session.close()
        return url_resolution

    def remove(self, short_url):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_obj = session.query(url_mapping).get(short_url)
        session.delete(url_obj)
        session.commit()
        session.close()

    def update_count(self, short):
        Session = sessionmaker(bind=engine)
        session = Session()
        url_obj = session.query(url_mapping).get(short)
        url_obj.url_count = url_obj.url_count + 1
        session.commit()
