from pyglet.gl import *
import res
import math
import random


class Stars:

	def __init__(self, num_stars=256):
		self.num_stars = num_stars
		self.stars = []
		self.gen_stars()

	def draw(self):
		glPointSize(3)
		glBegin(GL_POINTS)
		for star in self.stars:
			x, y = star['cords']
			glColor3f(*star['color'])
			glVertex2i(int(x), y)
		glEnd()

	def update(self, dt):
		for i, star in enumerate(self.stars):
			speed = star['speed'] * dt
			x, y = star['cords']
			x -= speed
			if x < 0:
				x, y = (res.WIN_W + x - 1, random.randint(0, res.WIN_H - 1))
			self.stars[i]['cords'] = (x, y)

	def gen_stars(self):
		for _ in range(self.num_stars):
			x, y = self.get_random_cords()
			star = {'speed': random.randint(60, 120),
					'cords': (x, y),
					'size': random.randint(1, 2),
					'color': (random.uniform(.4, .6), random.uniform(.4, .6), random.uniform(.4, .6))}
			self.stars.append(star)

	def get_random_cords(self):
		return (random.randint(0, res.WIN_W - 1), random.randint(0, res.WIN_H - 1))



class Color:

	def __init__(self, color):
		self.r, self.g, self.b, self.a = color

	def __mul__(self, value):
		return Color(tuple(map(lambda x: x * value, (self.r, self.g, self.b))) + (self.a,))

	def __div__(self, value):
		return Color(tuple(map(lambda x: x / value, (self.r, self.g, self.b))) + (self.a,))

	def __truediv__(self, value):
		return Color(tuple(map(lambda x: x / value, (self.r, self.g, self.b))) + (self.a,))

	def __add__(self, other):
		return Color((self.r + other.r, self.g + other.g, self.b + other.b, self.a))

	def __sub__(self, other):
		return Color((self.r - other.r, self.g - other.g, self.b - other.b, self.a))

	def shuffle(self):
		dr = self.r / 2
		dg = self.g / 2
		db = self.b / 2

		return Color((random.uniform(self.r - dr, self.r + dr),
					  random.uniform(self.g - dg, self.g + dg),
					  random.uniform(self.b - db, self.b + db),
					  self.a))

	def raw(self):
		return (self.r, self.g, self.b, self.a)
