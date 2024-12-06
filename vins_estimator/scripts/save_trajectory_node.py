#!/usr/bin/env python3
import os
from typing import cast

import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


class SaveTrajectoryNode:
    def __init__(self):
        rospy.init_node("save_trajectory_node", anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # Create a subscriber to the specified topic
        rospy.Subscriber(rospy.get_param("~topic"), Path, self.path_callback)

        # Create a file to write the odometry data
        file_name = rospy.get_param("~file_name")
        self.file = open(file_name, "w")
        self.file.write("# timestamp x y z qx qy qz qw\n")
        print("Trajectory saved in: " + os.path.realpath(self.file.name))

    def path_callback(self, msg: Path):
        self.file.seek(0)

        for pose_stamped in msg.poses:
            pose_stamped = cast(PoseStamped, pose_stamped)

            self.file.write(
                str(pose_stamped.header.stamp.secs)
                + "."
                + str(pose_stamped.header.stamp.nsecs)
                + " "
                + str(pose_stamped.pose.position.x)
                + " "
                + str(pose_stamped.pose.position.y)
                + " "
                + str(pose_stamped.pose.position.z)
                + " "
                + str(pose_stamped.pose.orientation.x)
                + " "
                + str(pose_stamped.pose.orientation.y)
                + " "
                + str(pose_stamped.pose.orientation.z)
                + " "
                + str(pose_stamped.pose.orientation.w)
                + "\n"
            )

        self.file.truncate()

    def shutdown(self):
        # Close the file before shutting down the node
        self.file.close()


if __name__ == "__main__":
    node = SaveTrajectoryNode()
    rospy.spin()
