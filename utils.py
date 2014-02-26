import math


class Vector2():

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def normalized(self):
		return Vector2(self.x / self.modul(), self.y / self.modul())

	def modul(self):
		return math.hypot(self.x, self.y)

	def __mul__(self, other):
		other_cls = type(other)

		if other_cls == int or other_cls == float:
			return Vector2(self.x * other, self.y * float)
		elif other_cls == Vector2:
			return self.x * other.x + self.y * other.y

	def __sub__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def __str__(self):
		return str(self.x, self.y)


class Color:

	def __init__(self, color):
		self.r, self.g, self.b, self.a = color

	def __mul__(self, value):
		return Color(tuple(map(lambda x: x * value, (self.r, self.g, self.b))) + (self.a,))

	def __div__(self, value):
		return Color(tuple(map(lambda x: x / value, (self.r, self.g, self.b))) + (self.a,))

	def __truediv__(self, value):
		return self.__div__(value)

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
