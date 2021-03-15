#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def cap_img():
    path = r'/home/starwars/catkin_ws/src/cv_coord_centroid/images/caixa-de-som-1.jpg'
    img = cv2.imread(path)
    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    return img

def pub_msgs():
    pub = rospy.Publisher("camera_frames", Image, queue_size=10)
    rospy.init_node("camera_pub", anonymous=True)
    rate = rospy.Rate(10)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        try:
            cap_image = cap_img()
            rospy.loginfo('Publicacao de imagem estatica em topico ROS: camera_frames')
            pub.publish(bridge.cv2_to_imgmsg(cap_image))
            rate.sleep()
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    pub_msgs()
