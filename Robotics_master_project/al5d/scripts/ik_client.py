#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from al5d.srv import *
from geometry_msgs.msg import Pose


def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 4:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])
    else:
        print(usage())
        sys.exit(1)
    print("Requesting IK %s+%s+%s"%(x, y, z))
    pos = Pose()
    pos.position.x = x
    pos.position.y = y
    pos.position.z = z
    pitch = 0.0
    roll = 0.0
    joint_pos = [0, 0, 0, 0, 0, 0]

    rospy.init_node('ik_client', anonymous=False)
    rospy.wait_for_service("al5d_ik", 3)
    IkService = rospy.ServiceProxy("al5d_ik", Ik)

    response = IkService(pos, pitch, roll)
    joint_pos[0] = response.j1
    joint_pos[1] = response.j2
    joint_pos[2] = response.j3
    joint_pos[3] = response.j4
    joint_pos[4] = response.j5
    
    print("%f,  %f, %f, %f, %f "%(joint_pos[0], 
    joint_pos[1],
    joint_pos[2],
    joint_pos[3],
    joint_pos[4]))