from __future__ import annotations  # Allow forward references
from as3lib import (Boolean, false, Math, null, Number, Object, String,
                    TypeError, true, uint, undefined, Vector)


class ColorTransform(Object):
    # TODO: rgb property/variable
    @property
    def alphaMultiplier(self):
        return self._alphaM

    @alphaMultiplier.setter
    def alphaMultiplier(self, value: Number):
        self._alphaM = Number(value)

    @property
    def alphaOffset(self):
        return self._alphaO

    @alphaOffset.setter
    def alphaOffset(self, value: Number):
        self._alphaO = Number(value)

    @property
    def blueMultiplier(self):
        return self._blueM

    @blueMultiplier.setter
    def blueMultiplier(self, value: Number):
        self._blueM = Number(value)

    @property
    def blueOffset(self):
        return self._blueO

    @blueOffset.setter
    def blueOffset(self, value: Number):
        self._blueO = Number(value)

    @property
    def color(self):
        return uint(self.redOffset << 16 | self.greenOffset << 8 | self.blueOffset)

    @color.setter
    def color(self, value: uint):
        value = uint(value)
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
    def greenMultiplier(self, value: Number):
        self._greenM = Number(value)

    @property
    def greenOffset(self):
        return self._greenO

    @greenOffset.setter
    def greenOffset(self, value: Number):
        self._greenO = Number(value)

    @property
    def redMultiplier(self):
        return self._redM

    @redMultiplier.setter
    def redMultiplier(self, value: Number):
        self._redM = Number(value)

    @property
    def redOffset(self):
        return self._redO

    @redOffset.setter
    def redOffset(self, value: Number):
        self._redO = Number(value)

    def __init__(self, redMultiplier: Number = 1.0,
                 greenMultiplier: Number = 1.0, blueMultiplier: Number = 1.0,
                 alphaMultiplier: Number = 1.0, redOffset: Number = 0,
                 greenOffset: Number = 0, blueOffset: Number = 0,
                 alphaOffset: Number = 0):
        self.redMultiplier = redMultiplier
        self.greenMultiplier = greenMultiplier
        self.blueMultiplier = blueMultiplier
        self.alphaMultiplier = alphaMultiplier
        self.redOffset = redOffset
        self.greenOffset = greenOffset
        self.blueOffset = blueOffset
        self.alphaOffset = alphaOffset

    def concat(self, second: ColorTransform = null):
        if second is null:
            return
        raise NotImplementedError

    def toString(self):
        return String('(redMultiplier=%s, greenMultiplier=%s, blueMultiplier=%s, alphaMultiplier=%s, redOffset=%s, greenOffset=%s, blueOffset=%s, alphaOffset=%s)' % (self._redM, self._greenM, self._blueM, self._alphaM, self._redO, self._greenO, self._blueO, self._alphaO))


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
    def a(self, value: Number):
        self._a = Number(value)

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value: Number):
        self._b = Number(value)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value: Number):
        self._c = Number(value)

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value: Number):
        self._d = Number(value)

    @property
    def tx(self):
        return self._tx

    @tx.setter
    def tx(self, value: Number):
        self._tx = Number(value)

    @property
    def ty(self):
        return self._ty

    @ty.setter
    def ty(self, value: Number):
        self._ty = Number(value)

    def __init__(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.tx = tx
        self.ty = ty

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

    def copyColumnFrom(self, column: uint, vector3D: Vector3D):
        # NOTE: According to the tests, copyColumnFrom is supposed to do the
        # same thing as copyRowFrom. This doesn't make sense but the test passes
        # on flash player so it must be right.
        self.copyRowFrom(column, vector3D)

    def copyColumnTo(self, column: uint, vector3D: Vector3D):
        column = uint(column)
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

    def copyRowFrom(self, row: uint, vector3D: Vector3D):
        temp = (vector3D.x, vector3D.y, vector3D.z)
        row = uint(row)
        if row == 0:
            self.a, self.c, self.tx = temp
        elif row == 1:
            self.b, self.d, self.ty = temp

    def copyRowTo(self, row: uint, vector3D: Vector3D):
        row = uint(row)
        if row == 0:
            vector3D.setTo(self.a, self.c, self.tx)
        elif row == 1:
            vector3D.setTo(self.b, self.d, self.ty)
        elif row == 2:
            vector3D.setTo(0.0, 0.0, 1.0)

    def createBox(self, scaleX: Number, scaleY: Number, rotation: Number = 0,
                  tx: Number = 0, ty: Number = 0):
        scaleX = Number(scaleX)
        scaleY = Number(scaleY)
        rotation = Number(rotation)
        tx = Number(tx)
        ty = Number(ty)
        self.identity()
        self.rotate(rotation)
        self.scale(scaleX, scaleY)
        self.translate(tx, ty)

    def createGradientBox(self, width: Number, height: Number,
                          rotation: Number = 0, tx: Number = 0,
                          ty: Number = 0):
        width = Number(width)
        height = Number(height)
        rotation = Number(rotation)
        tx = Number(tx)
        ty = Number(ty)
        self.createBox(width / 1638.4, height / 1638.4, rotation, tx + width / 2, ty + height / 2)

    def deltaTransformPoint(self, point: Point):
        return Point(self.a * point.x + self.c * point.y, self.b * point.x + self.d * point.y)

    def identity(self):
        self.a, self.b, self.c, self.d, self.tx, self.ty = 1, 0, 0, 1, 0, 0

    def invert(self):
        det = self.a * self.d - self.c * self.b

        self.setTo(
            self.d / det,
            self.b / -det,
            self.c / -det,
            self.a / det,
            (self.d * self.tx - self.c * self.ty) / -det,
            (self.b * self.tx - self.a * self.ty) / det
        )

    def rotate(self, angle: Number):
        angle = Number(angle)
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

    def scale(self, sx: Number, sy: Number):
        sx = Number(sx)
        sy = Number(sy)
        self.a *= sx
        self.b *= sy
        self.c *= sx
        self.d *= sy
        self.tx *= sx
        self.ty *= sy

    def setTo(self, aa: Number, ba: Number, ca: Number, da: Number,
              txa: Number, tya: Number):
        self.a = aa
        self.b = ba
        self.c = ca
        self.d = da
        self.tx = txa
        self.ty = tya

    def toString(self):
        return String(f'(a={self.a}, b={self.b}, c={self.c}, d={self.d}, tx={self.tx}, ty={self.ty})')

    def transformPoint(self, point: Point):
        return Point(self.a * point.x + self.c * point.y + self.tx, self.b * point.x + self.d * point.y + self.ty)

    def translate(self, dx: Number, dy: Number):
        self.tx += Number(dx)
        self.ty += Number(dy)


class Matrix3D(Object):
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
    def position(self, value: Vector3D):
        self._data[12] = value.x
        self._data[13] = value.y
        self._data[14] = value.z

    @property
    def rawData(self):
        return self._data

    @rawData.setter
    def rawData(self, value: Vector[Number]):
        if not isinstance(value, Vector):
            raise TypeError
        if value.length != 16:
            raise
        self._data = value

    def __init__(self, v: Vector[Number] = null):
        if not (isinstance(v, Vector) or v is null):
            raise TypeError
        if v is not null and v.length == 16:
            self._data = v
        else:
            self.identity()

    def append(self, lhs: Matrix3D):
        raise NotImplementedError

    def appendRotation(self, degrees: Number, axis: Vector3D, pivotPoint: Vector3D = null):
        raise NotImplementedError

    def appendScale(self, xScale: Number, yScale: Number, zScale: Number):
        raise NotImplementedError

    def appendTranslation(self, x: Number, y: Number, z: Number):
        raise NotImplementedError

    def clone(self):
        return Matrix3D(Vector[Number](self.rawData))

    def copyColumnFrom(self, column: uint, vector3D: Vector3D):
        raise NotImplementedError

    def copyColumnTo(self, column: uint, vector3D: Vector3D):
        raise NotImplementedError

    def copyFrom(self, sourceMatrix3D: Matrix3D):
        raise NotImplementedError

    def copyRawDataFrom(self, vector: Vector[Number], index: uint = 0, transpose: Boolean = false):
        raise NotImplementedError

    def copyRawDataTo(self, vector: Vector[Number], index: uint = 0, transpose: Boolean = false):
        raise NotImplementedError

    def copyRowFrom(self, row: uint, vector3D: Vector3D):
        raise NotImplementedError

    def copyRowTo(self, row: uint, vector3D: Vector3D):
        raise NotImplementedError

    def copyToMatrix(self, dest: Matrix3D):
        raise NotImplementedError

    def decompose(self, orientationStyle: String = 'eulerAngles'):
        raise NotImplementedError

    def deltaTransformVector(self, v: Vector3D):
        raise NotImplementedError

    def identity(self):
        self._data = Vector[Number]([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])

    @staticmethod
    def interpolate(thisMat: Matrix3D, toMat: Matrix3D, percent: Number):
        raise NotImplementedError

    def interpolateTo(self, toMat: Matrix3D, percent: Number):
        raise NotImplementedError

    def invert(self):
        raise NotImplementedError

    def pointAt(self, pos: Vector3D, at: Vector3D = null, up: Vector3D = null):
        raise NotImplementedError

    def prepend(self, rhs: Matrix3D):
        raise NotImplementedError

    def prependRotation(self, degrees: Number, axis: Vector3D, pivotPoint: Vector3D = null):
        raise NotImplementedError

    def prependScale(self, xScale: Number, yScale: Number, zScale: Number):
        raise NotImplementedError

    def prependTranslation(self, x: Number, y: Number, z: Number):
        raise NotImplementedError

    def recompose(self, components: Vector[Vector3D], orientationStyle: String = 'eulerAngles'):
        raise NotImplementedError

    def transformVector(self, v: Vector3D):
        raise NotImplementedError

    def transformVectors(self, vin: Vector[Number], vout: Vector[Number]):
        raise NotImplementedError

    def transpose(self):
        raise NotImplementedError


class Orientation3D(Object):
    AXIS_ANGLE = String('axisAngle')
    EULER_ANGLES = String('eulerAngles')
    QUATERNION = String('quanternion')


class PerspectiveProjection(Object):
    @property
    def fieldOfView(self):
        return self._fov

    @fieldOfView.setter
    def fieldOfView(self, value: Number):
        value = Number(value)
        if value < 0 or value > 180:
            raise
        self._fov = value

    @property
    def focalLength(self):
        return self._fLen

    @focalLength.setter
    def focalLength(self, value: Number):
        self._fLen = Number(value)

    @property
    def projectionCenter(self):
        return self._pC

    @projectionCenter.setter
    def projectionCenter(self, value: Point):
        if not isinstance(value, Point):
            raise TypeError
        self._pC = value

    def __init__(self):
        self.fieldOfView = 55
        self.focalLength = 480.24554443359375
        self.projectionCenter = Point(250, 250)  # TODO: Calculate centre of object this is in

    def toMatrix3D(self):
        raise NotImplementedError


class Point(Object):
    @property
    def length(self):
        return Math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: Number):
        self._x = Number(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: Number):
        self._y = Number(value)

    def __init__(self, x: Number = 0, y: Number = 0):
        self.x = x
        self.y = y

    def add(self, v: Point):
        return Point(self.x + v.x, self.y + v.y)

    def clone(self):
        return Point(self.x, self.y)

    def copyFrom(self, sourcePoint: Point):
        self.setTo(sourcePoint.x, sourcePoint.y)

    @staticmethod
    def distance(pt1: Point, pt2: Point):
        return Math.sqrt((pt2.x - pt1.x) ** 2 + (pt2.y - pt1.y) ** 2)

    def equals(self, toCompare: Point):
        return self.x == toCompare.x and self.y == toCompare.y

    @staticmethod
    def interpolate(pt1: Point, pt2: Point, f: Number):
        f = Number(f)
        return Point(pt2.x + f * (pt1.x - pt2.x), pt2.y + f * (pt1.y - pt2.y))

    def normalize(self, thickness: Number):
        # TODO: Handle NaN, undefined, and null for x and y
        thickness = Number(thickness)
        norm_magnitude = Number(1) / self.length
        if self.x == 0:
            x = 0
        else:
            x = self.x * norm_magnitude * thickness
        if self.y == 0:
            y = 0
        else:
            y = self.y * norm_magnitude * thickness
        self.setTo(x, y)

    def offset(self, dx: Number, dy: Number):
        self.x += Number(dx)
        self.y += Number(dy)

    @staticmethod
    def polar(len: Number, angle: Number):
        len = Number(len)
        angle = Number(angle)
        return Point(len * Math.cos(angle), len * Math.sin(angle))

    def setTo(self, xa: Number, ya: Number):
        self.x = xa
        self.y = ya

    def subtract(self, v: Point):
        return Point(self.x - v.x, self.y - v.y)

    def toString(self):
        return String('(x=%s, y=%s)' % (self.x, self.y))


class Rectangle(Object):
    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, value: Number):
        self.height = Number(value) - self.y

    @property
    def bottomRight(self):
        return Point(self.x + self.width, self.y + self.height)

    @bottomRight.setter
    def bottomRight(self, value: Point):
        raise NotImplementedError

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: Number):
        self._height = Number(value)

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value: Number):
        raise NotImplementedError

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value: Number):
        self.width = Number(value) - self.x

    @property
    def size(self):
        return Point(self.width, self.height)

    @size.setter
    def size(self, value: Point):
        self.width = value.x
        self.height = value.y

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value: Number):
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
    def width(self, value: Number):
        self._width = Number(value)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: Number):
        self._x = Number(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: Number):
        self._y = Number(value)

    def __init__(self, x: Number = 0, y: Number = 0, width: Number = 0, height: Number = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def clone(self):
        return Rectangle(self.x, self.y, self.width, self.height)

    def contains(self, x: Number, y: Number):
        x, y = Number(x), Number(y)
        return x >= self.x and x < self.right and y >= self.y and y < self.bottom

    def containsPoint(self, point: Point):
        return self.contains(point.x, point.y)

    def containsRect(self, rect: Rectangle):
        # TODO: Ensure that this is correct
        return self.containsPoint(rect.topLeft) and self.containsPoint(rect.bottomRight)

    def copyFrom(self, sourceRect: Rectangle):
        self.x = sourceRect.x
        self.y = sourceRect.y
        self.width = sourceRect.width
        self.height = sourceRect.height

    def equals(self, toCompare: Rectangle):
        return self.x == toCompare.x and self.y == toCompare.y and self.width == toCompare.width and self.height == toCompare.height

    def inflate(self, dx: Number, dy: Number):
        raise NotImplementedError

    def inflatePoint(self, point: Point):
        raise NotImplementedError

    def intersection(self, toIntersect: Rectangle):
        raise NotImplementedError

    def intersects(self, toIntersect: Rectangle):
        raise NotImplementedError

    def isEmpty(self):
        return self.width <= 0 or self.height <= 0

    def offset(self, dx: Number, dy: Number):
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
        return undefined

    def setTo(self, xa: Number, ya: Number, widtha: Number, heighta: Number):
        self.x = xa
        self.y = ya
        self.width = widtha
        self.height = heighta
        return undefined

    def toString(self):
        return String(f'(x={self.x}, y={self.y}, w={self.width}, h={self.height})')

    def union(self, toUnion: Rectangle):
        raise NotImplementedError


class Transform(Object):
    @property
    def colorTransform(self):
        return self._ct

    @colorTransform.setter
    def colorTransform(self, value: ColorTransform):
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
    def matrix(self, value: Matrix):
        if not isinstance(value, Matrix):
            raise TypeError
        self._matrix = value

    @property
    def matrix3D(self):
        return self._matrix3D

    @matrix3D.setter
    def matrix3D(self, value: Matrix3D):
        if not isinstance(value, Matrix3D):
            raise TypeError
        self._matrix3D = value

    @property
    def perspectiveProjection(self):
        return self._pp

    @perspectiveProjection.setter
    def perspectiveProjection(self, value: PerspectiveProjection):
        if not isinstance(value, PerspectiveProjection):
            raise TypeError
        self._pp = value

    @property
    def pixelBounds(self):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def getRelativeMatrix3D(self, relativeTo):
        raise NotImplementedError


class Utils3D(Object):
    @staticmethod
    def pointTowards(percent: Number, mat: Matrix3D, pos: Vector3D, at: Vector3D = null, up: Vector3D = null) -> Matrix3D:
        raise NotImplementedError

    @staticmethod
    def projectVector(m: Matrix3D, v: Vector3D) -> Vector3D:
        raise NotImplementedError

    @staticmethod
    def projectVectors(m: Matrix3D, verts: Vector[Number], projectedVerts: Vector[Number], uvts: Vector[Number]) -> None:
        raise NotImplementedError


class Vector3D(Object):
    @property
    def length(self):
        return Math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def lengthSquared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value: Number):
        self._w = Number(value)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: Number):
        self._x = Number(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: Number):
        self._y = Number(value)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value: Number):
        self._z = Number(value)

    def __init__(self, x: Number = 0, y: Number = 0, z: Number = 0, w: Number = 0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

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
        return Math.sqrt((pt2.x - pt1.x) ** 2 + (pt2.y - pt1.y) ** 2 + (pt2.z - pt1.z) ** 2)

    def dotProduct(self, a: Vector3D):
        raise NotImplementedError

    def equals(self, toCompare: Vector3D, allFour: Boolean = false):
        value = self.x == toCompare.x and self.y == toCompare.y and self.z == toCompare.z
        if Boolean(allFour):
            return Boolean(value and self.w == toCompare.w)
        return Boolean(value)

    def incrementBy(self, a: Vector3D):
        self.x += a.x
        self.y += a.y
        self.z += a.z

    def nearEquals(self, toCompare: Vector3D, tolerance: Number, allFour: Boolean = false):
        # TODO: allFour
        # NOTE: Can't use math.isclose here because it doesn't function the same
        tolerance = Number(tolerance)
        if Boolean(allFour):
            raise NotImplementedError
        if tolerance == 0:
            return false
        if (abs(self.x - toCompare.x) > tolerance or
            abs(self.y - toCompare.y) > tolerance or
            abs(self.z - toCompare.z) > tolerance):
            return false
        return true

    def negate(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def normalize(self):
        len = self.length
        self.x = 0 if self.x == 0 else self.x / len
        self.y = 0 if self.y == 0 else self.y / len
        self.z = 0 if self.z == 0 else self.z / len
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
        return String('(x=%s, y=%s, z=%s)' % (self.x, self.y, self.z))


Vector3D.X_AXIS = Vector3D(x=1)
Vector3D.Y_AXIS = Vector3D(y=1)
Vector3D.Z_AXIS = Vector3D(z=1)
