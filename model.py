from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Profiles(Base):
    __tablename__ = "profiles"

    author_fid = Column(Integer, primary_key=True)
    displayName = Column(String(255))
    username = Column(String(255))
    followerCount = Column(Integer)
    followingCount = Column(Integer)
    scrapped_timestamp = Column(DateTime)

    # Relationship to Casts
    casts = relationship("Casts", back_populates="profiles")


class Casts(Base):
    __tablename__ = "casts"

    id = Column(Integer, primary_key=True)
    author_fid = Column(Integer, ForeignKey("profiles.author_fid"))
    text = Column(Text)
    viewCount = Column(Integer)
    combinedRecastCount = Column(Integer)
    reactions = Column(Integer)
    replies = Column(Integer)
    warpsTipped = Column(Integer)
    timestamp = Column(DateTime)
    scrapped_timestamp = Column(DateTime)

    # Relationship to Profiles
    profiles = relationship("Profiles", back_populates="casts")


class Adresses(Base):
    __tablename__ = "adresses"

    id = Column(Integer, primary_key=True)
    author_fid = Column(Integer, ForeignKey("profiles.author_fid"))
    address = Column(Text)
    scrapped_timestamp = Column(DateTime)

    # Relationship to Profiles
    profiles = relationship("Profiles", back_populates="adresses")
