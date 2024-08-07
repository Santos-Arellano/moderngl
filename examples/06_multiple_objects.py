import math
import os
import sys

import glm
import moderngl
import numpy as np
import pygame

os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'

pygame.init()
pygame.display.set_mode((800, 800), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)


class TriangleGeometry:
    def __init__(self):
        self.ctx = moderngl.create_context()
        vertices = np.array([
            0.0, 0.4, 0.0,
            -0.4, -0.3, 0.0,
            0.4, -0.3, 0.0,
        ])

        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())

    def vertex_array(self, program):
        return self.ctx.vertex_array(program, [(self.vbo, '3f', 'in_vertex')])


class Mesh:
    def __init__(self, program, geometry):
        self.ctx = moderngl.create_context()
        self.vao = geometry.vertex_array(program)

    def render(self, position, color, scale):
        self.vao.program['position'].value = position
        self.vao.program['color'].value = color
        self.vao.program['scale'].value = scale
        self.vao.render()


class Scene:
    def __init__(self):
        self.ctx = moderngl.create_context()

        self.program = self.ctx.program(
            vertex_shader='''
                #version 120

                uniform mat4 camera;
                uniform vec3 position;
                uniform float scale;

                attribute vec3 in_vertex;

                void main() {
                    gl_Position = camera * vec4(position + in_vertex * scale, 1.0);
                }
            ''',
            fragment_shader='''
                #version 120

                uniform vec3 color;

                void main() {
                    gl_FragColor = vec4(color, 1.0);
                }
            ''',
        )

        self.triangle_geometry = TriangleGeometry()
        self.triangle = Mesh(self.program, self.triangle_geometry)

    def camera_matrix(self):
        now = pygame.time.get_ticks() / 1000.0
        eye = (math.cos(now), math.sin(now), 0.5)
        proj = glm.perspective(glm.radians(45.0), 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        return proj * look

    def render(self):
        camera = self.camera_matrix()

        self.ctx.clear(0.9, 0.9, 0.9)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.program['camera'].write(camera)

        self.triangle.render((-0.2, 0.0, 0.0), (1.0, 0.0, 0.0), 0.2)
        self.triangle.render((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.2)
        self.triangle.render((0.2, 0.0, 0.0), (0.0, 0.0, 1.0), 0.2)


scene = Scene()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.render()

    pygame.display.flip()





import math
import os
import sys

import glm
import moderngl
import numpy as np
import pygame

os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'

pygame.init()
pygame.display.set_mode((800, 800), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

# Get the existing OpenGL context from Pygame
ctx = moderngl.create_standalone_context()

class TriangleGeometry:
    def __init__(self, ctx):
        self.ctx = ctx
        vertices = np.array([
            0.0, 0.4, 0.0,
            -0.4, -0.3, 0.0,
            0.4, -0.3, 0.0,
        ], dtype='f4')
        self.vbo = self.ctx.buffer(vertices.tobytes())

    def vertex_array(self, program):
        return self.ctx.vertex_array(program, [(self.vbo, '3f', 'in_vertex')])


class Mesh:
    def __init__(self, ctx, program, geometry):
        self.ctx = ctx
        self.vao = geometry.vertex_array(program)

    def render(self, position, color, scale):
        self.vao.program['position'].value = position
        self.vao.program['color'].value = color
        self.vao.program['scale'].value = scale
        self.vao.render()


class Scene:
    def __init__(self, ctx):
        self.ctx = ctx

        self.program = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 camera;
                uniform vec3 position;
                uniform float scale;

                in vec3 in_vertex;

                void main() {
                    gl_Position = camera * vec4(position + in_vertex * scale, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                uniform vec3 color;

                out vec4 fragColor;

                void main() {
                    fragColor = vec4(color, 1.0);
                }
            ''',
        )

        self.triangle_geometry = TriangleGeometry(self.ctx)
        self.triangle = Mesh(self.ctx, self.program, self.triangle_geometry)

    def camera_matrix(self):
        now = pygame.time.get_ticks() / 1000.0
        eye = (math.cos(now), math.sin(now), 0.5)
        proj = glm.perspective(glm.radians(45.0), 1.0, 0.1, 1000.0)
        look = glm.lookAt(eye, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0))
        return proj * look

    def render(self):
        camera = self.camera_matrix()

        self.ctx.clear(0.9, 0.9, 0.9)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.program['camera'].write(camera)

        self.triangle.render((-0.2, 0.0, 0.0), (1.0, 0.0, 0.0), 0.2)
        self.triangle.render((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.2)
        self.triangle.render((0.2, 0.0, 0.0), (0.0, 0.0, 1.0), 0.2)


scene = Scene(ctx)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.render()
    pygame.display.flip()
