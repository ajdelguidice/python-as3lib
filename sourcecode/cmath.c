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

static PyObject * itk_windowresizefont(PyObject *self, PyObject *args) {
   int font;
   float mult;
   if (!PyArg_ParseTuple(args, "if", &font, &mult))
      return NULL;
   return PyLong_FromLong((long)round(font*mult*0.01));
};

static PyMethodDef cmathMethods[] = {
   {"calculate", itk_windowcalculate, METH_VARARGS, "window.calculate function in the interface_tk module."},
   {"resizefont", itk_windowresizefont, METH_VARARGS, "window.resizefont function in the interface_tk module."}
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
