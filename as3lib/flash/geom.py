import math
from as3lib._toplevel.Object import Object


class ColorTransform:...


class Matrix:...


class Matrix3D:...


class Orientation3D:...


class PerspectiveProjection:...


class Point(Object):
	@property
	def length(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self._y = value

	def __init__(self, x = 0, y = 0):
		self._x = x
		self._y = y

	def add(self, v: Point):
		return Point(self.x + v.x, self.y + v.y)

	def clone(self):
		return Point(self.x, self.y)

	def copyFrom(self, sourcePoint: Point):...

	@staticmethod
	def distance(pt1: Point, pt2: Point):...

	def equals(self, toCompare: Point):
		return self.x == toCompare.x and self.y == toCompare.y

	@staticmethod
	def interpolate(pt1: Point, pt2: Point, f):...

	def normalize(self, thickness):...

	def offset(self, dx, dy):
		self.x = self.x + dx
		self.y = self.y + dy

	@staticmethod
	def polar(len, angle):...

	def setTo(self, xa, ya):
		self.x = xa
		self.y = ya

	def subtract(self, v: Point):
		return Point(self.x - v.x, self.y - v.y)

	def toString(self):
		return f'(x={self.x}, y={self.y})'


class Rectangle:...


class Transform:...


class Utils3D:...


class Vector3D:...
