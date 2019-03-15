from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import Constants
Base = declarative_base()

# Change or remove this if use other database

class Videos(Base):
    __tablename__ = 'videos'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    video_path = Column(String(2000), nullable=False)

class Knows(Base):
    __tablename__ = 'knows'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    path = Column(String(2000), nullable=False)
    video_id = Column(Integer, ForeignKey('videos.id'))
    video = relationship(Videos)

class Unknows(Base):
    __tablename__ = 'unknows'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    alias = Column(String(500), nullable=False)
    path = Column(String(2000), nullable=False)
    video_id = Column(Integer, ForeignKey('videos.id'))
    video = relationship(Videos)

class Wishper(Base):
    __tablename__ = 'wishper'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    group = Column(String(500), nullable=False)
    alias = Column(String(500), nullable=False)
    path = Column(String(2000), nullable=False)
    original_image = Column(String(2000), nullable=False)
    video_id = Column(Integer, ForeignKey('videos.id'))
    video = relationship(Videos)