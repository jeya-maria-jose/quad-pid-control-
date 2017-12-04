#!/usr/bin/env python
#that has predefined waypoints and lands in the last waypoint
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import time
from geometry_msgs.msg import PoseArray
from tf.transformations import euler_from_quaternion
import sys
#yaw= 49.74 pitch= 14.33 roll=0
i = 0
pub_twist = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
waypoint_list = [[4.25, 4.05, 11], [-4.0, 3.25, 11], [-3.8, -4.2, 11],[4.25, -4.2, 11], [0, 0, 11]];

def callback(data):
    
    global i
    quaternion = (
    data.poses[0].orientation.x,
    data.poses[0].orientation.y,
    data.poses[0].orientation.z,
    data.poses[0].orientation.w)

    euler = euler_from_quaternion(quaternion)

    roll = euler[0]*180/3.14
    pitch = euler[1]*180/3.14
    yaw = euler[2]*180/3.14

    print (roll)," ",(pitch)," ",(yaw),"\n"

    error_yaw = yaw-49.74
    error_pitch= pitch-14.33
    error_roll=roll-0

    error_x = waypoint_list[i][0] -  data.poses[0].position.x
    error_y = waypoint_list[i][1] -  data.poses[0].position.y
    error_z = waypoint_list[i][2] -  data.poses[0].position.z

    if((abs(error_x) < 0.1) & (abs(error_y) < 0.1) & (abs(error_z)<0.1)):
        i = i + 1
        time.sleep(0.5)
        if i > 4:
	    time.sleep(1)
            pub_empty_landing.publish(Empty())
	    print "Quad Landed"
	    while 1:
	    	time.sleep(0.1)
    
    coy=0.75*error_y
    cox=0.5*error_x
    coz=0.2*error_z


    coyaw= 0.5*error_yaw
    copit= 0.5*error_pitch
    coroll= 0.01*error_roll

    twist = Twist()
    twist.linear.x =-coy; twist.linear.y = -cox; twist.linear.z = -coz
    twist.angular.x =-coyaw; twist.angular.y = -copit; twist.angular.z =-coroll
    pub_twist.publish(twist)
   

if __name__ == '__main__':
    
    print "Control"
    rospy.init_node('takeoffanand', anonymous=True)
    pub_empty_takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
    pub_empty_landing = rospy.Publisher('/ardrone/land', Empty,queue_size=1)
    
    
    time.sleep(1)
    pub_empty_takeoff.publish(Empty());
    rospy.Subscriber("/whycon/poses", PoseArray, callback)
    rospy.spin()
        
