"""
FastAPI poc for mountain peaks application poc.

"""
import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import folium
from fastapi.responses import HTMLResponse, RedirectResponse
import geoip2.database
geoip_reader = geoip2.database.Reader(os.path.join(os.path.split(os.path.abspath(__file__))[0],
                                             'GeoLite2-Country.mmdb'))

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def reject_non_french_ips(request: Request, call_next):
    """
    Arbitrarily reject non french IP as per Maxmind free country for ip database.
    :param request:
    :param call_next:
    :return:
    """
    try:
        match = geoip_reader.country(request.client.host)
        if match and match.country.iso_code != "FR":
            return HTTPException(status_code=403, detail=f"Forbidden for IP {request.client.host}")
    except geoip2.errors.AddressNotFoundError:
        pass
    response = await call_next(request)
    return response


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user. input data is validated by schema UserCreate, output by schema UserRead
    :param user:
    :param db:
    :return:
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Read all users
    :param skip:
    :param limit:
    :param db:
    :return:
    """
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Returns one user data given its id.
    :param user_id:
    :param db:
    :return:
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/peaks/", response_model=schemas.PeakRead)
def create_peak_for_user(
    user_id: int, peak: schemas.PeakCreate, db: Session = Depends(get_db)
):
    return crud.create_peak(db=db, peak=peak, user_id=user_id)


@app.get("/peaks/", response_model=List[schemas.PeakRead])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    peaks = crud.get_all_peaks(db, skip=skip, limit=limit)
    return peaks


@app.get("/", response_class=HTMLResponse)
def index(db: Session = Depends(get_db)):
    """
    Our index shows a nice folium map with our peaks.
    :return:
    """
    start_coords = (46.0, 2.0)  # roughly centered on Fr
    map = folium.Map(location=start_coords, zoom_start=6, tiles='Stamen Terrain')
    for peak in crud.get_all_peaks(db):
        folium.Marker(
            location=[peak.lat, peak.lon],
            popup=str(peak),
            icon=folium.Icon(icon='cloud') #  see font-awesome for icon list
        ).add_to(map)
    return map._repr_html_()


@app.get("/generate_data")
def gen_data(db: Session = Depends(get_db)):
    """
    Utility endpoint that populates the db with some fixed data. It is not RESTful, I know.
    :return:
    """
    PEAKS = ({
              "name": "aneto",
              "lat": 42.6311,
              "lon": 0.657252
            },
             {
             "name": "campbieil",
             "lat": 42.7923,
             "lon": 0.11978
             },
             {
             "name": "montcalm",
             "lat": 42.6719,
             "lon": 01.40614
             },
    )
    user = crud.get_or_create_user(db, schemas.UserCreate(email="frank@x.fr", password="tfp"))
    for peak in PEAKS:
        crud.get_or_create_peak(db, schemas.PeakCreate(**peak), user.id)
    return RedirectResponse("/")
