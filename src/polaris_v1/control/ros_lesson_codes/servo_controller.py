#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64

def move_servos(fls_position, frs_position, bls_position, brs_position):
    # ROS node'ini başlat
    rospy.init_node('servo_controller', anonymous=True)
    
    # Publisher'ları oluştur
    fls_pub = rospy.Publisher('/FLS_Joint_position_controller/command', Float64, queue_size=10)
    frs_pub = rospy.Publisher('/FRS_Joint_position_controller/command', Float64, queue_size=10)
    bls_pub = rospy.Publisher('/BLS_Joint_position_controller/command', Float64, queue_size=10)
    brs_pub = rospy.Publisher('/BRS_Joint_position_controller/command', Float64, queue_size=10)
    
    # Bir süre bekleyelim ki publisher'lar aktif hale gelsin
    rospy.sleep(1)
    
    # Pozisyon komutlarını gönder
    fls_pub.publish(fls_position)
    frs_pub.publish(frs_position)
    bls_pub.publish(bls_position)
    brs_pub.publish(brs_position)
    
    rospy.loginfo("Positions sent: FLS: %f, FRS: %f, BLS: %f, BRS: %f", fls_position, frs_position, bls_position, brs_position)
    
if __name__ == '__main__':
    try:
        # Örnek pozisyonlar
        fls_position = 1.0
        frs_position = 1.0
        bls_position = 1.0
        brs_position = 1.0
        
        move_servos(fls_position, frs_position, bls_position, brs_position)
        
    except rospy.ROSInterruptException:
        pass

