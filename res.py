import pyglet
import math
import random

WIN_W = 800
WIN_H = 600

HALF_WIN_W = WIN_W // 2
HALF_WIN_H = WIN_H // 2

WORLD_VELOCITY = 300
ASTEROIDS_DISTANCE = 250


def center_image(image):
    image.anchor_x = image.width  // 2
    image.anchor_y = image.height // 2

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

asteroid = pyglet.resource.image('asteroid.png')
center_image(asteroid)

wall = pyglet.image.ImageGrid(pyglet.resource.image('wall.png'), 1, 6)
for image in wall:
	image.height = WIN_W
wall_animation = wall.get_animation(0.2)

boom = pyglet.image.ImageGrid(pyglet.resource.image('boom.png'), 1, 4)
for image in boom:
	center_image(image)

boom_animation = boom.get_animation(0.5, loop=False)

ship = pyglet.image.ImageGrid(pyglet.resource.image('tiny_ship.png'), 1, 2)
for image in ship:
	center_image(image)

ship_animation = ship.get_animation(0.5)