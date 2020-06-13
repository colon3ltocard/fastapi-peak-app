"""
This module provides utility functions to interact with the database.
it decouples the db operations from the http endpoint implementation itself.
It is here that the ORM models are 'plugged' with the pydantic schemas.
"""

from sqlalchemy.orm import Session

from . import models, schemas


def get_or_create(db: Session, model, **kwargs):
    """
    Rough sqlalchemy equivalent of django get_or_create
    :param db: 
    :param model: 
    :param kwargs: 
    :return: 
    """
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        return instance


def get_or_create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    :param db:
    :param user:
    :return:
    """
    return get_or_create(db, models.User, **user.dict())


def get_or_create_peak(db: Session, peak: schemas.PeakCreate, user_id: int) -> models.Peak:
    """
    :param db:
    :param peak:
    :return:
    """
    return get_or_create(db, models.Peak, **peak.dict(), owner_id=user_id)


def get_user(db: Session, user_id: int):
    """
    Returns a User instance given its id
    :param db:
    :param user_id:
    :return:
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Returns a User instance given its email
    :param db:
    :param email:
    :return:
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns all users (capped at 100)
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user
    :param db:
    :param user:
    :return:
    """

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_peaks(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns all peaks (capped at 100)
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.Peak).offset(skip).limit(limit).all()


def create_peak(db: Session, peak: schemas.PeakCreate, user_id: int):
    """
    Create a peak 'belonging' to the user with id user_id.
    :param db:
    :param peak:
    :param user_id:
    :return:
    """
    db_item = models.Peak(**peak.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item