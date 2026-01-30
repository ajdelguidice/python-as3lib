from __future__ import annotations  # Allow forward references
from as3lib import Math, Number, Object, Vector, null, TypeError
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
      self._a = Number(value)

   @property
   def b(self):
      return self._b

   @b.setter
   def b(self, value):
      self._b = Number(value)

   @property
   def c(self):
      return self._c

   @c.setter
   def c(self, value):
      self._c = Number(value)

   @property
   def d(self):
      return self._d

   @d.setter
   def d(self, value):
      self._d = Number(value)

   @property
   def tx(self):
      return self._tx

   @tx.setter
   def tx(self, value):
      self._tx = Number(value)

   @property
   def ty(self):
      return self._ty

   @ty.setter
   def ty(self, value):
      self._ty = Number(value)

   def __init__(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
      self._a = Number(a)
      self._b = Number(b)
      self._c = Number(c)
      self._d = Number(d)
      self._tx = Number(tx)
      self._ty = Number(ty)

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
      self.a = Number(aa)
      self.b = Number(ba)
      self.c = Number(ca)
      self.d = Number(da)
      self.tx = Number(txa)
      self.ty = Number(tya)

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

   @staticmethod
   def _3x3Det(a, b, c, d, e, f, g, h, i):
      '''
      | a b c |
      | d e f |
      | g h i |
      '''
      return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

   @property
   def determinant(self):
      return self._data[0] * (self._3x3Det(self._data[5], self._data[9], self._data[13], self._data[6], self._data[10], self._data[14], self._data[7], self._data[11], self._data[15])) - self._data[4] * (self._3x3Det(self._data[1], self._data[9], self._data[13], self._data[2], self._data[10], self._data[14], self._data[3], self._data[11], self._data[15])) + self._data[8] * (self._3x3Det(self._data[1], self._data[5], self._data[13], self._data[2], self._data[6], self._data[14], self._data[3], self._data[7], self._data[15])) - self._data[12] * (self._3x3Det(self._data[1], self._data[5], self._data[9], self._data[2], self._data[6], self._data[10], self._data[3], self._data[7], self._data[11]))

   @property
   def position(self):
      return Vector3D(self._data[12], self._data[13], self._data[14])

   @position.setter
   def position(self, value):
      self._data[12] = value.x
      self._data[13] = value.y
      self._data[14] = value.z

   @property
   def rawData(self):
      return self._data

   @rawData.setter
   def rawData(self, value):
      if not isinstance(value, Vector):
         raise TypeError
      if value.length != 16:
         raise
      self._data = value

   def _identity(self):
      # TODO: Should be Vector.<Number>
      return Vector.Number([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])

   def __init__(self, v = null):
      if not (isinstance(v, Vector) or v is null):
         raise TypeError
      if v is not null and v.length == 16:
         self._data = v
      else:
         self._data = self._identity()

   def append(self, lhs:Matrix3D):
      raise NotImplementedError

   def appendRotation(self, degrees, axis, pivotPoint=null):
      raise NotImplementedError

   def appendScale(self, xScale, yScale, zScale):
      raise NotImplementedError

   def appendTranslation(self, x, y, z):
      raise NotImplementedError

   def clone(self):
      # TODO: Make this not cause rawData to be linked between the two
      return Matrix3D(self.rawData)

   def copyColumnFrom(self, column, vector3D:Vector3D):
      raise NotImplementedError

   def copyColumnTo(self, column, vector3D:Vector3D):
      raise NotImplementedError

   def copyFrom(self, sourceMatrix3D):
      raise NotImplementedError

   def copyRawDataFrom(self, vector, index=0, transpose=False):
      raise NotImplementedError

   def copyRawDataTo(self, vector, index=0, transpose=False):
      raise NotImplementedError

   def copyRowFrom(self, row, vector3D:Vector3D):
      raise NotImplementedError

   def copyRowTo(self, row, vector3D:Vector3D):
      raise NotImplementedError

   def copyToMatrix(self, dest):
      raise NotImplementedError

   def decompose(self, orientationStyle = 'eulerAngles'):
      raise NotImplementedError

   def deltaTransformVector(self, v:Vector3D):
      raise NotImplementedError

   def identity(self):
      self._data = self._identity()

   @staticmethod
   def interpolate(thisMat:Matrix3D, toMat:Matrix3D, percent):
      raise NotImplementedError

   def interpolateTo(self, toMat:Matrix3D, percent):
      raise NotImplementedError

   def invert(self):
      raise NotImplementedError

   def pointAt(self, pos:Vector3D, at: Vector3D = null, up: Vecto3D = null):
      raise NotImplementedError

   def prepend(self, rhs:Matrix3D):
      raise NotImplementedError

   def prependRotation(self, degrees, axis, pivotPoint=null):
      raise NotImplementedError

   def prependScale(self, xScale, yScale, zScale):
      raise NotImplementedError

   def prependTranslation(self, x, y, z):
      raise NotImplementedError

   def recompose(self, components, orientationStyle = 'eulerAngles'):
      raise NotImplementedError

   def transformVector(self, v:Vector3D):
      raise NotImplementedError

   def transformVectors(self, vin, vout):
      raise NotImplementedError

   def transpose(self):
      raise NotImplementedError


class Orientation3D(metaclass=_AS3_CONSTANTSOBJECT):
   AXIS_ANGLE = 'axisAngle'
   EULER_ANGLES = 'eulerAngles'
   QUATERNION = 'quanternion'


class PerspectiveProjection(Object):
   @property
   def fieldOfView(self):
      return self._fov

   @fieldOfView.setter
   def fieldOfView(self, value):
      if value < 0 or value > 180:
         raise
      self._fov = value

   @property
   def focalLength(self):
      return self._fLen

   @focalLength.setter
   def focalLength(self, value):
      self._fLen = value

   @property
   def projectionCenter(self):
      return self._pC

   @projectionCenter.setter
   def projectionCenter(self, value):
      if not isinstance(value, Point):
         raise TypeError
      self._pC = value

   def __init__(self):
      self._fov = 55
      self._fLen = 480.24554443359375
      self._pC = Point(250, 250)  # TODO: Calculate centre of object this is in

   def toMatrix3D(self):
      raise NotImplementedError



class Point(Object):
   @property
   def length(self):
      return math.sqrt(self.x ** 2 + self.y ** 2)

   @property
   def x(self):
      return self._x

   @x.setter
   def x(self, value):
      self._x = Number(value)

   @property
   def y(self):
      return self._y

   @y.setter
   def y(self, value):
      self._y = Number(value)

   def __init__(self, x=0, y=0):
      self._x = Number(x)
      self._y = Number(y)

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
   def interpolate(pt1: Point, pt2: Point, f):
      raise NotImplementedError

   def normalize(self, thickness):
      raise NotImplementedError

   def offset(self, dx, dy):
      self.x = self.x + dx
      self.y = self.y + dy

   @staticmethod
   def polar(len, angle):
      return Point(len * math.cos(angle), len * math.sin(angle))

   def setTo(self, xa, ya):
      self.x = Number(xa)
      self.y = Number(ya)

   def subtract(self, v: Point):
      return Point(self.x - v.x, self.y - v.y)

   def toString(self):
      return '(x=%s, y=%s)' % (self.x, self.y)


class Rectangle(Object):
   @property
   def bottom(self):
      return self.y + self.height

   @bottom.setter
   def bottom(self, value):
      self.height = value - self.y

   @property
   def bottomRight(self):
      raise NotImplementedError

   @property
   def height(self):
      return self._height

   @height.setter
   def height(self, value):
      self._height = value

   @property
   def left(self):
      raise NotImplementedError

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
   def top(self):
      raise NotImplementedError

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

   def containsRect(self, rect: Rectangle):
      raise NotImplementedError

   def copyFrom(self, sourceRect: Rectangle):
      self.x = sourceRect.x
      self.y = sourceRect.y
      self.width = sourceRect.width
      self.height = sourceRect.height

   def equals(self, toCompare: Rectangle):
      return self.x == toCompare.x and self.y == toCompare.y and self.width == toCompare.width and self.height == toCompare.height

   def inflate(self, dx, dy):
      raise NotImplementedError

   def inflatePoint(self, point: Point):
      raise NotImplementedError

   def intersection(self, toIntersect: Rectangle):
      raise NotImplementedError

   def intersects(self, toIntersect: Rectangle):
      raise NotImplementedError

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
      raise NotImplementedError


class Transform(Object):
   @property
   def colorTransform(self):
      return self._ct

   @colorTransform.setter
   def colorTransform(self, value):
      if not isinstance(value, ColorTransform):
         raise TypeError
      self._ct = value

   @property
   def concatenatedColorTransform(self):
      raise NotImplementedError

   @property
   def concatenatedMatrix(self):
      raise NotImplementedError

   @property
   def matrix(self):
      return self._matrix

   @matrix.setter
   def matrix(self, value):
      if not isinstance(value, Matrix):
         raise TypeError
      self._matrix = value

   @property
   def matrix3D(self):
      return self._matrix3D

   @matrix3D.setter
   def matrix3D(self, value):
      if not isinstance(value, Matrix3D):
         raise TypeError
      self._matrix3D = value

   @property
   def perspectiveProjection(self):
      return self._pp

   @perspectiveProjection.setter
   def perspectiveProjection(self, value):
      if not isinstance(value, PerspectiveProjection):
         raise TypeError
      self._pp = value

   @property
   def pixelBounds(self):
      raise NotImplementedError

   def __init__(self):
      raise NotImplementedError

   def getRelativeMatrix3D(relativeTo):
      raise NotImplementedError


class Utils3D(Object):
   @staticmethod
   def pointTowards(percent:Number, mat:Matrix3D, pos:Vector3D, at:Vector3D=null, up:Vector3D=null) -> Matrix3D:
      raise NotImplementedError

   @staticmethod
   def projectVector(m:Matrix3D, v:Vector3D) -> Vector3D:
      raise NotImplementedError

   @staticmethod
   def projectVectors(m:Matrix3D, verts:Vector, projectedVerts:Vector, uvts:Vector) -> None:
      raise NotImplementedError


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
      self._w = Number(value)

   @property
   def x(self):
      return self._x

   @x.setter
   def x(self, value):
      self._x = Number(value)

   @property
   def y(self):
      return self._y

   @y.setter
   def y(self, value):
      self._y = Number(value)

   @property
   def z(self):
      return self._z

   @z.setter
   def z(self, value):
      self._z = Number(value)

   def __init__(self, x=0, y=0, z=0, w=0):
      self._w = Number(w)
      self._x = Number(x)
      self._y = Number(y)
      self._z = Number(z)

   def add(self, a: Vector3D):
      # The documentation does not mention w
      return Vector3D(a.x + self.x, a.y + self.y, a.z + self.z)

   @staticmethod
   def angleBetween(a: Vector3D, b: Vector3D):
      return Math.acos((a.x * b.x + a.y * b.y + a.z * b.z) / (a.length * b.length))

   def clone(self):
      return Vector3D(self.x, self.y, self.z, self.w)

   def copyFrom(self, sourceVector: Vector3D):
      self.x = sourceVector.x
      self.y = sourceVector.y
      self.z = sourceVector.z

   def crossProduct(self, a: Vector3D):
      raise NotImplementedError

   def decrementBy(self, a: Vector3D):
      self.x -= a.x
      self.y -= a.y
      self.z -= a.z

   @staticmethod
   def distance(pt1: Vector3D, pt2: Vector3D):
      raise NotImplementedError

   def dotProduct(self, a: Vector3D):
      raise NotImplementedError

   def equals(self, toCompare: Vector3D, allFour=False):
      value = self.x == toCompare.x and self.y == toCompare.y and self.z == toCompare.z
      if allFour:
         return value and self.w == toCompare.w
      return value

   def incrementBy(self, a: Vector3D):
      self.x += a.x
      self.y += a.y
      self.z += a.z

   def nearEquals(self, toCompare: Vector3D, tolerance, allFour=False):
      raise NotImplementedError

   def negate(self):
      self.x = -self.x
      self.y = -self.y
      self.z = -self.z

   def normalize(self):
      len = self.length
      self.x /= len
      self.y /= len
      self.z /= len
      return len

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
      return Vector3D(self.x - a.x, self.y - a.y, self.z - a.z)

   def toString(self):
      return '(x=%s, y=%s, z=%s)' % (self.x, self.y, self.z)


Vector3D.X_AXIS = Vector3D(x=1)
Vector3D.Y_AXIS = Vector3D(y=1)
Vector3D.Z_AXIS = Vector3D(z=1)
