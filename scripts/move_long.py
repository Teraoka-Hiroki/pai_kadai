#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import time
import math

def move_long_pattern():
    rospy.init_node('robot_long_mover', anonymous=True)
    pub = rospy.Publisher('/dtw_robot/diff_drive_controller/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10Hz
    msg = Twist()

    rospy.loginfo("=== 1分半の自動走行パフォーマンスを開始します ===")
    start_global = time.time()

    while time.time() - start_global < 90.0 and not rospy.is_shutdown():
        elapsed = time.time() - start_global

        # 0秒〜15秒：前進
        if elapsed < 15.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            rospy.loginfo_throttle(3, "【フェーズ1】前進中...")

        # 15秒〜30秒：円を描いて旋回
        elif elapsed < 30.0:
            msg.linear.x = 0.25
            msg.angular.z = -0.8
            rospy.loginfo_throttle(3, "【フェーズ2】円を描いて旋回中...")

        # 30秒〜45秒：その場で高速スピン
        elif elapsed < 45.0:
            msg.linear.x = 0.0
            msg.angular.z = 1.5
            rospy.loginfo_throttle(3, "【フェーズ3】その場で高速スピン中...")

        # 45秒〜60秒：後退
        elif elapsed < 60.0:
            msg.linear.x = -0.3
            msg.angular.z = 0.0
            rospy.loginfo_throttle(3, "【フェーズ4】バック（後退）中...")

        # 60秒〜75秒：スラローム走行
        elif elapsed < 75.0:
            msg.linear.x = 0.3
            msg.angular.z = math.sin((elapsed - 60.0) * 2.0) * 1.2
            rospy.loginfo_throttle(3, "【フェーズ5】スラローム走行中...")

        # 75秒〜90秒：フィナーレの旋回
        else:
            msg.linear.x = 0.15
            msg.angular.z = 0.5
            rospy.loginfo_throttle(3, "【フェーズ6】フィナーレの旋回中...")

        pub.publish(msg)
        rate.sleep()

    # 停止
    msg.linear.x = 0.0
    msg.angular.z = 0.0
    pub.publish(msg)
    rospy.loginfo("=== 1分半の自動走行パフォーマンスが終了しました ===")

if __name__ == '__main__':
    try:
        move_long_pattern()
    except rospy.ROSInterruptException:
        pass
