import math
import sys

HEADER = """<?xml version="1.0"?>
<sdf version="1.9">
  <world name="line_world">
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    <light type="directional" name="sun">
      <cast_shadows>false</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>1 1 1 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="c">
          <geometry><plane><normal>0 0 1</normal><size>20 20</size></plane></geometry>
        </collision>
        <visual name="v">
          <geometry><plane><normal>0 0 1</normal><size>20 20</size></plane></geometry>
          <material><ambient>1 1 1 1</ambient><diffuse>1 1 1 1</diffuse></material>
        </visual>
      </link>
    </model>
"""
FOOTER = "  </world>\n</sdf>\n"
WIDTH = 0.03  # line width in metres


def segment(i, p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    length = math.hypot(x2 - x1, y2 - y1) + WIDTH * 0.3   # small overlap hides gaps
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    yaw = math.atan2(y2 - y1, x2 - x1)
    return f"""    <model name="seg{i}">
      <static>true</static>
      <pose>{cx:.4f} {cy:.4f} 0.0005 0 0 {yaw:.4f}</pose>
      <link name="link">
        <visual name="v">
          <geometry><box><size>{length:.4f} {WIDTH} 0.001</size></box></geometry>
          <material><ambient>0 0 0 1</ambient><diffuse>0 0 0 1</diffuse></material>
        </visual>
      </link>
    </model>
"""


def straight():
    return [(0, 0), (4, 0)]


def corner():
    return [(0, 0), (1.5, 0), (1.5, 1.5)]


def circle(r=1.0, n=60):
    # starts at the origin heading +x, curves left, returns to the start
    return [(r * math.sin(t), r * (1 - math.cos(t)))
            for t in [2 * math.pi * k / n for k in range(n + 1)]]


def s_curve(n=60):
    return [(4 * k / n, 0.3 * math.sin(2 * math.pi * (4 * k / n) / 4)) for k in range(n + 1)]


SHAPES = {'straight': straight, 'corner': corner, 'circle': circle, 's_curve': s_curve}

if __name__ == '__main__':
    shape, out = sys.argv[1], sys.argv[2]
    pts = SHAPES[shape]()
    body = ''.join(segment(i, pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    with open(out, 'w') as f:
        f.write(HEADER + body + FOOTER)
    print(f'Wrote {shape} track with {len(pts) - 1} segments to {out}')