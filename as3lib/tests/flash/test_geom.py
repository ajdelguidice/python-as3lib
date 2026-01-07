import as3lib
from as3lib import ArgumentError, Math, RangeError, TypeError, Vector
from as3lib.flash.display import Sprite, MovieClip
from as3lib.flash.geom import Matrix, Matrix3D, PerspectiveProjection, Point, Utils3D, Vector3D
from as3lib.tests import as3libTestCase, TestNotImplemented


class MatrixTests(as3libTestCase):
   def test_constructor(self):
      self.assertMatrix(Matrix(), 1, 0, 0, 1, 0, 0)
      self.assertMatrix(Matrix(1), 1, 0, 0, 1, 0, 0)
      self.assertMatrix(Matrix(1, 2), 1, 2, 0, 1, 0, 0)
      self.assertMatrix(Matrix(1, 2, 3), 1, 2, 3, 1, 0, 0)
      self.assertMatrix(Matrix(1, 2, 3, 4), 1, 2, 3, 4, 0, 0)
      self.assertMatrix(Matrix(1, 2, 3, 4, 5), 1, 2, 3, 4, 5, 0)
      self.assertMatrix(Matrix(1, 2, 3, 4, 5, 6), 1, 2, 3, 4, 5, 6)

   def test_indentity(self):
      matrix = Matrix(1, 2, 3, 4, 5, 6)
      matrix.identity()
      self.assertMatrix(matrix, 1, 0, 0, 1, 0, 0)

   def test_clone(self):
      matrix = Matrix(1, 2, 3, 4, 5, 6)
      cloned = matrix.clone()

      self.assertMatrix(cloned, 1, 2, 3, 4, 5, 6)
      self.assertIsNot(cloned, matrix)

   def test_scale(self):
      matrix = Matrix()
      matrix.scale(3, 5)
      self.assertMatrix(matrix, 3, 0, 0, 5, 0, 0)

      matrix = Matrix(2, 0, 0, 2, 100, 100)
      matrix.scale(7, 11)
      self.assertMatrix(matrix, 14, 0, 0, 22, 700, 1100)

      matrix = Matrix(1, 2, 3, 4, 5, 6)
      matrix.scale(13, 17)
      self.assertMatrix(matrix, 13, 34, 39, 68, 65, 102)

   def test_rotate(self):
      matrix = Matrix()
      matrix.rotate(0)
      self.assertMatrix(matrix, 1, 0, 0, 1, 0, 0)

      matrix = Matrix()
      matrix.rotate(0.5)
      self.assertMatrix(matrix, 0.8775825618903728, 0.479425538604203, -0.479425538604203, 0.8775825618903728, 0, 0)

      matrix = Matrix(1, 2, 3, 4, 5, 6)
      matrix.rotate(0)
      self.assertMatrix(matrix, 1, 2, 3, 4, 5, 6)

      matrix = Matrix(1, 2, 3, 4, 5, 6)
      matrix.rotate((90/180)*Math.PI)
      self.assertMatrix(matrix, -2, 1.0000000000000002, -4, 3.0000000000000004, -6, 5)

   def test_translate(self):
      matrix = Matrix()
      matrix.translate(3, 5)
      self.assertMatrix(matrix, 1, 0, 0, 1, 3, 5)

      matrix = Matrix(2, 0, 0, 2, 100, 100)
      matrix.translate(7, 11)
      self.assertMatrix(matrix, 2, 0, 0, 2, 107, 111)

   def test_invert(self):
      matrix = Matrix()
      matrix.invert()
      self.assertMatrix(matrix, 1, 0, 0, 1, 0, 0)

      matrix = Matrix(2, 3, 5, 7, 9, 11)
      matrix.invert()
      self.assertMatrix(matrix, -7, 3, 5, -2, 8, -5)

   def test_createBox(self):
      matrix = Matrix()
      matrix.createBox(2, 3)
      self.assertMatrix(matrix, 2, 0, 0, 3, 0, 0)

      matrix.createBox(2, 3, 0)
      self.assertMatrix(matrix, 2, 0, 0, 3, 0, 0)

      matrix.createBox(2, 3, 5)
      self.assertMatrix(matrix, 0.5673243709264525, -2.8767728239894153, 1.917848549326277, 0.8509865563896788, 0, 0)

      matrix.createBox(2, 3, 5, 7)
      self.assertMatrix(matrix, 0.5673243709264525, -2.8767728239894153, 1.917848549326277, 0.8509865563896788, 7, 0)

      matrix.createBox(2, 3, 5, 7, 9)
      self.assertMatrix(matrix, 0.5673243709264525, -2.8767728239894153, 1.917848549326277, 0.8509865563896788, 7, 9)

   def test_createGradientBox(self):
      matrix = Matrix()
      matrix.createGradientBox(200, 300)
      self.assertMatrix(matrix, 0.1220703125, 0, 0, 0.18310546875, 100, 150)

      matrix.createGradientBox(200, 300, 0)
      self.assertMatrix(matrix, 0.1220703125, 0, 0, 0.18310546875, 100, 150)

      matrix.createGradientBox(200, 300, 500)
      self.assertMatrix(matrix, -0.10789175701067846, -0.08565157568160574, 0.05710105045440383, -0.1618376355160177, 100, 150)

      matrix.createGradientBox(200, 300, 500, 700)
      self.assertMatrix(matrix, -0.10789175701067846, -0.08565157568160574, 0.05710105045440383, -0.1618376355160177, 800, 150)

      matrix.createGradientBox(200, 300, 500, 700, 900)
      self.assertMatrix(matrix, -0.10789175701067846, -0.08565157568160574, 0.05710105045440383, -0.1618376355160177, 800, 1050)

   def test_transformPoint(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      point = matrix.transformPoint(Point(1, 1))
      self.assertPoint(point, 18, 23)

   def test_deltaTransformPoint(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      point = matrix.deltaTransformPoint(Point(1, 1))
      self.assertPoint(point, 7, 10)

   def test_copyFrom(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      matrix2 = Matrix()
      self.assertMatrix(matrix2, 1, 0, 0, 1, 0, 0)
      matrix2.copyFrom(matrix)
      self.assertMatrix(matrix2, 2, 3, 5, 7, 11, 13)

   def test_setTo(self):
      matrix = Matrix()
      matrix.setTo(2, 3, 5, 7, 11, 13)
      self.assertMatrix(matrix, 2, 3, 5, 7, 11, 13)

   def test_copyRowTo(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      vector = Vector3D(1, 2, 3, 4)

      matrix.copyRowTo(0, vector)
      self.assertVector3D(vector, 2, 5, 11)

      matrix.copyRowTo(1, vector)
      self.assertVector3D(vector, 3, 7, 13)

      matrix.copyRowTo(2, vector)
      self.assertVector3D(vector, 0, 0, 1)

      matrix.copyRowTo(3, vector)
      self.assertVector3D(vector, 0, 0, 1)

   def test_copyColumnTo(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      vector = Vector3D(1, 2, 3, 4)

      matrix.copyColumnTo(0, vector)
      self.assertVector3D(vector, 2, 3, 0)

      matrix.copyColumnTo(1, vector)
      self.assertVector3D(vector, 5, 7, 0)

      matrix.copyColumnTo(2, vector)
      self.assertVector3D(vector, 11, 13, 1)

      matrix.copyColumnTo(3, vector)
      self.assertVector3D(vector, 11, 13, 1)

   def test_copyRowFrom(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      vector = Vector3D(17, 19, 23, 29)

      matrix.copyRowFrom(0, vector)
      self.assertMatrix(matrix, 17, 3, 19, 7, 23, 13)

      matrix.copyRowFrom(1, vector)
      self.assertMatrix(matrix, 17, 17, 19, 19, 23, 23)

      matrix.copyRowFrom(2, vector)
      self.assertMatrix(matrix, 17, 17, 19, 19, 23, 23)

      matrix.copyRowFrom(3, vector)
      self.assertMatrix(matrix, 17, 17, 19, 19, 23, 23)

   def test_copyColumnFrom(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      vector = Vector3D(17, 19, 23, 29)

      matrix.copyColumnFrom(0, vector)
      self.assertMatrix(matrix, 17, 3, 19, 7, 23, 13)

      matrix.copyColumnFrom(1, vector)
      self.assertMatrix(matrix, 17, 17, 19, 19, 23, 23)

      matrix.copyColumnFrom(2, vector)
      self.assertMatrix(matrix, 17, 17, 19, 19, 23, 23)

      matrix.copyColumnFrom(3, vector)
      self.assertMatrix(matrix, 17, 17, 19, 19, 23, 23)


class MatrixConcatTests(as3libTestCase):
   @classmethod
   def setUpClass(cls):
      cls.matrix = Matrix(11, 13, 17, 19, 23, 29)
      cls.scale = Matrix()
      cls.scale.scale(3, 5)
      cls.translate = Matrix()
      cls.translate.translate(7, 9)
      cls.rotate = Matrix()
      cls.rotate.rotate(Math.PI / 2)

   def test_double(self):
      # Scale + Translate
      result = self.scale.clone()
      result.concat(self.translate)
      self.assertMatrix(result, 3, 0, 0, 5, 7, 9)

      # Translate + Scale
      result = self.translate.clone()
      result.concat(self.scale)
      self.assertMatrix(result, 3, 0, 0, 5, 21, 45)

      # TODO: Fails because python uses one extra digit of precision
      # Scale + Rotate
      result = self.scale.clone()
      result.concat(self.rotate)
      self.assertMatrix(result, 1.836970198721029e-16, 3, -5, 3.0616169978683834e-16, 0, 0)

      # Rotate + Scale
      result = self.rotate.clone()
      result.concat(self.scale)
      self.assertMatrix(result, 1.836970198721029e-16, 5, -3, 3.0616169978683834e-16, 0, 0)

      # Translate + Rotate
      result = self.translate.clone()
      result.concat(self.rotate)
      self.assertMatrix(result, 6.123233995736766e-17, 1, -1, 6.123233995736766e-17, -9, 7.000000000000001)

      # Rotate + Translate
      result = self.rotate.clone()
      result.concat(self.translate)
      self.assertMatrix(result, 6.123233995736766e-17, 1, -1, 6.123233995736766e-17, 7, 9)

   def test_triple(self):
      # Scale + Translate + Rotate
      result = self.scale.clone()
      result.concat(self.translate)
      result.concat(self.rotate)
      self.assertMatrix(result, 1.836970198721029e-16, 3, -5, 3.0616169978683834e-16, -9, 7.000000000000001)

      # Scale + Rotate + Translate
      result = self.scale.clone()
      result.concat(self.rotate)
      result.concat(self.translate)
      self.assertMatrix(result, 1.836970198721029e-16, 3, -5, 3.0616169978683834e-16, 7, 9)

      # Translate + Scale + Rotate
      result = self.translate.clone()
      result.concat(self.scale)
      result.concat(self.rotate)
      self.assertMatrix(result, 1.836970198721029e-16, 3, -5, 3.0616169978683834e-16, -45, 21.000000000000004)

      # Translate + Rotate + Scale
      result = self.translate.clone()
      result.concat(self.rotate)
      result.concat(self.scale)
      self.assertMatrix(result, 1.836970198721029e-16, 5, -3, 3.0616169978683834e-16, -27, 35.00000000000001)

      # Rotate + Translate + Scale
      result = self.rotate.clone()
      result.concat(self.translate)
      result.concat(self.scale)
      self.assertMatrix(result, 1.836970198721029e-16, 5, -3, 3.0616169978683834e-16, 21, 45)

      # Rotate + Scale + Translate
      result = self.rotate.clone()
      result.concat(self.scale)
      result.concat(self.translate)
      self.assertMatrix(result, 1.836970198721029e-16, 5, -3, 3.0616169978683834e-16, 7, 9)

   def test_right_single(self):
      # Matrix + Scale
      result = self.matrix.clone()
      result.concat(self.scale)
      self.assertMatrix(result, 33, 65, 51, 95, 69, 145)

      # Matrix + Transform
      result = self.matrix.clone()
      result.concat(self.translate)
      self.assertMatrix(result, 11, 13, 17, 19, 30, 38)

      # Matrix + Rotate
      result = self.matrix.clone()
      result.concat(self.rotate)
      self.assertMatrix(result, -13, 11, -19, 17, -29, 23)

   def test_right_double(self):
      # Matrix + Scale + Translate
      result = self.matrix.clone()
      result.concat(self.scale)
      result.concat(self.translate)
      self.assertMatrix(result, 33, 65, 51, 95, 76, 154)

      # Matrix + Translate + Scale
      result = self.matrix.clone()
      result.concat(self.translate)
      result.concat(self.scale)
      self.assertMatrix(result, 33, 65, 51, 95, 90, 190)

      # Matrix + Scale + Rotate
      result = self.matrix.clone()
      result.concat(self.scale)
      result.concat(self.rotate)
      self.assertMatrix(result, -65, 33.00000000000001, -95, 51.00000000000001, -145, 69.00000000000001)

      # Matrix + Rotate + Scale
      result = self.matrix.clone()
      result.concat(self.rotate)
      result.concat(self.scale)
      self.assertMatrix(result, -39, 55, -57, 85, -87, 115)

      # Matrix + Translate + Rotate
      result = self.matrix.clone()
      result.concat(self.translate)
      result.concat(self.rotate)
      self.assertMatrix(result, -13, 11, -19, 17, -38, 30.000000000000004)

      # Matrix + Rotate + Translate
      result = self.matrix.clone()
      result.concat(self.rotate)
      result.concat(self.translate)
      self.assertMatrix(result, -13, 11, -19, 17, -22, 32)

   def test_right_triple(self):
      # Matrix + Scale + Translate + Rotate
      result = self.matrix.clone()
      result.concat(self.scale)
      result.concat(self.translate)
      result.concat(self.rotate)
      self.assertMatrix(result, -65, 33.00000000000001, -95, 51.00000000000001, -154, 76.00000000000001)

      # Matrix + Scale + Rotate + Translate
      result = self.matrix.clone()
      result.concat(self.scale)
      result.concat(self.rotate)
      result.concat(self.translate)
      self.assertMatrix(result, -65, 33.00000000000001, -95, 51.00000000000001, -138, 78.00000000000001)

      # Matrix + Translate + Scale + Rotate
      result = self.matrix.clone()
      result.concat(self.translate)
      result.concat(self.scale)
      result.concat(self.rotate)
      self.assertMatrix(result, -65, 33.00000000000001, -95, 51.00000000000001, -190, 90.00000000000001)

      # Matrix + Translate + Rotate + Scale
      result = self.matrix.clone()
      result.concat(self.translate)
      result.concat(self.rotate)
      result.concat(self.scale)
      self.assertMatrix(result, -39, 55, -57, 85, -114, 150.00000000000003)

      # Matrix + Rotate + Translate + Scale
      result = self.matrix.clone()
      result.concat(self.rotate)
      result.concat(self.translate)
      result.concat(self.scale)
      self.assertMatrix(result, -39, 55, -57, 85, -66, 160)

      # Matrix + Rotate + Scale + Translate
      result = self.matrix.clone()
      result.concat(self.rotate)
      result.concat(self.scale)
      result.concat(self.translate)
      self.assertMatrix(result, -39, 55, -57, 85, -80, 124)

   def test_left_single(self):
      # Scale + Matrix
      result = self.scale.clone()
      result.concat(self.matrix)
      self.assertMatrix(result, 33, 39, 85, 95, 23, 29)

      # Translate + Matrix
      result = self.translate.clone()
      result.concat(self.matrix)
      self.assertMatrix(result, 11, 13, 17, 19, 253, 291)

      # Rotate + Matrix
      result = self.rotate.clone()
      result.concat(self.matrix)
      self.assertMatrix(result, 17, 19, -10.999999999999998, -12.999999999999998, 23, 29)

   def test_left_double(self):
      # Scale + Translate + Matrix
      result = self.scale.clone()
      result.concat(self.translate)
      result.concat(self.matrix)
      self.assertMatrix(result, 33, 39, 85, 95, 253, 291)

      # Translate + Scale + Matrix
      result = self.translate.clone()
      result.concat(self.scale)
      result.concat(self.matrix)
      self.assertMatrix(result, 33, 39, 85, 95, 1019, 1157)

      # Scale + Rotate + Matrix
      result = self.scale.clone()
      result.concat(self.rotate)
      result.concat(self.matrix)
      self.assertMatrix(result, 51, 57, -54.99999999999999, -65, 23, 29)

      # Rotate + Scale + Matrix
      result = self.rotate.clone()
      result.concat(self.scale)
      result.concat(self.matrix)
      self.assertMatrix(result, 85, 95, -32.99999999999999, -38.99999999999999, 23, 29)

      # Translate + Rotate + Matrix
      result = self.translate.clone()
      result.concat(self.rotate)
      result.concat(self.matrix)
      self.assertMatrix(result, 17, 19, -10.999999999999998, -12.999999999999998, 43.000000000000014, 45.00000000000003)

      # Rotate + Translate + Matrix
      result = self.rotate.clone()
      result.concat(self.translate)
      result.concat(self.matrix)
      self.assertMatrix(result, 17, 19, -10.999999999999998, -12.999999999999998, 253, 291)

   def test_left_triple(self):
      # scale + translate + rotate + matrix
      result = self.scale.clone()
      result.concat(self.translate)
      result.concat(self.rotate)
      result.concat(self.matrix)
      self.assertMatrix(result, 51, 57, -54.99999999999999, -65, 43.000000000000014, 45.00000000000003)

      # scale + rotate + translate + matrix
      result = self.scale.clone()
      result.concat(self.rotate)
      result.concat(self.translate)
      result.concat(self.matrix)
      self.assertMatrix(result, 51, 57, -54.99999999999999, -65, 253, 291)

      # translate + scale + rotate + matrix
      result = self.translate.clone()
      result.concat(self.scale)
      result.concat(self.rotate)
      result.concat(self.matrix)
      self.assertMatrix(result, 51, 57, -54.99999999999999, -65, -114.99999999999994, -156.99999999999994)

      # translate + rotate + scale + matrix
      result = self.translate.clone()
      result.concat(self.rotate)
      result.concat(self.scale)
      result.concat(self.matrix)
      self.assertMatrix(result, 85, 95, -32.99999999999999, -38.99999999999999, 321.0000000000001, 343.0000000000001)

      # rotate + translate + scale + matrix
      result = self.rotate.clone()
      result.concat(self.translate)
      result.concat(self.scale)
      result.concat(self.matrix)
      self.assertMatrix(result, 85, 95, -32.99999999999999, -38.99999999999999, 1019, 1157)

      # rotate + scale + translate + matrix
      result = self.rotate.clone()
      result.concat(self.scale)
      result.concat(self.translate)
      result.concat(self.matrix)
      self.assertMatrix(result, 85, 95, -32.99999999999999, -38.99999999999999, 253, 291)

   def test_middle_double(self):
      # scale + matrix + translate
      result = self.scale.clone()
      result.concat(self.matrix)
      result.concat(self.translate)
      self.assertMatrix(result, 33, 39, 85, 95, 30, 38)

      # translate + matrix + scale
      result = self.translate.clone()
      result.concat(self.matrix)
      result.concat(self.scale)
      self.assertMatrix(result, 33, 65, 51, 95, 759, 1455)

      # scale + matrix + rotate
      result = self.scale.clone()
      result.concat(self.matrix)
      result.concat(self.rotate)
      self.assertMatrix(result, -39, 33, -95, 85, -29, 23)

      # rotate + matrix + scale
      result = self.rotate.clone()
      result.concat(self.matrix)
      result.concat(self.scale)
      self.assertMatrix(result, 51, 95, -32.99999999999999, -64.99999999999999, 69, 145)

      # translate + matrix + rotate
      result = self.translate.clone()
      result.concat(self.matrix)
      result.concat(self.rotate)
      self.assertMatrix(result, -13, 11, -19, 17, -291, 253.00000000000003)

      # rotate + matrix + translate
      result = self.rotate.clone()
      result.concat(self.matrix)
      result.concat(self.translate)
      self.assertMatrix(result, 17, 19, -10.999999999999998, -12.999999999999998, 30, 38)

   def test_middle_triple1(self):
      # scale + matrix + translate + rotate
      result = self.scale.clone()
      result.concat(self.matrix)
      result.concat(self.translate)
      result.concat(self.rotate)
      self.assertMatrix(result, -39, 33, -95, 85, -38, 30.000000000000004)

      # scale + matrix + rotate + translate
      result = self.scale.clone()
      result.concat(self.matrix)
      result.concat(self.rotate)
      result.concat(self.translate)
      self.assertMatrix(result, -39, 33, -95, 85, -22, 32)

      # translate + matrix + scale + rotate
      result = self.translate.clone()
      result.concat(self.matrix)
      result.concat(self.scale)
      result.concat(self.rotate)
      self.assertMatrix(result, -65, 33.00000000000001, -95, 51.00000000000001, -1455, 759.0000000000001)

      # translate + matrix + rotate + scale
      result = self.translate.clone()
      result.concat(self.matrix)
      result.concat(self.rotate)
      result.concat(self.scale)
      self.assertMatrix(result, -39, 55, -57, 85, -873, 1265.0000000000002)

      # rotate + matrix + translate + scale
      result = self.rotate.clone()
      result.concat(self.matrix)
      result.concat(self.translate)
      result.concat(self.scale)
      self.assertMatrix(result, 51, 95, -32.99999999999999, -64.99999999999999, 90, 190)

      # rotate + matrix + scale + translate
      result = self.rotate.clone()
      result.concat(self.matrix)
      result.concat(self.scale)
      result.concat(self.translate)
      self.assertMatrix(result, 51, 95, -32.99999999999999, -64.99999999999999, 76, 154)

   def test_middle_triple2(self):
      # scale + translate + matrix + rotate
      result = self.scale.clone()
      result.concat(self.translate)
      result.concat(self.matrix)
      result.concat(self.rotate)
      self.assertMatrix(result, -39, 33, -95, 85, -291, 253.00000000000003)

      # scale + rotate + matrix + translate
      result = self.scale.clone()
      result.concat(self.rotate)
      result.concat(self.matrix)
      result.concat(self.translate)
      self.assertMatrix(result, 51, 57, -54.99999999999999, -65, 30, 38)

      # translate + scale + matrix + rotate
      result = self.translate.clone()
      result.concat(self.scale)
      result.concat(self.matrix)
      result.concat(self.rotate)
      self.assertMatrix(result, -39, 33, -95, 85, -1157, 1019.0000000000001)

      # translate + rotate + matrix + scale
      result = self.translate.clone()
      result.concat(self.rotate)
      result.concat(self.matrix)
      result.concat(self.scale)
      self.assertMatrix(result, 51, 95, -32.99999999999999, -64.99999999999999, 129.00000000000006, 225.00000000000014)

      # rotate + translate + matrix + scale
      result = self.rotate.clone()
      result.concat(self.translate)
      result.concat(self.matrix)
      result.concat(self.scale)
      self.assertMatrix(result, 51, 95, -32.99999999999999, -64.99999999999999, 759, 1455)

      # rotate + scale + matrix + translate
      result = self.rotate.clone()
      result.concat(self.scale)
      result.concat(self.matrix)
      result.concat(self.translate)
      self.assertMatrix(result, 85, 95, -32.99999999999999, -38.99999999999999, 30, 38)


class Matrix3DTests(as3libTestCase):
   def test_constructor(self):
      m = Matrix3D()
      self.assertMatrix3D(m, (1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))

   def test_appendScale(self):
      m = Matrix3D()
      m.appendScale(1, 2, 3)
      self.assertMatrix3D(m, (1,0,0,0,0,2,0,0,0,0,3,0,0,0,0,1))

   def test_identity(self):
      m = Matrix3D(Vector.Number([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]))
      self.assertMatrix3D(m, (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
      m.identity()
      self.assertMatrix3D(m, (1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))

   def test_determinant(self):
      # Zero
      m = Matrix3D(Vector.Number([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
      self.assertEqual(m.determinant, 0)

      m = Matrix3D(Vector.Number([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]))
      self.assertEqual(m.determinant, 0)

      # Non-zero, randomly generated input
      m = Matrix3D(Vector.Number([37,48,70,38,17,33,70,52,94,89,11,4,2,43,90,50]))
      self.assertEqual(m.determinant, 1953360)

      m = Matrix3D(Vector.Number([30,76,67,56,69,61,99,11,95,92,84,24,14,35,96,71]))
      self.assertEqual(m.determinant, 8822702)

   def test_2(self):
      m = Matrix3D(Vector.Number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]))
      self.assertMatrix3D(m, (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))

      self.assertVector3D(m.position, 13, 14, 15)
      m.position = Vector3D(12, 13, 14)
      self.assertVector3D(m.position, 12, 13, 14)

      m.prependTranslation(-1, 0, 2)
      self.assertVector3D(m.position, 29, 31, 33)
      self.assertMatrix3D(m, (1,2,3,4,5,6,7,8,9,10,11,12,29,31,33,36))

      m.prepend(m)
      self.assertMatrix3D(m, (154,168,182,200,330,364,398,440,506,560,614,680,1525,1690,1855,2056))

      other = Matrix3D()
      other.copyFrom(m)
      self.assertMatrix3D(other, (154,168,182,200,330,364,398,440,506,560,614,680,1525,1690,1855,2056))

      out = Vector.Number()
      out.length = 20
      m.copyRawDataTo(out, 1, True)
      self.assertArray(out, (0,154,168,182,200,330,364,398,440,506,560,614,680,1525,1690,1855,2056,0,0,0))
      m.copyRawDataTo(out, 2, True)
      self.assertArray(out, (0,154,154,330,506,1525,168,364,560,1690,182,398,614,1855,200,440,680,2056,0,0))

      v = Vector3D(1, 2, 3, 4)
      vOut = m.transformVector(v)
      self.assertVector3D(vOut, 3857, 4266, 4675, 5176)

      vecs = Vector.Number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
      vecsOut = Vector.Number()
      m.transformVectors(vecs, vecsOut)
      self.assertArray(vecsOut, (3857,4266,4675,6827,7542,8257,9797,10818,11839))

      vecsOutFixed = Vector.Number(vecs.length, True)
      m.transformVectors(vecs, vecsOutFixed)
      self.assertArray(vecsOutFixed, (3857,4266,4675,6827,7542,8257,9797,10818,11839,0))

      vecsOutFixedTooSmall = Vector.Number(4, True)
      self.assertRaises(RangeError, m.transformVector, vecs, vecsOutFixedTooSmall)

      self.assertRaises(TypeError, m.transformVectors, as3lib.null, vecsOut)
      self.assertRaises(TypeError, m.transformVectors, vecs, as3lib.null)

      vOut = m.deltaTransformVector(v)
      self.assertVector3D(vOut, 2332, 2576, 2820, 3120)

      tooShort = Matrix3D(Vector.Number([1, 2]))
      self.assertMatrix3D(tooShort, (1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))

      tooLong = Matrix3D(Vector.Number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]))
      self.assertMatrix3D(tooLong, (1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))

      modified = Vector.Number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
      newMat = Matrix3D(modified)
      self.assertMatrix3D(newMat, (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
      modified[0] = 9999
      self.assertMatrix3D(newMat, (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))

      newMat = Matrix3D(Vector.Number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]))
      col = Vector3D()
      check = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16))
      for i in range(4):
         newMat.copyColumnTo(i, row)
         self.assertVector3D(col, *check[i])

      self.assertRaises(ArgumentError, newMat.copyColumnTo, 4, col)

      row = Vector3D()
      check = ((1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (3, 8, 12, 16))
      for i in range(4):
         newMat.copyRowTo(i, row)
         self.assertVector3D(col, *check[i])

      self.assertRaises(ArgumentError, newMat.copyRowTo, 4, row)

      row0 = Vector3D(100, 200, 300, 400)
      row1 = Vector3D(500, 600, 700, 800)
      row2 = Vector3D(900, 1000, 1100, 1200)
      row3 = Vector3D(1300, 1400, 1500, 1600)

      newMat.copyRowFrom(0, row0)
      newMat.copyRowFrom(1, row1)
      newMat.copyRowFrom(2, row2)
      newMat.copyRowFrom(3, row3)

      self.assertRaises(ArgumentError, newMat.copyRowFrom, 4, row3)

      self.assertMatrix3D(newMat, (100,500,900,1300,200,600,1000,1400,300,700,1100,1500,400,800,1200,1600))

      newMat.prependRotation(90, Vector3D.X_AXIS)
      self.assertMatrix3D(newMat, (100,500,900,1300,300,700,1100,1500,-199.99999999999997,-600,-999.9999999999999,-1400,400,800,1200,1600))

      newMat.prependScale(1, 2, 3)
      self.assertMatrix(newMat, (100,500,900,1300,600,1400,2200,3000,-599.9999999999999,-1800,-2999.9999999999995,-4200,400,800,1200,1600))

   def test_copyColumnFrom(self):
      mat = Matrix3D(Vector.Number([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
      col = Vector3D(3, 4, 5, 6)
      check = ((3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0),(3,4,5,6,3,4,5,6,0,0,0,0,0,0,0,0),(3,4,5,6,3,4,5,6,3,4,5,6,0,0,0,0),(3,4,5,6,3,4,5,6,3,4,5,6,3,4,5,6))
      for i in range(4):
         mat.copyColumnFrom(i, col)
         self.assertMatrix3D(mat, check[i])

      self.assertRaises(ArgumentError, mat.copyColumnFrom, 4, col)

   def test_compose(self):
      raise TestNotImplemented

   def test_invert(self):
      raise TestNotImplemented


class PerspectiveProjectionTests(as3libTestCase):...


class PointTests(as3libTestCase):
   def test_constructor(self):
      p = Point()
      self.assertPoint(p, 0, 0)

      p = Point(1)
      self.assertPoint(p, 1, 0)

      p = Point(1, 2)
      self.assertPoint(p, 1, 2)

      # TODO: Find a way to handle this
      p = Point(as3lib.Object(), 2)
      self.assertNaN(p.x)
      self.assertEqual(p.y, 2)

   def test_add(self):
      p = Point()
      self.assertPoint(p.add(Point(1, 2)), 1, 2)
      self.assertPoint(p, 0, 0)

   def test_subtract(self):
      p = Point()
      self.assertPoint(p.subtract(Point(1, 2)), -1, -2)
      self.assertPoint(p, 0, 0)

   def test_distance(self):
      d = Point.distance(Point(), Point())
      self.assertEqual(d, 0)

      d = Point.distance(Point(-100, 200), Point(100, 200))
      self.assertEqual(d, 200)

   def test_equals(self):
      p = Point()
      self.assertFalse(p.equals(Point(1, 2)))
      self.assertTrue(p.equals(p))
      self.assertPoint(p, 0, 0)

   def test_clone(self):
      p = Point(1, 2)
      clone = p.clone()
      self.assertPoint(p, 1, 2)
      self.assertPoint(clone, 1, 2)

      self.assertIsNot(p, clone)
      self.assertTrue(p.equals(clone))

   def test_interpolate(self):
      p1 = Point(-100, -200)
      p2 = Point(100, 200)

      self.assertPoint(Point.interpolate(p1, p2, -1), 300, 600)
      self.assertPoint(Point.interpolate(p1, p2, 0), 100, 200)
      self.assertPoint(Point.interpolate(p1, p2, 0.5), 0, 0)
      self.assertPoint(Point.interpolate(p1, p2, 1), -100, -200)
      self.assertPoint(Point.interpolate(p1, p2, 2), -300, -600)

   def test_length(self):
      self.assertEqual(Point().length, 0)
      self.assertEqual(Point(100, 0).length, 100)
      self.assertEqual(Point(0, -200).length, 200)

   def test_normalize(self):
      p = Point()
      p.normalize(10)
      self.assertPoint(p, 0, 0)

      p = Point()
      p.normalize(-5)
      self.assertPoint(p, 0, 0)

      p = Point(100, 200)
      p.normalize(10)
      self.assertPoint(p, 4.47213595499958, 8.94427190999916)

      p = Point(100, 200)
      p.normalize(-5)
      self.assertPoint(p, -2.23606797749979, -4.47213595499958)

      p = Point(-200, 100)
      p.normalize(10)
      self.assertPoint(p, -8.94427190999916, 4.47213595499958)

      p = Point(-200, 100)
      p.normalize(-5)
      self.assertPoint(p, 4.47213595499958, -2.23606797749979)

      p = Point(as3lib.undefined, 100)
      p.normalize(1)
      self.assertPoint(p, as3lib.NaN, 100)

      p = Point(100, as3lib.null)
      p.normalize(1)
      self.assertPoint(p, 1, 0)

   def test_offset(self):
      p = Point()
      self.assertPoint(p, 0, 0)

      p.offset(100, 200)
      self.assertPoint(p, 100, 200)

      p.offset(-1000, -2000)
      self.assertPoint(p, -900, -1800)

   def test_polar(self):
      self.assertPoint(Point.polar(5, Math.atan(3/4)), 4, 3)
      self.assertPoint(Point.polar(0, Math.atan(3/4)), 0, 0)

   def test_toString(self):
      p = Point()
      self.assertEqual(p.toString(), '(x=0, y=0)')


class RectangleTests(as3libTestCase):...


class TransformTests(as3libTestCase):
   class TestClass(MovieClip):
      def __init__(self, cls):
         self.c = cls
         self.testEQ()
         self.test2D()
         self.test3D()
         self.testCopy2D()
         self.testCopy3D()
         # self.testImageComparison()

      def testEQ(self):
         # These tests originally used ===
         # TODO: Test these on flash player
         s = Sprite()
         t = s.transform

         t.matrix = Matrix()
         self.c.assertIsNot(t.matrix, t.matrix)

         t.matrix3D = Matrix3D()
         self.c.assertIs(t.matrix3D, t.matrix3D)

         t.perspectiveProjection = PerspectiveProjection()
         self.c.assertIsNot(t.perspectiveProjection, t.perspectiveProjection)

         t.colorTransform = ColorTransform()
         self.c.assertIsNot(t.colorTransform, t.colorTransform)

      def test2D(self):
         sprite2D = Sprite()

         # sprite2D: new Sprite has null matrix3D and valid matrix
         self.c.assertMatrix(sprite2D.transform.matrix, 1, 0, 0, 1, 0, 0)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)

         # sprite2D: set identity matrix
         mat2D = Matrix()
         mat2D.identity()
         sprite2D.transform.matrix = mat2D
         self.c.assertMatrix(sprite2D.transform.matrix, 1, 0, 0, 1, 0, 0)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)
         self.c.assertMatrix(mat2D, 1, 0, 0, 1, 0, 0)

         #  sprite2D: update mat2D"
         mat2D.setTo(2,3,4,5,6,7)
         self.c.assertMatrix(sprite2D.transform.matrix, 1, 0, 0, 1, 0, 0)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)
         self.c.assertMatrix(mat2D, 2, 3, 4, 5, 6, 7)

         # sprite2D: .matrix = mat2D
         sprite2D.transform.matrix = mat2D;
         self.c.assertMatrix(sprite2D.transform.matrix, 2, 3, 4, 5, 6, 7)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)
         self.c.assertMatrix(mat2D, 2, 3, 4, 5, 6, 7)

         # sprite2D: .matrix = null
         sprite2D.transform.matrix = as3lib.null
         self.c.assertEqual(sprite2D.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite2D.transform.matrix3D, (2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1))
         self.c.assertMatrix(mat2D, 2, 3, 4, 5, 6, 7)

         # sprite2D: .matrix3D = null
         sprite2D.transform.matrix3D = as3lib.null
         self.c.assertMatrix(sprite2D.transform.matrix, 1, 0, 0, 1, 0, 0)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)
         self.c.assertMatrix(mat2D, 2, 3, 4, 5, 6, 7)

         # sprite2D: set x = 30, y = 50
         sprite2D.x = 30
         sprite2D.y = 50
         self.c.assertMatrix(sprite2D.transform.matrix, 1, 0, 0, 1, 30, 50)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)
         self.c.assertMatrix(mat2D, 2, 3, 4, 5, 6, 7)

      def test3D(self):
         sprite3D = Sprite()

         # sprite3D: set identity matrix3D
         mat3D = Matrix3D()
         mat3D.identity()
         sprite3D.transform.matrix3D = mat3D
         self.c.assertEqual(sprite2D.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite2D.transform.matrix3D, (1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))
         self.c.assertMatrix3D(mat3D, (1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))

         # sprite3D: update mat3D
         # RUFFLE: FIXME: values shouldn't be zero (0) for test coverage. Unsupported now.
         mat3D.copyFrom(Matrix3D(Vector.Number([2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1])))
         self.c.assertEqual(sprite2D.transform.matrix, as3lib.null)
         # RUFFLE: FIXME: mat3D update should be applied to transform.matrix3D immediately
         # trace("sprite3D.transform.matrix3D.rawData", sprite3D.transform.matrix3D.rawData);
         self.c.assertMatrix3D(mat3D, (2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1))

         # sprite3D: .matrix3D = mat3D
         sprite3D.transform.matrix3D = mat3D
         self.c.assertEqual(sprite2D.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite2D.transform.matrix3D, (2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1))
         self.c.assertMatrix3D(mat3D, (2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1))

         # sprite3D: .matrix = null
         self.c.assertEqual(sprite2D.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite2D.transform.matrix3D, (2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1))
         self.c.assertMatrix3D(mat3D, (2,3,0,0,4,5,0,0,0,0,1,0,6,7,0,1))

         # sprite3D: set x = 30, y = 50
         sprite3D.x = 30
         sprite3D.y = 50
         self.c.assertEqual(sprite2D.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite2D.transform.matrix3D, (2,3,0,0,4,5,0,0,0,0,1,0,30,50,0,1))
         # RUFFLE: FIXME: mat3D.rawData should be updated by sprite3D x/y update.
         # trace("mat3D.rawData", mat3D.rawData);

         # sprite3D: .matrix3D = null
         sprite3D.transform.matrix3D = null
         self.c.assertMatrix(sprite2D.transform.matrix, 1, 0, 0, 1, 0, 0)
         self.c.assertEqual(sprite2D.transform.matrix3D, as3lib.null)
         # RUFFLE: FIXME: mat3D.rawData should be updated by sprite3D x/y update.
         # trace("mat3D.rawData", mat3D.rawData)

      def testCopy2D(self):
         sprite1 = Sprite()
         sprite2 = Sprite()

         mat2D = Matrix(1, 2, 3, 4, 5, 6)
         sprite1.transform.matrix = mat2D
         sprite2.transform = sprite1.transform
         self.c.assertMatrix(sprite1.transform.matrix, 1, 2, 3, 4, 5, 6)
         self.c.assertEqual(sprite1.transform.matrix3D, as3lib.null)
         self.c.assertMatrix(sprite2.transform.matrix, 1, 2, 3, 4, 5, 6)
         self.c.assertEqual(sprite2.transform.matrix3D, as3lib.null)

      def testCopy3D(self):
         sprite1 = Sprite()
         sprite2 = Sprite()

         mat3D = Matrix3D()
         mat3D.appendRotation(1, Vector3D.Z_AXIS)
         # RUFFLE: FIXME: zScale shouldn't be one (1) for test coverage. Unsupported now.
         mat3D.appendScale(2, 3, 1)
         # RUFFLE: FIXME: z shouldn't be zero (0) for test coverage. Unsupported now.
         mat3D.appendTranslation(5, 6, 0)
         sprite1.transform.matrix3D = mat3D
         sprite2.transform = sprite1.transform
         self.c.assertEqual(sprite1.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite1.transform.matrix3D, (1.9996954202651978,0.05235721915960312,0,0,-0.03490481153130531,2.9995431900024414,0,0,0,0,1,0,5,6,0,1))
         self.c.assertEqual(sprite2.transform.matrix, as3lib.null)
         self.c.assertMatrix3D(sprite2.transform.matrix3D, (1.9996954202651978,0.05235721915960312,0,0,-0.03490481153130531,2.9995431900024414,0,0,0,0,1,0,5,6,0,1))

      '''
      def testImageComparison(self):
         m = Matrix3D()

         # id
         s1 = Sprite()
         s1.x = 10
         s1.y = 10
         bd1 = BitmapData(50, 50, as3lib.false, 0xFF0000)
         b1 = Bitmap(bd1)
         m.identity()
         b1.transform.matrix3D = m.clone()
         s1.addChild(b1)
         self.addChild(s1)  # This comes from DisplayObjectContainer

         # scale
         s2 = Sprite()
         s2.x = 160
         s2.y = 10
         bd2 = BitmapData(50, 50, false, 0x00FF00)
         b2 = Bitmap(bd2)
         m.identity()
         m.appendScale(1.5, 3, 1)
         b2.transform.matrix3D = m.clone()
         s2.addChild(b2)
         self.addChild(s2)

         # rotation
         s3 = Sprite()
         s3.x = 310
         s3.y = 10
         bd3 = BitmapData(50, 50, false, 0x00FFFF)
         b3 = Bitmap(bd3)
         m.identity()
         m.appendRotation(30, Vector3D.Z_AXIS)
         b3.transform.matrix3D = m.clone()
         s3.addChild(b3)
         self.addChild(s3)

         # translation
         s4 = Sprite()
         s4.x = 10
         s4.y = 160
         bd4 = BitmapData(50, 50, false, 0x0000FF)
         b4 = Bitmap(bd4)
         m.identity()
         m.appendTranslation(50, 50, 0)
         b4.transform.matrix3D = m.clone()
         s4.addChild(b4)
         self.addChild(s4)

         # scale + rotation + translation
         s5 = Sprite()
         s5.x = 160
         s5.y = 160
         bd5 = BitmapData(50, 50, false, 0xFF00FF)
         b5 = Bitmap(bd5)
         m.identity()
         m.appendScale(2, 3, 1)
         m.appendRotation(30, Vector3D.Z_AXIS)
         m.appendTranslation(50, 50, 0)
         b5.transform.matrix3D = m.clone()
         s5.addChild(b5)
         self.addChild(s5)
      '''

   def test_1(self):
      TransformTests.TestClass(self)


class Utils3DTests(as3libTestCase):
   def test_1(self):
      vec = Vector3D(1.0, 2.0, 3.0, 4.0)
      mat = Matrix3D(Vector.Number([
         100, 200, 300, 400,
         500, 600, 700, 800,
         900, 1000, 1100, 1200,
         1300, 1400, 1500, 1600
      ]))

      projected = Utils3D.projectVector(mat, vec)
      self.assertVector3D(projected, 0.7083333333333334, 0.8055555555555556,
                          0.9027777777777778, 7200)

      verts = Vector.Number([100, 200, 300, 400, 500, 600])
      projectedVerts = Vector.Number([])
      uvts = Vector.Number([])

      # Bad project
      Utils3D.projectVectors(mat, verts, projectedVerts, uvts)
      self.assertArray(projectedVerts, (0.6789529914529915, 0.7859686609686609, 0.6486423220973783, 0.7657615480649188), 4)
      self.assertArray(uvts, (0, 0, 0.0000017806267806267806, 0, 0, 7.802746566791511e-7), 6)

      # Good project
      # Deliberately missing a final z coord
      uvts = uvts = Vector.Number([1000, 2000, 3000, 4000, 5000, 6000, 5, 6])

      Utils3D.projectVectors(mat, verts, projectedVerts, uvts)
      self.assertArray(projectedVerts, (0.6789529914529915, 0.7859686609686609, 0.6486423220973783, 0.7657615480649188), 4)
      self.assertArray(uvts, (1000, 2000, 0.0000017806267806267806, 4000, 5000, 7.802746566791511e-7, 5, 6), 8)


class Vector3DTests(as3libTestCase):
   mp = Math.pow(10, 12)

   def roundNumber(self, x):  # Originally called r
      return Math.round(x * self.mp) / self.mp

   def roundVector(self, v):  # Originally called rv
      return Vector3D(self.roundNumber(v.x), self.roundNumber(v.y), self.roundNumber(v.z), self.roundNumber(v.w))

   def test_constructor(self):
      v = Vector3D()
      self.assertVector3D(v, 0, 0, 0, 0)

      v = Vector3D(1)
      self.assertVector3D(v, 1, 0, 0, 0)

      v = Vector3D(1, 2)
      self.assertVector3D(v, 1, 2, 0, 0)

      v = Vector3D(1, 2, 3)
      self.assertVector3D(v, 1, 2, 3, 0)

      v = Vector3D(1, 2, 3, 4)
      self.assertVector3D(v, 1, 2, 3, 4)

      v = Vector3D(as3lib.Object(), 2)
      self.assertNaN(v.x)
      self.assertEqual(v.y, 2)
      self.assertEqual(v.z, 0)
      self.assertEqual(v.w, 0)

   def test_toString(self):
      v = Vector3D()
      self.assertEqual(v.toString(), '(x=0, y=0, z=0)')

      v = Vector3D(1)
      self.assertEqual(v.toString(), '(x=1, y=0, z=0)')

      v = Vector3D(1, 2)
      self.assertEqual(v.toString(), '(x=1, y=2, z=0)')

      v = Vector3D(1, 2, 3)
      self.assertEqual(v.toString(), '(x=1, y=2, z=3)')

      v = Vector3D(1, 2, 3, 4)
      self.assertEqual(v.toString(), '(x=1, y=2, z=3)')

   def test_constants(self):
      self.assertVector3D(Vector3D.X_AXIS, 1, 0, 0, 0)
      self.assertVector3D(Vector3D.Y_AXIS, 0, 1, 0, 0)
      self.assertVector3D(Vector3D.Z_AXIS, 0, 0, 1, 0)

   def test_copyFrom(self):
      v = Vector3D(1, 2, 3, 4)
      v.copyFrom(Vector3D())
      self.assertVector3D(v, 0, 0, 0, 4)

      v = Vector3D()
      v.copyFrom(Vector3D(4, 5, 6, 7))
      self.assertVector3D(v, 4, 5, 6, 0)

      v = Vector3D(1, 2, 3, 4)
      v.copyFrom(Vector3D(4, 5, 6, 7))
      self.assertVector3D(v, 4, 5, 6, 4)

   def test_setTo(self):
      v = Vector3D()
      v.setTo(6, 7, 8)
      self.assertVector3D(v, 6, 7, 8, 0)

      v = Vector3D(1, 2, 3, 4)
      v.setTo(6, 7, 8)
      self.assertVector3D(v, 6, 7, 8, 4)

   def test_add(self):
      v1 = Vector3D()
      v2 = v1.add(Vector3D(1, 2, 3, 4))
      self.assertVector3D(v2, 1, 2, 3, 0)
      self.assertVector3D(v1, 0, 0, 0, 0)

      v1 = Vector3D(5, 6, 8, 9)
      v2 = v1.add(Vector3D())
      self.assertVector3D(v2, 5, 6, 8, 0)

      v1 = Vector3D(6, -7, 8, -9)
      v2 = v1.add(Vector3D(-10, 20, -30, 40))
      self.assertVector3D(v2, -4, 13, -22, 0)

   def test_subtract(self):
      v1 = Vector3D()
      v2 = v1.subtract(Vector3D(1, 2, 3, 4))
      self.assertVector3D(v2, -1, -2, -3, 0)
      self.assertVector3D(v1, 0, 0, 0, 0)

      v1 = Vector3D(5, 6, 8, 9)
      v2 = v1.subtract(Vector3D())
      self.assertVector3D(v2, 5, 6, 8, 0)

      v1 = Vector3D(6, -7, 8, -9)
      v2 = v1.subtract(Vector3D(-10, 20, -30, 40))
      self.assertVector3D(v2, 16, -27, 38, 0)

   def test_incrementBy(self):
      v = Vector3D()
      v.incrementBy(Vector3D())
      self.assertVector3D(v, 0, 0, 0, 0)

      v = Vector3D()
      v.incrementBy(Vector3D(1, 2, -3, 4))
      self.assertVector3D(v, 1, 2, -3, 0)

      v = Vector3D(3, -4, 5, 6)
      v.incrementBy(Vector3D(1, 2, -3, 4))
      self.assertVector3D(v, 4, -2, 2, 6)

   def test_decrementBy(self):
      v = Vector3D()
      v.decrementBy(Vector3D())
      self.assertVector3D(v, 0, 0, 0, 0)

      v = Vector3D()
      v.decrementBy(Vector3D(1, 2, -3, 4))
      self.assertVector3D(v, -1, -2, 3, 0)

      v = Vector3D(3, -4, 5, 6)
      v.decrementBy(Vector3D(1, 2, -3, 4))
      self.assertVector3D(v, 2, -6, 8, 6)

   def test_scaleBy(self):
      v = Vector3D(2, -4, 0, 5)
      v.scaleBy(10)
      self.assertVector3D(v, 20, -40, 0, 5)

      v = Vector3D(2, -4, 0, 5)
      v.scaleBy(-0.5)
      self.assertVector3D(v, -1, 2, 0, 5)

      v = Vector3D(2, -4, 0, 5)
      v.scaleBy(0)
      self.assertVector3D(v, 0, 0, 0, 5)

      v = Vector3D(2, -4, 0, 5)
      v.scaleBy(1)
      self.assertVector3D(v, 2, -4, 0, 5)

      v = Vector3D()
      v.scaleBy(100)
      self.assertVector3D(v, 0, 0, 0, 0)

   def test_negate(self):
      v = Vector3D(2, -4, 0)
      v.negate()
      self.assertVector3D(v, -2, 4, 0, 0)

      v = Vector3D(2, -4, 0, 5)
      v.negate()
      self.assertVector3D(v, -2, 4, 0, 5)

      v = Vector3D()
      v.negate()
      self.assertVector3D(v, 0, 0, 0, 0)

   def test_distance(self):
      d = Vector3D.distance(Vector3D(), Vector3D())
      self.assertEqual(d, 0)

      d = Vector3D.distance(Vector3D(-100, 200, 300, -400), Vector3D(100, 200, 300, -400))
      self.assertEqual(d, 200)

      d = Vector3D.distance(Vector3D(-100, 200, 300, -400), Vector3D(-102, 210, 311, -420))
      self.assertEqual(d, 15)

   def test_equals(self):
      v = Vector3D()
      self.assertFalse(v.equals(Vector3D(1, 2, 3, 4)))

      self.assertTrue(v.equals(v))

      self.assertTrue(Vector3D(1, 2, 3).equals(Vector3D(1, 2, 3, 4)))

   def test_nearEquals(self):
      # allFour=False
      n = Vector3D(100, 200, 300).nearEquals(Vector3D(100, 200, 300), 0, False)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300).nearEquals(Vector3D(100, 200, 300), 1, False)
      self.assertTrue(n)
      n = Vector3D(100, 200, 300).nearEquals(Vector3D(100, 200, 300), 10, False)
      self.assertTrue(n)

      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 400), 0, False)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 400), 1, False)
      self.assertTrue(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 400), 10, False)
      self.assertTrue(n)

      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 350, 400), 10, False)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 350, 400), 100, False)
      self.assertTrue(n)

      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 450), 10, False)
      self.assertTrue(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 450), 100, False)
      self.assertTrue(n)

      # allFour=True
      n = Vector3D(100, 200, 300).nearEquals(Vector3D(100, 200, 300), 0, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300).nearEquals(Vector3D(100, 200, 300), 1, True)
      self.assertTrue(n)
      n = Vector3D(100, 200, 300).nearEquals(Vector3D(100, 200, 300), 10, True)
      self.assertTrue(n)

      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 400), 0, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 400), 1, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 400), 10, True)
      self.assertFalse(n)

      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 350, 400), 10, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 350, 400), 100, True)
      self.assertFalse(n)

      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 450), 10, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 400).nearEquals(Vector3D(100, 200, 300, 450), 100, True)
      self.assertFalse(n)

      # Buggy with allFour=True
      n = Vector3D(100, 200, 300, 10).nearEquals(Vector3D(100, 200, 300, 20), 100, True)
      self.assertTrue(n)
      n = Vector3D(100, 200, 300, 210).nearEquals(Vector3D(100, 200, 300, 220), 100, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 0).nearEquals(Vector3D(100, 200, 300, 200), 100, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, 200).nearEquals(Vector3D(100, 200, 300, 0), 100, True)
      self.assertTrue(n)
      n = Vector3D(100, 200, 300, 0).nearEquals(Vector3D(100, 200, 300, -200), 100, True)
      self.assertFalse(n)
      n = Vector3D(100, 200, 300, -200).nearEquals(Vector3D(100, 200, 300, 0), 100, True)
      self.assertTrue(n)

   def test_clone(self):
      v = Vector3D(1, 2, 3, 4)
      clone = v.clone()

      self.assertVector3D(v, 1, 2, 3, 4)
      self.assertVector3D(clone, 1, 2, 3, 4)
      self.assertIsNot(v, clone)
      self.assertTrue(v.equals(clone))

   def test_length(self):
      self.assertEqual(Vector3D().length, 0)
      self.assertEqual(Vector3D(100, 0).length, 100)
      self.assertEqual(Vector3D(2, -10, 11, -20).length, 15)

   def test_lengthSquared(self):
      self.assertEqual(Vector3D().lengthSquared, 0)
      self.assertEqual(Vector3D(100, 0).lengthSquared, 10000)
      self.assertEqual(Vector3D(100, -200, 300, -400).lengthSquared, 140000)

   def test_normalize(self):
      v = Vector3D()
      n = v.normalize()
      self.assertEqual(n, 0)
      self.assertVector3D(v, 0, 0, 0, 0)

      v = Vector3D(30, 40)
      n = v.normalize()
      self.assertEqual(n, 50)
      self.assertVector3D(v, 0.6, 0.8, 0, 0)

      v = Vector3D(-9, 12, 20)
      n = v.normalize()
      self.assertEqual(n, 25)
      self.assertVector3D(v, -0.36, 0.48, 0.8, 0)

      v = Vector3D(-9, 12, 20, -100)
      n = v.normalize()
      self.assertEqual(n, 25)
      self.assertVector3D(v, -0.36, 0.48, 0.8, -100)

      v = Vector3D(as3lib.undefined, 100, 100, 100)
      n = v.normalize()
      self.assertNaN(n)
      self.assertVector3DNaN(v, 100)

      v = Vector3D(7, as3lib.null, 24, 365)
      n = v.normalize()
      self.assertEqual(n, 25)
      self.assertVector3D(v, 0.28, 0, 0.96, 365)

   def test_project(self):
      v = Vector3D()
      v.project()
      self.assertVector3DNaN(v, 0)

      v = Vector3D(1, 2, 3)
      v.project()
      self.assertVector3D(v, as3lib.Infinity, as3lib.Infinity, as3lib.Infinity, 0)

      v = Vector3D(1, 2, 3, 1)
      v.project()
      self.assertVector3D(v, 1, 2, 3, 1)

      v = Vector3D(0, 0, 0, 1)
      v.project()
      self.assertVector3D(v, 0, 0, 0, 1)

      v = Vector3D(20, 30, 40, 10)
      v.project()
      self.assertVector3D(v, 2, 3, 4, 10)

      v = Vector3D(5, -6, 7, 0.1)
      v.project()
      self.assertVector3D(v, 50, -60, 70, 0.1)

      v = Vector3D(5, -6, 7, -0.2)
      v.project()
      self.assertVector3D(v, -25, 30, -35, -0.2)

   def test_angleBetween(self):
      a = Vector3D.angleBetween(Vector3D(), Vector3D())
      self.assertNaN(self.roundNumber(a))

      a = Vector3D.angleBetween(Vector3D(), Vector3D(1, 0, 0))
      self.assertNaN(self.roundNumber(a))

      a = Vector3D.angleBetween(Vector3D(1, 0, 0), Vector3D())
      self.assertNaN(self.roundNumber(a))

      a = Vector3D.angleBetween(Vector3D(1, 0, 0), Vector3D(0, 1, 0))
      self.assertEqual(self.roundNumber(a), 1.570796326795)

      a = Vector3D.angleBetween(Vector3D(0, -1, 0), Vector3D(0, 0, 1))
      self.assertEqual(self.roundNumber(a), 1.570796326795)

      a = Vector3D.angleBetween(Vector3D(0, -20, 0), Vector3D(0, 0, 0.1))
      self.assertEqual(self.roundNumber(a), 1.570796326795)

      a = Vector3D.angleBetween(Vector3D(2, 4, 6), Vector3D(0.6, 0.5, 0.1))
      self.assertEqual(self.roundNumber(a), 0.869901249923)

      a = Vector3D.angleBetween(Vector3D(0.6, 0.5, 0.1), Vector3D(2, 4, 6))
      self.assertEqual(self.roundNumber(a), 0.869901249923)

      a = Vector3D.angleBetween(Vector3D(2, 4, 6, 8), Vector3D(0.6, 0.5, 0.1, -0.2))
      self.assertEqual(self.roundNumber(a), 0.869901249923)

   def test_dotProduct(self):
      dp = Vector3D().dotProduct(Vector3D())
      self.assertEqual(self.roundNumber(dp), 0)

      dp = Vector3D().dotProduct(Vector3D(1, 0, 0))
      self.assertEqual(self.roundNumber(dp), 0)

      dp = Vector3D(1, 0, 0).dotProduct(Vector3D())
      self.assertEqual(self.roundNumber(dp), 0)

      dp = Vector3D(1, 0, 0).dotProduct(Vector3D(0, 1, 0))
      self.assertEqual(self.roundNumber(dp), 0)

      dp = Vector3D(0, -1, 0).dotProduct(Vector3D(0, 0, 1))
      self.assertEqual(self.roundNumber(dp), 0)

      dp = Vector3D(0, -20, 0).dotProduct(Vector3D(0, 0, 0.1))
      self.assertEqual(self.roundNumber(dp), 0)

      dp = Vector3D(2, 4, 6).dotProduct(Vector3D(0.6, 0.5, 0.1))
      self.assertEqual(self.roundNumber(dp), 3.8)

      dp = Vector3D(0.6, 0.5, 0.1).dotProduct(Vector3D(2, 4, 6))
      self.assertEqual(self.roundNumber(dp), 3.8)

      dp = Vector3D(2, 4, 6, 8).dotProduct(Vector3D(0.6, 0.5, 0.1, -0.2))
      self.assertEqual(self.roundNumber(dp), 3.8)

   def test_crossProduct(self):
      cp = Vector3D().crossProduct(Vector3D())
      self.assertVector3D(cp, 0, 0, 0, 1)

      cp = Vector3D().crossProduct(Vector3D(1, 0, 0))
      self.assertVector3D(cp, 0, 0, 0, 1)

      cp = Vector3D(1, 0, 0).crossProduct(Vector3D())
      self.assertVector3D(cp, 0, 0, 0, 1)

      cp = Vector3D(1, 0, 0).crossProduct(Vector3D(0, 1, 0))
      self.assertVector3D(cp, 0, 0, 1, 1)

      cp = Vector3D(0, -1, 0).crossProduct(Vector3D(0, 0, 1))
      self.assertVector3D(cp, -1, 0, 0, 1)

      cp = Vector3D(0, -20, 0).crossProduct(Vector3D(0, 0, 0.1))
      self.assertVector3D(cp, -2, 0, 0, 1)

      cp = Vector3D(2, 4, 6).crossProduct(Vector3D(0.6, 0.5, 0.1))
      self.assertVector3D(cp, -2.6, 3.4, -1.4, 1)

      cp = Vector3D(0.6, 0.5, 0.1).crossProduct(Vector3D(2, 4, 6))
      self.assertVector3D(cp, 2.6, -3.4, 1.4, 1)

      cp = Vector3D(2, 4, 6, 8).crossProduct(Vector3D(0.6, 0.5, 0.1, -0.2))
      self.assertVector3D(cp, -2.6, 3.4, -1.4, 1)
