from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from utils import geolocation
from utils.logger import logger
import models

router = APIRouter()

class FromCurrent(BaseModel):
    target_distance: float


class FromCoordinates(BaseModel):
    latitude: float
    longitude: float
    altitude: float


@router.get('/from_current/{target_distance}')
def from_current_locations(target_distance: float, db: Session = Depends(get_db)):
    '''
    This endpoint retrieves locations within the target distance. \n
    Your current location is the reference. \n
    List of location details will be returned.
    '''
    locations = db.query(models.Geolocs).all()
    if locations is None:
        raise HTTPException(
            status_code = 404,
            detail = f'No data exists.'
        )

    closest_locations: list = []

    for location in locations:
        distance = geolocation.get_from_current_location(location)
        if distance <= target_distance:
            closest_locations.append(location)

    logger(__name__, level='info',
           message=f'{from_current_locations.__name__}, Target distance -> {target_distance}\
            Closest locations -> {closest_locations}.')
    
    return {'message': f'Around {target_distance} KM from your current location','locations': closest_locations}


@router.post('/from_coordinates/{target_distance}')
def from_given_coordinates(from_coordinates: FromCoordinates, target_distance: float, db: Session = Depends(get_db)):
    '''
    This endpoint retrieves locations within the target distance. \n
    A coordinate will be given as a reference. \n
    List of location details will be returned.
    '''
    closest_locations: list = []

    locations = db.query(models.Geolocs).all()

    if locations is None:
        return {'closest locations': closest_locations}
    
    for location in locations:
        if location.latitude == from_coordinates.latitude \
                and location.longitude == from_coordinates.longitude \
                and location.altitude == from_coordinates.altitude:
            continue
        distance = geolocation.get_from_saved_location(from_coordinates, location)
        if distance <= target_distance:
            closest_locations.append(location)

    logger(__name__, level='info',
           message=f'{from_given_coordinates.__name__}, Target distance -> {target_distance}\
            From -> {from_coordinates} Closest locations -> {closest_locations}.')

    return {'message': f'Around {target_distance} KM from {from_coordinates}','locations': closest_locations}


@router.get('/from_saved_locations/{from_location_id}/{target_distance}')
def from_saved_locations(from_location_id: int, target_distance: float, db: Session = Depends(get_db)):
    '''
    This endpoint retrieves locations within the target distance. \n
    An address will be given as a reference. \n
    List of location details will be returned.
    '''
    closest_locations: list = []

    locations = db.query(models.Geolocs).all()

    if locations is None:
        return {'closest locations': closest_locations}
    
    geoloc_model = db.query(models.Geolocs).filter(models.Geolocs.id == from_location_id).first()

    if geoloc_model is None:
        logger(__name__, level='warning',
            message=f'{from_saved_locations.__name__}, Checking ID: {from_location_id} but does not exists.')
        # raise HTTPException(
        #     status_code = 500,
        #     detail = f'ID: {from_location_id} does not exists.'
        # )
        return HTTPException(
            status_code = 500,
            detail = f'ID: {from_location_id} does not exists.'
        ) 

    for location in locations:
        if location.id == geoloc_model.id:
            continue
        distance = geolocation.get_from_saved_location(geoloc_model, location)
        if distance <= target_distance:
            closest_locations.append(location)

    logger(__name__, level='info',
           message=f'{from_saved_locations.__name__}, Target distance -> {target_distance}\
            From -> {geoloc_model.address} Closest locations -> {closest_locations}.')

    return {'message': f'Around {target_distance} KM from {geoloc_model.address}','locations': closest_locations}

