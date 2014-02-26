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
