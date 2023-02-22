#!/usr/bin/env python3
import json
import sys
import rospy
import turtlebot_Controller as tc
from turtlesim.msg import Pose

def teleport(t,x,y):
        t.pen_off()
        t.ab_tp_srv(x,y,0)
        t.pen_on()
if __name__ == '__main__':
    try:

        f = open("/home/hassan/learning/ROS_Learning/ros1_learning/src/draw_name/scripts/letters.json")
        letters = json.load(f)
        name=sys.argv[1]
        # rospy.INFO("x")

        sc=0.12
        
        turtle=tc.TurtleBot()
        
        st=Pose(1,4,0,0,0)
        
        teleport(turtle,st.x,st.y)
     

        cnt=0
        for l in name:
            for p in letters[l]:
                 
                goal=Pose(sc*(p[0]+10*cnt)+0.5*cnt+st.x,sc*p[1]+st.y,0,0,0)
                turtle.move2goal_linear(goal)
            
            teleport(turtle,sc*(10+10*cnt)+0.5*cnt+st.x,st.y)
            turtle.pen_off()
            turtle.re_tp_srv(0.5,0)
            turtle.pen_on()
            cnt+=1

        turtle.pen_off()
        turtle.ab_tp_srv(0,0,0)
        turtle.pen_on()

    
        rospy.spin()


    except rospy.ROSInterruptException:
        pass
