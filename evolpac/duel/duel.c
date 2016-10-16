#include <Python.h>
#include <numpy/arrayobject.h>
#include "PacWar.h"

static char module_docstring[] =
    "This module provides an interface for battling between two genes.";
static char battle_docstring[] =
    "Battle two genes and return the statistics of result.";

static PyObject *battle_PyPacwar(PyObject *self, PyObject *args);

static PyMethodDef duel_methods[] = {
    {"battle", battle_PyPacwar, METH_VARARGS, battle_docstring},
    {NULL, NULL, 0, NULL}
};

static int
duel_exec(PyObject *m)
{
    import_array();
    return 0;
}

static struct PyModuleDef_Slot duel_slots[] = {
    {Py_mod_exec, duel_exec},
    {0, NULL},
};

static struct PyModuleDef duel_module = {
    PyModuleDef_HEAD_INIT,
    "evolpac.duel.duel",
    module_docstring,
    0,
    duel_methods,
    duel_slots,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC
PyInit_duel(void)
{
    return PyModuleDef_Init(&duel_module);
}


static PyObject *battle_PyPacwar(PyObject *self, PyObject *args)
{
    PyObject *g1_obj, *g2_obj;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "OO", &g1_obj, &g2_obj))
        return NULL;

    /* Interpret the input objects as numpy arrays. */
    PyObject *g1_array = PyArray_FROM_OTF(g1_obj, NPY_INT, NPY_IN_ARRAY);
    PyObject *g2_array = PyArray_FROM_OTF(g2_obj, NPY_INT, NPY_IN_ARRAY);

    /* If that didn't work, throw an exception. */
    if (g1_array == NULL || g2_array == NULL) {
        Py_XDECREF(g1_array);
        Py_XDECREF(g2_array);
        return NULL;
    }

    /* How many data points are there? */
    //int N = 50;

    /* Get pointers to the data as C-types. */
    int *g1 = (int*)PyArray_DATA(g1_array);
    int *g2 = (int*)PyArray_DATA(g2_array);

    /* Do battle. */
    int numrounds = 500;
  	int count[2]; 
  	char g1_str[51], g2_str[51];
  	PacGene g[2]; 
  	PacGenePtr gp[2] = {&g[0], &g[1]};
  	int i;
  	for (i = 0; i < 50; i++) {
  		g1_str[i] = g1[i] + '0';
  		g2_str[i] = g2[i] + '0';
  	}
    g1_str[i] = 0; g2_str[i] = 0;
    SetGeneFromString(g1_str, gp[0]);
    SetGeneFromString(g2_str, gp[1]);
    FastDuel(gp[0],gp[1],&numrounds,&count[0],&count[1]);

    /* Clean up. */
    Py_DECREF(g1_array);
    Py_DECREF(g2_array);

    /* Build the output tuple */
    PyObject *ret = Py_BuildValue("iii", numrounds,count[0],count[1]);
    return ret;
}

