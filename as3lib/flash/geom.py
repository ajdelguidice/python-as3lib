from __future__ import annotations  # Allow forward references
from as3lib import Math, Object
from as3lib.metaclasses import _AS3_CONSTANTSOBJECT
import math


class ColorTransform:...


class Matrix(Object):
   '''
   | a c tx |
   | b d ty |
   | u v w  |
   u and v are 0.0 and w is 1.0 here
   '''
   @property
   def a(self):
      return self._a

   @a.setter
   def a(self, value):
      self._a = value

   @property
   def b(self):
      return self._b

   @b.setter
   def b(self, value):
      self._b = value

   @property
   def c(self):
      return self._c

   @c.setter
   def c(self, value):
      self._c = value

   @property
   def d(self):
      return self._d

   @d.setter
   def d(self, value):
      self._d = value

   @property
   def tx(self):
      return self._tx

   @tx.setter
   def tx(self, value):
      self._tx = value

   @property
   def ty(self):
      return self._ty

   @ty.setter
   def ty(self, value):
      self._ty = value

   def __init__(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
      self._a = a
      self._b = b
      self._c = c
      self._d = d
      self._tx = tx
      self._ty = ty

   def clone(self):
      return Matrix(self.a, self.b, self.c, self.d, self.tx, self.ty)

   def concat(self, m: Matrix):
      self.setTo(
         self.a * m.a + self.c * m.b,  # + self.tx * 0.0
         self.b * m.a + self.d * m.b,  # + self.ty * 0.0
         self.a * m.c + self.c * m.d,  # + self.tx * 0.0
         self.b * m.c + self.d * m.d,  # + self.ty * 0.0
         self.a * m.tx + self.c * m.ty + self.tx,  # * 1.0
         self.b * m.tx + self.d * m.ty + self.ty,  # * 1.0
      )

   def copyColumnFrom(self, column, vector3D: Vector3D):...
   def copyColumnTo(self, column, vector3D: Vector3D):...
   def copyFrom(self, sourceMatrix: Matrix):
      self.a = sourceMatrix.a
      self.b = sourceMatrix.b
      self.c = sourceMatrix.c
      self.d = sourceMatrix.d
      self.tx = sourceMatrix.tx
      self.ty = sourceMatrix.ty

   def copyRowFrom(self, vector3D: Vector3D):...
   def copyRowTo(self, vector3D: Vector3D):...
   def createBox(self, scaleX, scaleY, rotation=0, tx=0, ty=0):...
   def createGradientBox(self, width, height, rotation=0, tx=0, ty=0):...
   def deltaTransformPoint(self, point: Point):...
   def identity(self):
      self.a, self.b, self.c, self.d, self.tx, self.ty = 1, 0, 0, 1, 0, 0

   def invert(self):...
   def rotate(self, angle):
      c = Math.cos(angle)
      s = Math.sin(angle)
      self.concat(Matrix(c, s, -s, c, 0, 0))

   def scale(self, sx, sy):
      self.concat(Matrix(sx, 0, 0, sy, 0, 0))

   def setTo(self, aa, ba, ca, da, txa, tya):
      self.a = aa
      self.b = ba
      self.c = ca
      self.d = da
      self.tx = txa
      self.ty = tya

   def toString(self):
      return f'(a={self.a}, b={self.b}, c={self.c}, d={self.d}, tx={self.tx}, ty={self.ty})'

   def transformPoint(self, point: Point):...
   def translate(self, dx, dy):...


class Matrix3D:
   '''
   | scaleX 0      0      tx |
   | 0      scaleY 0      ty |
   | 0      0      scaleZ tz |
   | 0      0      0      tw |
   '''
   ...


class Orientation3D(metaclass=_AS3_CONSTANTSOBJECT):
   AXIS_ANGLE = 'axisAngle'
   EULER_ANGLES = 'eulerAngles'
   QUATERNION = 'quanternion'


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

   def __init__(self, x=0, y=0):
      self._x = x
      self._y = y

   def add(self, v: Point):
      return Point(self.x + v.x, self.y + v.y)

   def clone(self):
      return Point(self.x, self.y)

   def copyFrom(self, sourcePoint: Point):...

   @staticmethod
   def distance(pt1: Point, pt2: Point):
      return math.sqrt((pt2.x-pt1.x) ** 2 + (pt2.y-pt1.y) ** 2)

   def equals(self, toCompare: Point):
      return self.x == toCompare.x and self.y == toCompare.y

   @staticmethod
   def interpolate(pt1: Point, pt2: Point, f):...

   def normalize(self, thickness):...

   def offset(self, dx, dy):
      self.x = self.x + dx
      self.y = self.y + dy

   @staticmethod
   def polar(len, angle):
      return Point(len * math.sin(angle), len * math.cos(angle))

   def setTo(self, xa, ya):
      self.x = xa
      self.y = ya

   def subtract(self, v: Point):
      return Point(self.x - v.x, self.y - v.y)

   def toString(self):
      return f'(x={self.x}, y={self.y})'


class Rectangle(Object):
   @property
   def bottom(self):
      return self.y + self.height

   @bottom.setter
   def bottom(self, value):
      self.height = value - self.y

   @property
   def bottomRight(self):...

   @property
   def height(self):
      return self._height

   @height.setter
   def height(self, value):
      self._height = value

   @property
   def left(self):...

   @property
   def right(self):
      return self.x + self.width

   @right.setter
   def right(self, value):
      self.width = value - self.x

   @property
   def size(self):
      return Point(self.width, self.height)

   @size.setter
   def size(self, value: Point):
      self.width = value.x
      self.height = value.y

   @property
   def top(self):...

   @property
   def topLeft(self):
      return Point(self.x, self.y)

   @topLeft.setter
   def topLeft(self, value: Point):
      self.x = value.x
      self.y = value.y

   @property
   def width(self):
      return self._width

   @width.setter
   def width(self, value):
      self._width = value

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

   def __init__(self, x=0, y=0, width=0, height=0):
      self._x = x
      self._y = y
      self._width = width
      self._height = height

   def clone(self):
      return Rectangle(self.x, self.y, self.width, self.height)

   def contains(self, x, y):
      # TODO: Make sure that this is correct. I am unsure if the boundaries are considered inside of the rectangle.
      # If the boundaries are not inside the rectangle, this should be < and > instead of <= and >=.
      return x >= self.x and x <= self.right and y >= self.y and y <= self.bottom

   def containsPoint(self, point: Point):
      return self.contains(point.x, point.y)

   def containsRect(self, rect: Rectangle):...

   def copyFrom(self, sourceRect: Rectangle):
      self.x = sourceRect.x
      self.y = sourceRect.y
      self.width = sourceRect.width
      self.height = sourceRect.height

   def equals(self, toCompare: Rectangle):
      return self.x == toCompare.x and self.y == toCompare.y and self.width == toCompare.width and self.height == toCompare.height

   def inflate(self, dx, dy):...

   def inflatePoint(self, point: Point):...

   def intersection(self, toIntersect: Rectangle):...

   def intersects(self, toIntersect: Rectangle):...

   def isEmpty(self):
      return self.width <= 0 or self.height <= 0

   def offset(self, dx, dy):
      self.x = dx
      self.y = dy

   def offsetPoint(self, point: Point):
      self.x = point.x
      self.y = point.y

   def setEmpty(self):
      self.x = 0
      self.y = 0
      self.width = 0
      self.height = 0

   def setTo(self, xa, ya, widtha, heighta):
      self.x = xa
      self.y = ya
      self.width = widtha
      self.height = heighta

   def toString(self):
      return f'(x={self.x}, y={self.y}, w={self.width}, h={self.height})'

   def union(self, toUnion: Rectangle):
      if self.isEmpty() or toUnion.isEmpty():
         ...  # The documentation says empty rectangles are ignored. I'm not sure what this is supposed to return here
      ...


class Transform:...


class Utils3D:...


class Vector3D:...
