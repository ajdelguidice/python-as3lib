from __future__ import annotations  # Allow forward references
from as3lib import Math, Object
from as3lib.metaclasses import _AS3_CONSTANTSOBJECT
import math


class ColorTransform(Object):
   @property
   def alphaMultiplier(self):
      return self._alphaM

   @alphaMultiplier.setter
   def alphaMultiplier(self, value):
      self._alphaM = value

   @property
   def alphaOffset(self):
      return self._alphaO

   @alphaOffset.setter
   def alphaOffset(self, value):
      self._alphaO = value

   @property
   def blueMultiplier(self):
      return self._blueM

   @blueMultiplier.setter
   def blueMultiplier(self, value):
      self._blueM = value

   @property
   def blueOffset(self):
      return self._blueO

   @blueOffset.setter
   def blueOffset(self, value):
      self._blueO = value

   @property
   def color(self):
      return self.redOffset << 16 | self.greenOffset << 8 | self.blueOffset

   @color.setter
   def color(self, value):
      self.redMultiplier = 0
      self.greenMultiplier = 0
      self.blueMultiplier = 0
      self.redOffset = (value >> 16) & 0xFF
      self.greenOffset = (value >> 8) & 0xFF
      self.blueOffset = value & 0xFF

   @property
   def greenMultiplier(self):
      return self._greenM

   @greenMultiplier.setter
   def greenMultiplier(self, value):
      self._greenM = value

   @property
   def greenOffset(self):
      return self._greenO

   @greenOffset.setter
   def greenOffset(self, value):
      self._greenO = value

   @property
   def redMultiplier(self):
      return self._redM

   @redMultiplier.setter
   def redMultiplier(self, value):
      self._redM = value

   @property
   def redOffset(self):
      return self._redO

   @redOffset.setter
   def redOffset(self, value):
      self._redO = value

   def __init__(self, redMultiplier = 1.0, greenMultiplier = 1.0, blueMultiplier = 1.0, alphaMultiplier = 1.0, redOffset = 0, greenOffset = 0, blueOffset = 0, alphaOffset = 0):
      self._redM = redMultiplier
      self._redO = redOffset
      self._greenM = greenMultiplier
      self._greenO = greenOffset
      self._blueM = blueMultiplier
      self._blueO = blueOffset
      self._alphaM = alphaMultiplier
      self._alphaO = alphaOffset

   def concat(self, second: ColorTransform):
      raise NotImplementedError

   def toString(self):
      return 'redMultiplier=%s, redOffset=%s, greenMultiplier=%s, greenOffset=%s, blueMultiplier=%s, blueOffset=%s, alphaMultiplier=%s, alphaOffset=%s)' % (self._redM, self._redO, self._greenM, self._greenO, self._blueM, self._blueO, self._alphaM, self._alphaO)


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
         m.a * self.a + m.c * self.b,
         m.b * self.a + m.d * self.b,
         m.a * self.c + m.c * self.d,
         m.b * self.c + m.d * self.d,
         m.a * self.tx + m.c * self.ty + m.tx,
         m.b * self.tx + m.d * self.ty + m.ty,
      )

   def copyColumnFrom(self, column, vector3D: Vector3D):
      # NOTE: According to the tests, copyColumnFrom is supposed to do the
      # same thing as copyRowFrom. This doesn't make sense but the test passes
      # on flash player so it must be right.
      self.copyRowFrom(column, vector3D)

   def copyColumnTo(self, column, vector3D: Vector3D):
      if column == 0:
         vector3D.setTo(self.a, self.b, 0.0)
      elif column == 1:
         vector3D.setTo(self.c, self.d, 0.0)
      elif column == 2:
         vector3D.setTo(self.tx, self.ty, 1.0)

   def copyFrom(self, sourceMatrix: Matrix):
      self.a = sourceMatrix.a
      self.b = sourceMatrix.b
      self.c = sourceMatrix.c
      self.d = sourceMatrix.d
      self.tx = sourceMatrix.tx
      self.ty = sourceMatrix.ty

   def copyRowFrom(self, row, vector3D: Vector3D):
      temp = (vector3D.x, vector3D.y, vector3D.z)
      if row == 0:
         self.a, self.c, self.tx = temp
      elif row == 1:
         self.b, self.d, self.ty = temp

   def copyRowTo(self, row, vector3D: Vector3D):
      if row == 0:
         vector3D.setTo(self.a, self.c, self.tx)
      elif row == 1:
         vector3D.setTo(self.b, self.d, self.ty)
      elif row == 2:
         vector3D.setTo(0.0, 0.0, 1.0)

   def createBox(self, scaleX, scaleY, rotation=0, tx=0, ty=0):
      self.identity()
      self.rotate(rotation)
      self.scale(scaleX, scaleY)
      self.translate(tx, ty)

   def createGradientBox(self, width, height, rotation=0, tx=0, ty=0):
      self.createBox(width / 1638.4, height / 1638.4, rotation, tx + width / 2, ty + height / 2)

   def deltaTransformPoint(self, point: Point):
      return Point(self.a * point.x + self.c * point.y, self.b * point.x + self.d * point.y)

   def identity(self):
      self.a, self.b, self.c, self.d, self.tx, self.ty = 1, 0, 0, 1, 0, 0

   def invert(self):
      det = self.a * self.d - self.c * self.b
      a = self.d / det
      b = self.b / -det
      c = self.c / -det
      d = self.a / det
      tx = (self.d * self.tx - self.c * self.ty) / -det
      ty = (self.b * self.tx - self.a * self.ty) / det

      self.setTo(a, b, c, d, tx, ty)

   def rotate(self, angle):
      c = Math.cos(angle)
      s = Math.sin(angle)
      self.setTo(
         c * self.a + (-s) * self.b,
         s * self.a + c * self.b,
         c * self.c + (-s) * self.d,
         s * self.c + c * self.d,
         c * self.tx + (-s) * self.ty,
         s * self.tx + c * self.ty
      )

   def scale(self, sx, sy):
      self.a *= sx
      self.b *= sy
      self.c *= sx
      self.d *= sy
      self.tx *= sx
      self.ty *= sy

   def setTo(self, aa, ba, ca, da, txa, tya):
      self.a = aa
      self.b = ba
      self.c = ca
      self.d = da
      self.tx = txa
      self.ty = tya

   def toString(self):
      return f'(a={self.a}, b={self.b}, c={self.c}, d={self.d}, tx={self.tx}, ty={self.ty})'

   def transformPoint(self, point: Point):
      return Point(self.a * point.x + self.c * point.y + self.tx, self.b * point.x + self.d * point.y + self.ty)

   def translate(self, dx, dy):
      self.tx += dx
      self.ty += dy


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

   def copyFrom(self, sourcePoint: Point):
      self.setTo(sourcePoint.x, sourcePoint.y)

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


class Vector3D(Object):
   @property
   def length(self):
      return Math.sqrt(self.x**2 + self.y**2 + self.z**2)

   @property
   def lengthSquared(self):
      return self.x**2 + self.y**2 + self.z**2

   @property
   def w(self):
      return self._w

   @w.setter
   def w(self, value):
      self._w = value

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

   @property
   def z(self):
      return self._z

   @z.setter
   def z(self, value):
      self._z = value

   def __init__(self, x=0, y=0, z=0, w=0):
      self._w = w
      self._x = x
      self._y = y
      self._z = z

   def add(self, a: Vector3D):
      # The documentation does not mention w
      return Vector3D(a.x + self.x, a.y + self.y, a.z + self.z)

   @staticmethod
   def angleBetween(a: Vector3D, b: Vector3D):
      return Math.acos((a.x * b.x + a.y * b.y + a.z * b.z) / (a.length * b.length))

   def clone(self):
      return Vector3D(self.x, self.y, self.z, self.w)

   def copyFrom(self, sourceVector: Vector3D):
      self.w = sourceVector.w
      self.x = sourceVector.x
      self.y = sourceVector.y
      self.z = sourceVector.z

   def crossProduct(self, a: Vector3D):...
   def decrementBy(self, a: Vector3D):...
   @staticmethod
   def distance(pt1: Vector3D, pt2: Vector3D):...
   def dotProduct(self, a: Vector3D):...
   def equals(self, toCompare: Vector3D, allFour=False):
      value = self.x == toCompare.x and self.y == toCompare.y and self.z == toCompare.z
      if allFour:
         return value and self.w == toCompare.w
      return value

   def incrementBy(self, a: Vector3D):...
   def nearEquals(self, toCompare: Vector3D, tolerance, allFour=False):...
   def negate(self):
      self.x = -self.x
      self.y = -self.y
      self.z = -self.z

   def normalize(self):
      len = self.length
      self.x /= len
      self.y /= len
      self.z /= len

   def project(self):
      self.x /= self.w
      self.y /= self.w
      self.z /= self.w

   def scaleBy(self, s):
      self.x *= s
      self.y *= s
      self.z *= s

   def setTo(self, xa, ya, za):
      self.x = xa
      self.y = ya
      self.z = za

   def subtract(self, a: Vector3D):
      # The documentation does not mention w
      return Vector3D(a.x - self.x, a.y - self.y, a.z - self.z)

   def toString(self):
      return f'Vector3D({self.x}, {self.y}, {self.z})'


Vector3D.X_AXIS = Vector3D(x=1)
Vector3D.Y_AXIS = Vector3D(y=1)
Vector3D.Z_AXIS = Vector3D(z=1)
