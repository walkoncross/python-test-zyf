#include <Python.h>

static PyObject *SpamError;

static PyObject*
spam_system(PyObject *self, PyObject * args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;

    sts = system(command);
    // return Py_BuildValuse("i", sts);
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);    
}

static PyMethodDef SpamMethods[] = {
    //...
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    //...
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initspam(void)
{
    PyObject *m;
    m = Py_InitModule("spam", SpamMethods);
    if (m==NULL)
        return;
}