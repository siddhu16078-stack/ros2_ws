import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('line_bot_description')
    world = os.path.join(pkg, 'worlds', 'line_world.sdf')
    urdf = os.path.join(pkg, 'urdf', 'robot.urdf')        # adjust to where yours lives
    bridge_cfg = os.path.join(pkg, 'config', 'bridge.yaml')

    gz = ExecuteProcess(cmd=['gz', 'sim', '-r', world], output='screen')

    spawn = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-file', urdf, '-name', 'line_bot', '-z', '0.03', '-y', '0.05'],
        output='screen')

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        parameters=[{'config_file': bridge_cfg}],
        output='screen')

    return LaunchDescription([gz, spawn, bridge])