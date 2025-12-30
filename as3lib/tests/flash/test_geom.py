from as3lib import Math
from as3lib.flash.geom import Matrix, Point, Vector3D
from as3lib.tests import as3libTestCase, TestNotImplemented


class GeomTestsBase(as3libTestCase):
   def assertMatrix(self, matrix, a, b, c, d, tx, ty):
      self.assertEqual(matrix.a, a)
      self.assertEqual(matrix.b, b)
      self.assertEqual(matrix.c, c)
      self.assertEqual(matrix.d, d)
      self.assertEqual(matrix.tx, tx)
      self.assertEqual(matrix.ty, ty)

   def assertPoint(self, point, x, y):
      self.assertEqual(point.x, x)
      self.assertEqual(point.y, y)

   def assertVector3D(self, vector, x, y, z, w=None):
      self.assertEqual(vector.x, x)
      self.assertEqual(vector.y, y)
      self.assertEqual(vector.z, z)
      if w is not None:
         self.assertEqual(vector.w, w)


class MatrixTests(GeomTestsBase):
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

   def test_createbox(self):
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

   def test_creategradientbox(self):
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

   def test_transformpoint(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      point = matrix.transformPoint(Point(1, 1))
      self.assertPoint(point, 18, 23)

   def test_deltatransformpoint(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      point = matrix.deltaTransformPoint(Point(1, 1))
      self.assertPoint(point, 7, 10)

   def test_copyfrom(self):
      matrix = Matrix(2, 3, 5, 7, 11, 13)
      matrix2 = Matrix()
      self.assertMatrix(matrix2, 1, 0, 0, 1, 0, 0)
      matrix2.copyFrom(matrix)
      self.assertMatrix(matrix2, 2, 3, 5, 7, 11, 13)

   def test_setTo(self):
      matrix = Matrix()
      matrix.setTo(2, 3, 5, 7, 11, 13)
      self.assertMatrix(matrix, 2, 3, 5, 7, 11, 13)

   def test_copyrowto(self):
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

   def test_copycolumnto(self):
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

   def test_copyrowfrom(self):
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


   def test_copycolumnfrom(self):
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


class MatrixConcatTests(GeomTestsBase):
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

   def test_rightsingle(self):
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

   def test_rightdouble(self):
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

   def test_righttriple(self):
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

   def test_leftsingle(self):
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

   def test_leftdouble(self):
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

   def test_lefttriple(self):
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

   def test_middledouble(self):
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

   def test_middletriple1(self):
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

   def test_middletriple2(self):
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
