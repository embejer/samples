'''
Created By: Marlon Bejer
Created Date: Oct 21, 2023
Description: Eastvantage Technical Exam for Python Developer

Application Details;
- Able to do CRUD using API.
- Data will be saved to SQLite.
- Can retrieve near locations from a given distance and location coordinates.
'''

from fastapi import FastAPI
from database import engine
from routers import geoloc, get_distance
import models

'''
Creates the database table if it doesn't exist.
'''
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

'''
Created router for multiple endpoints with different functions.
'''
app.include_router(geoloc.router)
app.include_router(get_distance.router)
