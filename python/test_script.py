#!/usr/bin/env python

import clients.nasa 
import datetime

pod_url = clients.nasa.get_picture_of_day()
print(pod_url['url'])

rover_pics = clients.nasa.get_rover_pics(sol=1000)
print(rover_pics)

