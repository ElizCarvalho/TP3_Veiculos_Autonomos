#!/usr/bin/env python3

import rospy, cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Pose2D

def define_goal(centroid):
    pose = Pose2D()
    pose.x = centroid[0]
    pose.y = centroid[1]
    pose.theta = 0
    rospy.loginfo("Publicacao coordenada centroide: X = %s e Y = %s", pose.x, pose.y)
    return pose

def get_centroid(cv_img, mask, put_text=False, draw_contour=False):
    """
    Finds image centroid and contourn
    Author: Adalberto Oliveira 
    cv_img: input image RGB
    mask: binary image mask
    """

    cv_output = cv_img.copy()
    
    # fiding mask contours
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]
    
    # contours parameters
    area = 0
    moment = []
    cont_out = []
    centroid = [0,0]

    # fiding great area in the mask
    for c in contours:
        M = cv2.moments(c)        
        if (M["m00"] > area):
            moment = M
            cont_out = [c]
    
    # computing centroid
    centroid[0] = int(moment["m10"]/moment["m00"])
    centroid[1] = int(moment["m01"]/moment["m00"])

    # drawning image output elements
    cv2.circle(cv_output, (centroid[0], centroid[1]), 4, (255,0,0),-1)
    if draw_contour:
        cv2.drawContours(cv_output, cont_out ,-1,(0,255,0),4)

    if put_text:
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (centroid[0],centroid[1])
        fontScale = 0.5
        fontColor = (255,255,255)
        lineType = 1
        text = '('+str(centroid[0])+', '+str(centroid[1]+10)+')'

        cv2.putText(cv_output,text, 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

    return centroid, cv_output

def get_mask(image, low, high, im_blur=False):
    """
    Receives an image and lower and upper values for color segmentation
    Author: Adalberto Oliveira 
    image: a RGB type image
    low, high: numpy array
    im_blur: applying Gaussian blur
    """
    # converting from RGB to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # creating mask
    mask = cv2.inRange(hsv,low, high)
    
    # applying Gaussian smoothing    
    if im_blur:
        mask = cv2.GaussianBlur(mask,(5,5),10)
    
    # applying morphological operations
    kernel = np.ones((5,5),np.uint8)
    mask_out = cv2.dilate(mask,kernel,iterations=2)
    mask_out = cv2.morphologyEx(mask_out,cv2.MORPH_CLOSE, kernel)
    
    return mask_out

def callback_camera(data):
    global low, high
    global cent
    rospy.loginfo("Leitura da imagem publicada no topico ROS: camera_frames")
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    mask = get_mask(cv_image, low, high, True)
    centroid, img_cont = get_centroid(cv_image, mask, True, True)
    cent = centroid
    cv2.imshow("Camera With Mask", img_cont)
    cv2.waitKey(1)

def main():
    global cent
    rospy.init_node("coord_centroid", anonymous=False)
    rospy.Subscriber("camera_frames", Image, callback_camera)
    pub_goal = rospy.Publisher('/goal', Pose2D, queue_size=10)
    rate = rospy.Rate(10)
    pose_goal = Pose2D()
    #rospy.spin()
    while not rospy.is_shutdown():
        pose_goal = define_goal(cent)
        pub_goal.publish(pose_goal)
        rate.sleep()


#Limites low e high da mascara
low = np.array([0, 18, 0], dtype=np.uint8)
high = np.array([255, 255, 255], dtype=np.uint8)
cent = [0,0]

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass