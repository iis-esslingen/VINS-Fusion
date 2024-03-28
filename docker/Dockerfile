FROM osrf/ros:noetic-desktop-full

SHELL ["/bin/bash", "-c"]

ENV CERES_VERSION="1.12.0"
ENV CATKIN_WS=/workspaces/catkin_ws

      # set up thread number for building
RUN   if [ "x$(nproc)" = "x1" ] ; then export USE_PROC=1 ; \
      else export USE_PROC=$(($(nproc)/2)) ; fi && \
      apt-get update && apt-get upgrade -y && apt-get install -y \
      python3-pip \
      python3-tk \
      cmake \
      libatlas-base-dev \
      libeigen3-dev \
      libgoogle-glog-dev \
      libsuitesparse-dev \
      python3-catkin-tools \
      git \
      ros-${ROS_DISTRO}-cv-bridge \
      ros-${ROS_DISTRO}-image-transport \
      ros-${ROS_DISTRO}-message-filters \
      ros-${ROS_DISTRO}-tf && \
      # Build and install Ceres
      git clone https://ceres-solver.googlesource.com/ceres-solver && \
      cd ceres-solver && \
      git checkout tags/${CERES_VERSION} && \
      mkdir build && cd build && \
      cmake .. && \
      make -j$(USE_PROC) install && \
      rm -rf ../../ceres-solver && \
      mkdir -p $CATKIN_WS/src/VINS-Fusion/

RUN pip3 install \
        evo --upgrade --no-binary evo \
        packaging
 
RUN echo "source /opt/ros/noetic/setup.bash" >> "/root/.bashrc" && \
    # Automatic sourcing of catkin workspace.
    echo "[ -f /workspaces/catkin_ws/devel/setup.bash ] && source /workspaces/catkin_ws/devel/setup.bash" >> "/root/.bashrc"