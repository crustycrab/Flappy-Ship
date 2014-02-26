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

		self.scored = False

		self.dead_animation = res.boom_animation

	def update(self, dt):
		self.x += self.velocity.x * dt
		self.y += self.velocity.y * dt

	def distance_with(self, other):
		return math.hypot(self.x - other.x, self.y - other.y)

	def collide_with(self, other):
		distance = self.distance_with(other)
		distance_to_collide = self.width / 4 + other.width / 2

		return distance < distance_to_collide

	def collide_handle(self, other):
		if isinstance(other, Entity):
			if self.collide_with(other):
				self.dead = True


class Player(Entity):

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=res.ship_animation, *args, **kwargs)

		self.x = res.PLAYER_X
		self.y = res.HALF_WIN_H

		self.scored = True

		self.gravity = -9.8 * 3
		self.velocity = utils.Vector2(10, 0)

		self.score = 0

		self.key_handler = key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]

	def update(self, dt):
		if not self.dead:
			self.velocity.y += self.gravity * dt
			self.y += self.velocity.y

			if self.y <= 22 or self.y > res.WIN_H - 22:
				self.dead = True

			normal_velocity = self.velocity.normalized()
			self.rotation = math.atan2(
				normal_velocity.x, normal_velocity.y) / math.pi * 180 - 90

			if self.key_handler[key.SPACE]:
				self.velocity.y = self.velocity.x

		else:
			self.to_remove = True

	def collide_with(self, other):
		distance = self.distance_with(other)
		distance_to_collide = self.height / 4 + other.width / 2

		return distance < distance_to_collide

	def collide_handle(self, other):
		if isinstance(other, Asteroid):
			super(Player, self).collide_handle(other)


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
		y = random.randint(res.WALL_HEIGHT + res.asteroid.height // 2, 
			res.HALF_WIN_H - res.WALL_HEIGHT)
		game_objects.append(Asteroid(x=start + random.randint(-40, 40), y=y))

		y = y + res.ASTEROIDS_DISTANCE
		game_objects.append(Asteroid(x=start, y=y))

		start += min_distance


class DeadAnimation(pyglet.sprite.Sprite):

	def __init__(self, obj, *args, **kwargs):
		super(DeadAnimation, self).__init__(
			img=obj.dead_animation, *args, **kwargs)

		self.to_remove = False

		self.x = obj.x
		self.y = obj.y

	def on_animation_end(self):
		self.to_remove = True
