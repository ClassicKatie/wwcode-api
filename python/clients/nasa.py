#!/usr/bin/env python

from apicalls.nasa import Nasa

def get_picture_of_day():
    """
        params:
        date: a datetime object
        hd: boolean
    """
    args = {
        'endpoint_postfix': 'planetary/apod?',
        'params': {}
    }
    api_call = Nasa(args)
    api_call.place_call()
    if (api_call.error):
        return
    else:
        return api_call.data

def get_rover_pics(sol, camera=None, page=1):
    """
    Gets pictures from Curiosity Rover on a given Martian sol, with a certain camera
    There may be multiple pages

    params:
        sol: int
        camera: string (valid options: )
        page: int
    """

    #Validation
    valid_cameras = [
        'FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI',
        'MARDI', 'NAVCAM', 'PANCAM', 'MINITES'
    ]
    if camera and camera not in valid_cameras:
        raise Exception('Not a valid camera!')

    params = {
        'sol': sol,
        'page': page,
    }
    args = {
        'endpoint_postfix': 'mars-photos/api/v1/rovers/curiosity/photos?',
        'params': params
    }
    api_call = Nasa(args)
    api_call.place_call()

    return api_call.data
