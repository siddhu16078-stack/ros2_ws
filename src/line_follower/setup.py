from setuptools import find_packages, setup

package_name = 'line_follower'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='siddhu',
    maintainer_email='siddhu@example.com',
    description='Line follower package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello = line_follower.hello:main',
            'circle = line_follower.circle:main',
            'listener = line_follower.listener:main',
            'go_to_center = line_follower.go_to_center:main',
            'line_detector = line_follower.line_detector:main',
            'line_steering = line_follower.line_steering:main',

        ],
    },
)