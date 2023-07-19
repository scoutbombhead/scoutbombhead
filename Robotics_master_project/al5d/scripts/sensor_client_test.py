#!/usr/bin/env python
import rospy
from al5d.srv import *

def sensor_client(sensor_list, reps):
    rospy.wait_for_service('sensor_service')
    try:
        service = rospy.ServiceProxy('sensor_service', sensor_service)
        res = service(sensor_list, reps)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        



if __name__ == "__main__":
    print("Requesting sensor service")
    sensor_list = [True, True, True, True, True, True, True]
    # sensor_list = [False, False, False, False, True, True]
    reps = 5
    sensor_client(sensor_list, reps)