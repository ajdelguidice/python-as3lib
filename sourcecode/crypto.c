#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h> 
#include <stdlib.h>

char* GenRandBytes(int nb, char* chars) {
    FILE* fptr = fopen("/dev/urandom", "rb");
    int i, j;
    for (i = 0, j = 0; i <= nb; i++) {
        chars[j] = fgetc(fptr);
        j++;
    };
    fclose(fptr);
    return chars;
};

static PyObject * generateRandomBytes(PyObject *self, PyObject *args) {
    int numBytes;
    if (!PyArg_ParseTuple(args, "i", &numBytes))
        return NULL;
    char chars[numBytes];
    return PyBytes_FromString(GenRandBytes(numBytes, chars));
};

static PyMethodDef CryptoMethods[] = {
    {"generateRandomBytes", generateRandomBytes, METH_VARARGS, "Gets random bytes."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Crypto = {
    PyModuleDef_HEAD_INIT,
    "crypto",
    "Python C module for as3lib's flash.crypto library",
    -1,
    CryptoMethods
};
PyMODINIT_FUNC PyInit_crypto(void) {
    PyObject *module;
    module = PyModule_Create(&Crypto);
    if (module == NULL)
        return NULL;
    return module;
}