import rospy

from geometry_msgs.msg import Twist


class Mux:
    def __init__(self):
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("auto/cmd_vel", Twist, callback=self.on_auto_cmd)
        rospy.Subscriber("teleop/cmd_vel", Twist, callback=self.on_teleop_cmd)
        rospy.Subscriber("roversys", MuxSwitch, callback=self.switch)
        self.teleopswitch = True # False for auto, True for teleop

    def switch(self, switched):
        self.teleopswitch = not self.teleopswitch

    def on_auto_cmd(self, twist):
        if not self.teleopswitch:
            self.publisher.publish(twist)
    
    def on_teleop_cmd(self, twist):
        if self.teleopswitch:
            self.publisher.publish(twist)

if __name__ == '__main__':
    rospy.init_node("rover_mux")
    mux = Mux()
    rospy.spin()