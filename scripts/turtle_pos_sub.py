#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose

def pose_log(msg):
   pos_str="turtle x: " +str(msg.x)+" y: "+str(msg.y)
   rospy.loginfo(pos_str)
if __name__ == '__main__':
    try:
        rospy.init_node("draw_pose_sub",anonymous=True)

        pose_subscriber = rospy.Subscriber("turtle1/pose",Pose, pose_log)
        rospy.spin()
      


    except rospy.ROSInterruptException:
        pass