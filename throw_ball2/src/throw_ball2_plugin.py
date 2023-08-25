#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose, Twist
from gazebo_msgs.msg import LinkState
from gazebo_msgs.srv import SetLinkState
from std_msgs.msg import Empty
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ContactsState

def contact_callback(msg):
    # Extract and process contact information from the message
    print("entered contact callback")
    #link_state = LinkState()
    for contact in msg.states:
        print("Collision between:", contact.collision1_name, "and", contact.collision2_name)
        print("Contact points:", contact.contact_positions)
        #print("Ball position when touched the ground:")
        #print("Position x:", link_state.pose.position.x)
        #print("Position y:", link_state.pose.position.y)
        #print("Position z:", link_state.pose.position.z)
        #print("Contact forces:", contact.total_wrench.force)

    return

def throw_ball2_plugin():
    # Initialize the ROS node

    # Set the name of the link you want to throw (modify accordingly)
    link_name = 'throwable_ball::ball_link'


    # Set the initial pose of the ball (modify as needed)
    initial_pose = Pose()
    initial_pose.position.x = 0.0  # Initial x position
    initial_pose.position.y = 0.0  # Initial y position
    initial_pose.position.z = 0.5  # Initial z position (above the ground)


    # Set the initial velocity of the ball (modify as needed)
    initial_twist = Twist()
    initial_twist.linear.x = 5.5  # Initial x velocity
    initial_twist.linear.y = 0.0  # Initial y velocity
    initial_twist.linear.z = 4.0  # Initial z velocity (set to 0 to simulate no initial z velocity)


    # Create a LinkState message
    link_state = LinkState()
    link_state.link_name = link_name
    link_state.pose = initial_pose
    link_state.twist = initial_twist

    # Create a ROS publisher to send the LinkState message
    pub = rospy.Publisher('/gazebo/set_link_state', LinkState, queue_size=10)
    #contact_publisher = rospy.Publisher('/gazebo/default/throwable_basketball/ball_link/my_contact', ContactsState, queue_size=10)
    # Create a client to call the set_link_state service
    rospy.wait_for_service('/gazebo/set_link_state')
    set_link_state = rospy.ServiceProxy('/gazebo/set_link_state', SetLinkState)

    # Call the set_link_state service to move the ball with the initial velocity
    response = set_link_state(link_state)
    if response.success:
        print("Ball movement applied successfully")
    else:
        print("Failed to move the ball")

    rate = rospy.Rate(0.5)  # Publish rate of 10 Hz
    while not rospy.is_shutdown():
    
     pub.publish(link_state)
     
     rate.sleep()
    return


if __name__ == '__main__':
    try:
        
        rospy.init_node('throw_ball2_plugin', anonymous=True)
        print("BEFORE CONTACT SUB")
        rate = rospy.Rate(10)
        
        contact_topic = '/gazebo/default/throwable_ball/ball_link/my_contact'  # Adjust the topic name accordingly
        rospy.Subscriber(contact_topic, ContactsState, contact_callback, queue_size=1)
        rate.sleep()
        print("AFTER SUB")
        
        throw_ball2_plugin()
        
    except rospy.ROSInterruptException:
        pass
