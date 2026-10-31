import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, AppendEnvironmentVariable
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('line_bot_description')
    world = os.path.join(pkg, 'worlds', 'final_grading.sdf')
    urdf = os.path.join(pkg, 'urdf', 'robot.urdf')
    bridge_cfg = os.path.join(pkg, 'config', 'bridge.yaml')

    # Tell Gazebo where to find model://meshes/final_grading.stl
    set_res = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(pkg, 'models'))

    gz = ExecuteProcess(cmd=['gz', 'sim', '-r', world], output='screen')

    spawn = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-file', urdf, '-name', 'line_bot', '-x', '0', '-y', '0', '-z', '0.03'],
        output='screen')

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        parameters=[{'config_file': bridge_cfg}],
        output='screen')

    return LaunchDescription([set_res, gz, spawn, bridge])