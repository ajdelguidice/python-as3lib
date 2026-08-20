#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>

double itkwcalc(double neww, double newh, int startw, int starth) {
   double xmult = neww/startw;
   double ymult = newh/starth;
   if (xmult > ymult)
      return ymult;
   return xmult;
};

static PyObject * itk_windowcalculate(PyObject *self, PyObject *args) {
   double nw, nh;
   int sw, sh;
   if (!PyArg_ParseTuple(args, "ddii", &nw, &nh, &sw, &sh))
      return NULL;
   return PyFloat_FromDouble(itkwcalc(nw,nh,sw,sh));
};

static PyMethodDef cmathMethods[] = {
   {"calculate", itk_windowcalculate, METH_VARARGS, "window.calculate function in the interface_tk module."}
};

static struct PyModuleDef cmath = {
   PyModuleDef_HEAD_INIT,
   "cmath",
   NULL,
   -1,
   cmathMethods
};

PyMODINIT_FUNC PyInit_cmath(void) {
   return PyModule_Create(&cmath);
}
