from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    articubot_dir = get_package_share_directory('vbot1')
    pkg_qt_gui_ros2 = get_package_share_directory('qt_gui_ros2')

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')

    return LaunchDescription([
        # Declare launch arguments
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('map', default_value=os.path.join(articubot_dir, 'worlds', 'newmap.yaml')),

        # Launch robot
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(articubot_dir, 'launch', 'launch_robot.launch.py')
            )
        ),

        # Delay 2 seconds before launching RPLiDAR
        TimerAction(
            period=15.0,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(articubot_dir, 'launch', 'rplidar.launch.py')
                    )
                )
            ]
        ),

        # Delay 5 seconds before launching localization
        TimerAction(
            period=20.0,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        os.path.join(articubot_dir, 'launch', 'localization_launch.py')
                    ),
                    launch_arguments={
                        'map': map_file,
                        'use_sim_time': 'false'
                    }.items()
                )
            ]
        ),



        # Delay 8 seconds before launching navigation
        #TimerAction(
            #period=50.0,
            #actions=[
                #IncludeLaunchDescription(
                    #PythonLaunchDescriptionSource(
                        #os.path.join(articubot_dir, 'launch', 'navigation_launch.py')
                    #),
                    #launch_arguments={
                        #'use_sim_time': 'false',
                        #'map_subscribe_transient_local': 'true'
                    #}.items()
                #)
            #]
        #),
    ])
