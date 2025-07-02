#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64MultiArray, Bool, Int32MultiArray

# Global değişkenler
ultrasound_data = []
infrared_data = []
temperature_data = []
gas_data = []
current_data = []
encoder_data = []


def ultrasound_callback(msg):
    global ultrasound_data
    ultrasound_data = msg.data
    rospy.loginfo("Ultrasonik Sensör Verileri: %s", ultrasound_data)


def infrared_callback(msg):
    global infrared_data
    infrared_data = msg.data
    rospy.loginfo("Infrared Sensör Verileri: %s", infrared_data)


def temperature_callback(msg):
    global temperature_data
    temperature_data = msg.data
    rospy.loginfo("Sıcaklık Sensör Verileri: %s", temperature_data)


def gas_callback(msg):
    global gas_data
    gas_data = msg.data
    rospy.loginfo("Gaz Sensör Verisi: %s", gas_data)


def current_callback(msg):
    global current_data
    current_data = msg.data
    rospy.loginfo("Akım Sensör Verileri: %s", current_data)


def encoder_callback(msg):
    global encoder_data
    encoder_data = msg.data
    rospy.loginfo("Encoder Verileri: %s", encoder_data)


def motor_control(pwm_values, dir_values):
    pwm_pub = rospy.Publisher('/pwm_topic', Int32MultiArray, queue_size=10)
    dir_pub_RF = rospy.Publisher('/RF_dir_topic', Bool, queue_size=10)
    # dir_pub_LF = rospy.Publisher('/LF_dir_topic', Bool, queue_size=10)
    # dir_pub_RB = rospy.Publisher('/RB_dir_topic', Bool, queue_size=10)
    # dir_pub_LB = rospy.Publisher('/LB_dir_topic', Bool, queue_size=10)

    rospy.init_node('motor_control_node', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    pwm_msg = Int32MultiArray()
    dir_msg_RF = Bool()
    # dir_msg_LF = Bool()
    # dir_msg_RB = Bool()
    # dir_msg_LB = Bool()

    while not rospy.is_shutdown():
        # Motor PWM değerlerini ayarlayın
        pwm_msg.data = pwm_values  # Örnek PWM değerleri
        pwm_pub.publish(pwm_msg)

        # Motor yön değerlerini ayarlayın
        dir_msg_RF.data = dir_values[0]
        # dir_msg_LF.data = dir_values[1]
        # dir_msg_RB.data = dir_values[2]
        # dir_msg_LB.data = dir_values[3]

        dir_pub_RF.publish(dir_msg_RF)
        # dir_pub_LF.publish(dir_msg_LF)
        # dir_pub_RB.publish(dir_msg_RB)
        # dir_pub_LB.publish(dir_msg_LB)

        rate.sleep()

"""
def listener():
    rospy.init_node('sensor_listener', anonymous=True)

    # Sensörlerden gelen verileri dinleyen abonelikler
    rospy.Subscriber('/ultra_distance', Float64MultiArray, ultrasound_callback)
    rospy.Subscriber('/infra_distance', Float64MultiArray, infrared_callback)
    rospy.Subscriber('/temperature', Float64MultiArray, temperature_callback)
    rospy.Subscriber('/gas_alarm', Bool, gas_callback)
    rospy.Subscriber('/currents', Float64MultiArray, current_callback)
    rospy.Subscriber('/encoder', Float64MultiArray, encoder_callback)
    pwm_values = [100]
    dir_values = [True]
    motor_control(pwm_values, dir_values)
    rospy.spin()"""


"""
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
"""