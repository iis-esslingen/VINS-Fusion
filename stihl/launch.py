#!/usr/bin/env python3
import os
import os.path
import subprocess
from pathlib import Path

payloads = [
    ("hinterhof", "perimeter", 0, 438),
    ("hinterhof", "lane", 544, 100000),
    ("kwald1", "perimeter", 0, 361),
    ("kwald1", "lane", 551, 100000),
    ("kwald2", "perimeter", 0, 466),
    ("kwald2", "lane", 647, 100000),
    ("seestraße", "lane", 1013, 100000),
    ("seestraße", "perimeter", 0, 830),
]

for location, scenario, start, duration in payloads:
    for run in range(5):
        path = Path(f"/workspaces/mounted_directory/{location}/{scenario}/{run}")
        path.mkdir(parents=True, exist_ok=True)
        lc_trajectory_filepath = os.path.join(path, "lc_trajectory.csv")
        no_lc_trajectory_filepath = os.path.join(path, "trajectory.csv")

        # Launch the permutation.
        command = [
            "roslaunch",  
            "/workspaces/catkin_ws/src/stihl/stihl_stereo-inertial_t265_internal.launch", 
            f"bag:=/workspaces/mounted_directory/{location}/rosbag.bag",
            f"bag_start:={start}",
            f"duration:={duration}",
            f"lc_traj_file_name:={lc_trajectory_filepath}",
            f"traj_file_name:={no_lc_trajectory_filepath}",
        ]
        subprocess.call(command)

        for trajectory_filepath in [lc_trajectory_filepath, no_lc_trajectory_filepath]:
            output_path = Path(path, Path(trajectory_filepath).stem)
            output_path.mkdir(parents=True, exist_ok=True)

            # Evaluate the trajectory.
            command = [
                "evo_traj",
                "tum",
                "--no_warnings",
                f"--ref",
                "../../../ground_truth.csv",
                "--save_plot",
                "traj",
                "--save_table",
                "traj_results.zip",
                "--plot_mode",
                "xy",
                trajectory_filepath,
            ]
            subprocess.call(command, cwd=output_path)

            # Evaluate the APE.
            command = [
                "evo_ape",
                "tum",
                "--no_warnings",
                "-a",
                "-r",
                "point_distance",
                "--save_results",
                "ape_results.zip",
                "--save_plot",
                "ape",
                "--plot_mode",
                "xy",
                "../../../ground_truth.csv",
                trajectory_filepath,
            ]
            subprocess.call(command, cwd=output_path)

            # Evaluate the RPE.
            command = [
                "evo_rpe",
                "tum",
                "--no_warnings",
                "-a",
                "-u",
                "m",
                "-d",
                "1",
                "-r",
                "point_distance",
                "--save_results",
                "rpe_results.zip",
                "--save_plot",
                "rpe",
                "--plot_mode",
                "xy",
                "../../../ground_truth.csv",
                trajectory_filepath,
            ]
            subprocess.call(command, cwd=output_path)