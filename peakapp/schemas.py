"""
Pydantic schemas for our mountain peak application.
These schemas are used for data 'typing' and validation.
Note that we enable orm_mode in our classes to make sure pydantic will work
nicely with sqlalchemy ORM model instances.
"""
from typing import List

from pydantic import BaseModel


class PeakBase(BaseModel):
    """
    schema used for attributes shared by peak read and write operations.
    """
    name: str
    lat: float
    lon: float


class PeakCreate(PeakBase):
    """
    schema used to validate peak creation data submitted to the API.
    """
    pass


class PeakRead(PeakBase):
    """
    schema used for data returned by peak read operations.
    """

    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """
    schema for shared data by user read and create operations.
    """
    email: str


class UserCreate(UserBase):
    """
    When creating a user, a password is required.
    """
    password: str

    class Config:
        orm_mode = True


class UserRead(UserBase):
    """
    schema of data returned by a user read operation.
    """
    id: int
    is_active: bool
    peaks: List[PeakRead] = []

    class Config:
        orm_mode = True
