"""
This module holds our peak app models using the sqlalchemy ORM.
We have two tables: one for the users and one for the peaks.
Each peak is owned/created by one user (the person who created it).
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """
    A user of our peak-app.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    peaks = relationship("Peak", back_populates="owner")


class Peak(Base):
    """
    A mountain peak.
    """
    __tablename__ = "peaks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    lat = Column(Float, index=True)
    lon = Column(Float, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="peaks")

    def __repr__(self):
        return f"{self.name} peak located at {self.lat},{self.lon} created by {self.owner.email}"

