#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def move_robot():
    rospy.init_node('robot_circle_mover', anonymous=True)
    pub = rospy.Publisher('/dtw_robot/diff_drive_controller/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    msg = Twist()

    rospy.loginfo("=== ロボットの自動走行を開始します ===")
    
    # ステップ1: 前進
    rospy.loginfo("ステップ1: 前進中...")
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < 2.0:
        msg.linear.x = 0.3
        msg.angular.z = 0.0
        pub.publish(msg)
        rate.sleep()

    msg.linear.x = 0.0
    pub.publish(msg)
    rospy.sleep(1.0)

    # ステップ2: 原点の周りを1周（旋回）
    rospy.loginfo("ステップ2: 原点の周りを1周（旋回）します...")
    turn_duration = 6.28
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < turn_duration:
        msg.linear.x = 0.1
        msg.angular.z = 1.0
        pub.publish(msg)
        rate.sleep()

    # ステップ3: 停止
    msg.linear.x = 0.0
    msg.angular.z = 0.0
    pub.publish(msg)
    rospy.loginfo("=== 走行が完了しました ===")

if __name__ == '__main__':
    try:
        move_robot()
    except rospy.ROSInterruptException:
        pass
