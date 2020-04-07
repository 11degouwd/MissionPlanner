'''
Yes it' easy to send waypoint or to control a servo with python script running through APM. 
Indeed for the servo you must use channel 5 or 6 as if it was to control a gimbal. 
Here an example of code to drop a load on a gps defined target based on Joe M example, I've not tested this code in flight yet, only on the ground:
'''

import sys
from math import*
import clr
import time
import MissionPlanner import *
a = 3.14 / 180# rad/deg convertion
cible = (48.7639686*a,2.2907084*a) # gps pos of target
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
time.sleep(10)                                             # wait 10 seconds before starting
print 'Starting Mission'
Script.ChangeMode("Guided")                     # changes mode to "Guided"
item = MissionPlanner.Utilities.Locationwp() # creating waypoint
lat = 48.7639686                                          # Latitude value
lng = 2.2907084                                         # Longitude value
alt = 45.720000                                           # altitude value
MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat)     # sets latitude
MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng)   # sets longitude
MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)     # sets altitude
print 'Drop zone set'
MAV.setGuidedModeWP(item)                                    # tells UAV "go to" the set lat/long @ alt
print 'Going to DZ
dist = 10 # distance ini, just to go in the loop
Script.SendRC(5,1000,True) # servo pos 1 : close      
while abs(dist)>5: #5 is the radius in meter of the target, center on the gps pos
    pos = (cs.lat*a,cs.lng*a) # drone pos
    t1 = sin(pos[0]) * sin(cible[0])#distance to the target calcul
    t2 = cos(pos[0]) * cos(cible[0])
    t3 = cos(pos[1] - cible[1])
    t4 = t2 * t3
    t5 = t1 + t4
    rad_dist = atan(-t5/sqrt(-t5 * t5 +1)) + 2 * atan(1)
    dist = ((rad_dist * 3437.74677 * 1.1508) * 1.6093470878864446)*1000
    print dist
Script.SendRC(5,1900,True)#servo in pos 2 : open
print "Load dropped"
Script.ChangeMode("LOITER")   