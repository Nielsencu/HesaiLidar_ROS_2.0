import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    description_dir = get_package_share_directory('hesai_ros_driver')

    cfg_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value='config_front.yaml',
        description='Filename of config file in config/'
    )

    rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='false',
        description='Launch RViz2 visualisation'
    )

    yaml_config = PathJoinSubstitution([description_dir, 'config', LaunchConfiguration('config_file')])
    rviz_config = PathJoinSubstitution([description_dir, 'rviz', 'rviz2.rviz'])

    driver_node = Node(
        namespace='hesai_ros_driver',
        package='hesai_ros_driver',
        executable='hesai_ros_driver_node',
        output='screen',
        parameters=[{'config_path': yaml_config}]
    )

    # --- optional visualisation ---
    rviz_node = Node(
        namespace='rviz2',
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    return LaunchDescription([
        cfg_file_arg,
        rviz_arg,
        driver_node,
        rviz_node
    ])
