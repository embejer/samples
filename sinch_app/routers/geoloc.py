from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from utils import geolocation
from utils.logger import logger
import models

router = APIRouter()

class Geoloc(BaseModel):
    address: str

class GeoCoor(BaseModel):
    latitude: str
    longitude: str

@router.get('/')
def get_geos(db: Session = Depends(get_db)):
    '''
    This endpoint retrieves all saved location details and
    return it as list of objects
    '''
    return db.query(models.Geolocs).all()

@router.post('/address')
def add_geo_via_name(geo_loc: Geoloc, db: Session = Depends(get_db)):
    '''
    This endpoint allow you to add or save new location using name or address. \n
    A payload or body is required for this endpoint. \n
    It will return details on the added location.
    '''
    logger(__name__, level='info', message=f'{add_geo_via_name.__name__}, Adding {geo_loc}.')

    _latitude, _longitude, _altitude = geolocation.get_details_via_address(geo_loc.address)
    
    geoloc_model = models.Geolocs()
    
    geoloc_model.address = geo_loc.address
    geoloc_model.latitude = _latitude
    geoloc_model.longitude = _longitude
    geoloc_model.altitude = _altitude

    db.add(geoloc_model)
    db.commit()
    db.refresh(geoloc_model)

    logger(__name__, level='info', message=f'{add_geo_via_name.__name__}, {geo_loc} has been added.')

    return geoloc_model  

@router.post('/coordinates')
def add_geo_via_coor(geo_loc: GeoCoor, db: Session = Depends(get_db)):
    '''
    This endpoint allow you to add or save new location using coordinates. \n
    A payload or body is required for this endpoint. \n
    It will return details on the added location.
    '''
    logger(__name__, level='info', message=f'{add_geo_via_coor.__name__}, Adding {geo_loc}.')

    _latitude = geo_loc.latitude
    _longitude = geo_loc.longitude
    _altitude = 0.0
    result = geolocation.get_details_via_coordinates(_latitude,_longitude)

    if result == None:
        return HTTPException(
            status_code = 500,
            detail = f'Coordinates: {geo_loc} does not exists.'
        ) 
    
    _address = result.address

    geoloc_model = models.Geolocs()
    
    geoloc_model.address = _address
    geoloc_model.latitude = _latitude
    geoloc_model.longitude = _longitude
    geoloc_model.altitude = _altitude

    db.add(geoloc_model)
    db.commit()
    db.refresh(geoloc_model)

    logger(__name__, level='info', message=f'{add_geo_via_coor.__name__}, {geo_loc} has been added.')

    return geoloc_model  

@router.put('/{geo_id}')
def put_geo(geo_id: int, geo_loc: Geoloc, db: Session = Depends(get_db)):
    '''
    This endpoint allow you to modify a location. \n
    A payload/body and URL parameter required for this endpoint. \n
    URL parameter is the location's ID from the database. \n
    Body contains the new location. New location coordinates will be generated. \n
    It will return details on the modified location.
    '''

    geoloc_model = db.query(models.Geolocs).filter(models.Geolocs.id == geo_id).first()

    if geoloc_model is None:
        logger(__name__, level='warning',
            message=f'{put_geo.__name__}, Updating ID: {geo_id} but does not exists.')  
        return HTTPException(
            status_code = 500,
            detail = f'ID: {geo_id} does not exists.'
        ) 
    
    logger(__name__, level='info',
        message=f'{put_geo.__name__}, Updating {geoloc_model.address} to {geo_loc.address}.')
    
    _temp_address = geoloc_model.address
    _latitude, _longitude, _altitude = geolocation.get_details_via_address(geo_loc.address)

    geoloc_model.address = geo_loc.address
    geoloc_model.latitude = _latitude
    geoloc_model.longitude = _longitude
    geoloc_model.altitude = _altitude

    db.add(geoloc_model)
    db.commit()
    db.refresh(geoloc_model)

    logger(__name__, level='info',
           message=f'{put_geo.__name__}, Updated from {_temp_address} to {geo_loc.address}.')

    return geoloc_model

@router.delete('/{geo_id}')
def delete_geo(geo_id: int, db: Session = Depends(get_db)):
    '''
    This endpoint allow you to delete or remove a location. \n
    URL parameter is required for this endpoint. \n
    A confirmation message will be returned after deletion.
    '''
    geoloc_model = db.query(models.Geolocs).filter(models.Geolocs.id == geo_id).first()
    if geoloc_model is None:
        logger(__name__, level='warning',
            message=f'{delete_geo.__name__}, Deleting ID: {geo_id} but does not exists.')
        return HTTPException(
            status_code = 500,
            detail = f'ID: {geo_id} does not exists.'
        ) 
    logger(__name__, level='info',
           message=f'{delete_geo.__name__}, Deleting {geoloc_model.address}.')
    
    db.query(models.Geolocs).filter(models.Geolocs.id == geo_id).delete()
    db.commit()

    logger(__name__, level='info',
           message=f'{delete_geo.__name__}, {geoloc_model.address} has been deleted.')

    return {'message': f'Location with ID: {geo_id} has been deleted'}