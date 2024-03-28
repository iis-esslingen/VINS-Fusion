#!/usr/bin/env bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

roslaunch vins vins_rviz.launch &
rosrun vins vins_node ${SCRIPTPATH}/config.yaml &
rosrun loop_fusion loop_fusion_node ${SCRIPTPATH}/config.yaml &
rosbag play /workspaces/mounted_directory/hinterhof/rosbag.bag
