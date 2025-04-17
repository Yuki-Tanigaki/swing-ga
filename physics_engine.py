# physics_engine.py

import math
import Box2D
from Box2D.b2 import (world, polygonShape, staticBody, dynamicBody)
import pygame

PPM = 20.0  # pixels per meter (for rendering)
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SIM_DURATION = 10.0  # seconds

# Simulation size
WIDTH, HEIGHT = 640, 480

class SwingSimulator:
    def __init__(self, visualize=False):
        self.world = world(gravity=(0, -9.81), doSleep=True)
        self.visualize = visualize

        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Swing Simulation")
            self.clock = pygame.time.Clock()

        self._create_environment()

    def _create_environment(self):
        # Anchor point (static)
        self.anchor = self.world.CreateStaticBody(position=(WIDTH / (2 * PPM), HEIGHT / PPM - 2))

        # Upper leg
        self.upper = self.world.CreateDynamicBody(
            position=self.anchor.position + (0, -1),
            fixtures=Box2D.b2FixtureDef(
                shape=polygonShape(box=(0.1, 0.5)),
                density=1.0,
                friction=0.3
            )
        )

        # Lower leg
        self.lower = self.world.CreateDynamicBody(
            position=self.upper.position + (0, -1),
            fixtures=Box2D.b2FixtureDef(
                shape=polygonShape(box=(0.1, 0.5)),
                density=1.0,
                friction=0.3
            )
        )

        # Joint between anchor and upper
        self.joint1 = self.world.CreateRevoluteJoint(
            bodyA=self.anchor,
            bodyB=self.upper,
            anchor=self.anchor.position,
            enableMotor=True,
            maxMotorTorque=10.0,
            motorSpeed=0.0
        )

        # Joint between upper and lower
        self.joint2 = self.world.CreateRevoluteJoint(
            bodyA=self.upper,
            bodyB=self.lower,
            anchor=self.upper.position + (0, -0.5),
            enableMotor=True,
            maxMotorTorque=10.0,
            motorSpeed=0.0
        )

    def simulate(self, control_sequence):
        """
        control_sequence: list of tuples [(joint1_speed, joint2_speed), ...] per frame
        Returns: fitness value (e.g., max height of lower limb)
        """
        max_height = self.lower.position[1]
        num_frames = int(SIM_DURATION * TARGET_FPS)

        for i in range(num_frames):
            if i < len(control_sequence):
                j1, j2 = control_sequence[i]
                self.joint1.motorSpeed = j1
                self.joint2.motorSpeed = j2
            else:
                self.joint1.motorSpeed = 0
                self.joint2.motorSpeed = 0

            self.world.Step(TIME_STEP, 10, 10)

            # track max vertical position
            max_height = max(max_height, self.lower.position[1])

            if self.visualize:
                self._draw_frame()

        return max_height  # or another fitness metric

    def _draw_frame(self):
        self.screen.fill((255, 255, 255))
        for body in [self.upper, self.lower]:
            for fixture in body.fixtures:
                shape = fixture.shape
                vertices = [(body.transform * v) * PPM for v in shape.vertices]
                vertices = [(v[0], HEIGHT - v[1]) for v in vertices]
                pygame.draw.polygon(self.screen, (0, 0, 0), vertices)
        pygame.display.flip()
        self.clock.tick(TARGET_FPS)
