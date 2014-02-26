import pyglet
from pyglet.window import key
import res
import utils
import random
import math


class Entity(pyglet.sprite.Sprite):

	def __init__(self, *args, **kwargs):
		super(Entity, self).__init__(*args, **kwargs)

		self.velocity = utils.Vector2()

		self.dead = False
		self.to_remove = False

	def update(self, dt):
		self.x += self.velocity.x * dt
		self.y += self.velocity.y * dt



class Player(Entity):

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=res.ship_animation, *args, **kwargs)

		self.x = res.HALF_WIN_W // 2
		self.y = res.HALF_WIN_H

		self.gravity = -9.8 * 3
		self.velocity = utils.Vector2(10, 0)

		self.distance = self.x
		self.score_table = []

		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]

	def update(self, dt):
		if not self.dead:
			self.velocity.y += self.gravity * dt
			self.y += self.velocity.y

			if self.y <= 22:
				self.y = 22
				self.dead = True
			elif self.y >= res.WIN_H:
				self.y = res.WIN_H - 1

			normal_velocity = self.velocity.normalized()
			self.rotation = math.atan2(
				normal_velocity.x, normal_velocity.y) / math.pi * 180 - 90

			if self.key_handler[key.SPACE]:
				self.velocity.y = self.velocity.x

		else:
			self.to_remove = True

	def distance_with(self, other):
		return math.hypot(self.x - other.x, self.y - other.y)

	def collide_with(self, other):
		distance = self.distance_with(other)
		distance_to_collide = self.height / 4 + other.width / 2

		return distance < distance_to_collide

	def collide_handle(self, other):
		if isinstance(other, Asteroid):
			if self.collide_with(other):
				self.dead = True


class Asteroid(Entity):

	def __init__(self, velocity=utils.Vector2(-res.WORLD_VELOCITY, 0), *args, **kwargs):
		super(Asteroid, self).__init__(img=res.asteroid, *args, **kwargs)

		self.velocity = velocity

		self.direction = random.choice([-1, 1])

	def update(self, dt):
		super(Asteroid, self).update(dt)
		self.rotation += random.randint(5, 10) * dt * self.direction
		if self.x <= -self.width // 2:
			self.to_remove = True


def load_asteroids(game_objects, min_distance):

	if len(game_objects) == 1:
		start = game_objects[0].x + res.WIN_W
	else:
		start = game_objects[-1].x + min_distance

	while start <= res.WIN_W * 3:
		x = start
		y = random.randint(100, res.HALF_WIN_H)
		game_objects.append(Asteroid(x=x, y=y))
		y = y + res.ASTEROIDS_DISTANCE
		game_objects.append(Asteroid(x=x, y=y))
		start += min_distance


class DeadAnimation(pyglet.sprite.Sprite):

	def __init__(self, *args, **kwargs):
		super(DeadAnimation, self).__init__(
			img=res.boom_animation, *args, **kwargs)
		self.to_remove = False

	def on_animation_end(self):
		self.to_remove = True
