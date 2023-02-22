
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import *

from math import pow, atan2, sqrt,cos,sin


class TurtleBot:

    def __init__(self):
  
        self.id=1
        rospy.init_node('draw_name_turtlebot', anonymous=True)


        #services
        self.ab_tp_srv= rospy.ServiceProxy("turtle1/teleport_absolute", TeleportAbsolute)
        self.pen_srv= rospy.ServiceProxy("turtle1/set_pen", SetPen)
        self.re_tp_srv= rospy.ServiceProxy("turtle1/teleport_relative", TeleportRelative)



        self.velocity_publisher = rospy.Publisher("turtle1/cmd_vel",Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber("turtle1/pose",Pose, self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(60)
        self.speed=1
    
    def pen_off(self):
        self.pen_srv(0,0,0,0,1)
    
    def pen_on(self):
        self.pen_srv(0,0,0,3,0)

    
    def update_pose(self, data):
      
        self.pose = data

    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

   

    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose):
        return self.speed*(self.steering_angle(goal_pose) - self.pose.theta)

    def linear_vel_x(self, goal_pose):
        return  self.speed* (goal_pose.x - self.pose.x)
    def linear_vel_y(self, goal_pose):
        return  self.speed* (goal_pose.y -self.pose.y)

    def move2goal_linear(self,goal_pose):

        distance_tolerance = 0.02
        v_x=self.linear_vel_x(goal_pose) 
        v_y=self.linear_vel_y(goal_pose) 
        # v_theta=(self.steering_angle(goal_pose) - self.pose.theta)

        rospy.loginfo(str(v_x))

        vel_msg = Twist()


        # vel_msg.angular.z=self.speed*v_theta

        # while (self.steering_angle(goal_pose) - self.pose.theta)>=distance_tolerance:
        #     self.velocity_publisher.publish(vel_msg)

    
        vel_msg.linear.x = v_x
        vel_msg.linear.y =v_y
        vel_msg.angular.z=0
        

        while self.euclidean_distance(goal_pose) >= distance_tolerance:

            self.velocity_publisher.publish(vel_msg)


            pub_str="I publish linear_vel_x: "+str(vel_msg.linear.x)+" linear_vel_y: "+str(vel_msg.linear.y)
            rospy.loginfo(pub_str)


            self.rate.sleep()

        vel_msg.linear.x = 0
        vel_msg.linear.y =0
        self.velocity_publisher.publish(vel_msg)

        # rospy.spin()
