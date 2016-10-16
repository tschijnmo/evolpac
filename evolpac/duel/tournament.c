#include<Python.h>
#include<numpy/arrayobject.h>
#include<stdio.h>

#include"PacWar.h"


typedef signed char PacBits;
static const int PACBIT_TYPE = NPY_BYTE;
typedef unsigned int Score;
static const int SCORE_TYPE = NPY_UINT;


/*
 * Pacwar core
 * ===========
 */


/**
 * Run a single duel between two Pac-mites.
 */

static void run_duel(PacBits *pac1, PacBits *pac2, Score *scores)
{
    /* Do battle. */
    int n_rounds = 500;
    int count[2]; 
    FastDuel(
        (PacGenePtr) pac1, (PacGenePtr) pac2, &n_rounds, 
        count, count + 1
    );

    /** Compute the score. */
    int first_win = (count[0] >= count[1]);
    int win_count = first_win ? count[0] : count[1];
    int los_count = first_win ? count[1] : count[0];
    Score *win_score = first_win ? scores : scores + 1;
    Score *los_score = first_win ? scores + 1 : scores;
    double ratio;

    if (los_count == 0) {
        if (n_rounds < 100) {
            *win_score = 20;
            *los_score = 0;
        } else if (n_rounds < 200) {
            *win_score = 19;
            *los_score = 1;
        } else if (n_rounds < 300) {
            *win_score = 18;
            *los_score = 2;
        } else {
            *win_score = 17;
            *los_score = 3;
        }
    } else {
        ratio = ((double) win_count) / los_count;
        if (ratio >= 10) {
            *win_score = 13;
            *los_score = 7;
        } else if (ratio >= 3) {
            *win_score = 12;
            *los_score = 8;
        } else if (ratio >= 1.5) {
            *win_score = 11;
            *los_score = 9;
        } else {
            *win_score = 10;
            *los_score = 10;
        }
    }

    return;
}


/**
 * Run the tournament.
 *
 * The result array is assumed to be zeroed already.
 */

static void 
run_tour_core(int n_pacs, PacBits *pacs_array, Score *res_array)
{
    int i, j;
    Score scores[2];

    #pragma omp parallel for private(scores) schedule(static)
    for (i = 0; i < n_pacs; i++) {
        for (j = i % 2; j < i; j += 2) {
            run_duel(pacs_array + i * n_pacs, pacs_array + j * n_pacs, scores);
            #pragma omp atomic
            res_array[i] += scores[0];
            #pragma omp atomic
            res_array[j] += scores[1];
        }
        for (j = i + 1; j < n_pacs; j += 2) {
            run_duel(pacs_array + i * n_pacs, pacs_array + j * n_pacs, scores);
            #pragma omp atomic
            res_array[i] += scores[0];
            #pragma omp atomic
            res_array[j] += scores[1];
        }
    }

    return;
}


/*
 * Python wrapper
 * ==============
 *
 *
 * Python functions
 * ----------------
 */


/**
 * Ensure a Python object is a group of Pac-mites.
 */

static PyArrayObject *get_pacs(PyObject *obj, int *n_pacs, PacBits **array)
{
    npy_intp *shape;
    PyArrayObject *pacs;

    /* Create/Get the array object */
    pacs = (PyArrayObject *) PyArray_FROM_OTF(
        obj, PACBIT_TYPE, NPY_ARRAY_IN_ARRAY | NPY_ARRAY_ENSUREARRAY
    );
    if (pacs == NULL) return NULL;

    if (PyArray_NDIM(pacs) != 2) {
        PyErr_SetString(PyExc_ValueError, "Pacs needs to have two dimensions");
        goto error;
    }

    shape = PyArray_SHAPE(pacs);
    if (shape[1] != 50) {
        PyErr_SetString(PyExc_ValueError, "Each Pac should have 50 bits");
        goto error;
    }

    *n_pacs = shape[0];
    *array = PyArray_DATA(pacs);
    return pacs;

error: 
    Py_DECREF(pacs);
    return NULL;
}


/**
 * Run tournament among a group of Pac-mites.
 */

static PyObject *run_tour(PyObject *self, PyObject *args)
{
    PyObject *pacs_arg;
    PyArrayObject *pacs;
    PyArrayObject *res;
    npy_intp res_dims[1];

    int n_pacs;
    PacBits *pacs_array;
    Score *res_array;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "O", &pacs_arg))
        return NULL;

    /* Interpret the input objects as numpy arrays. */
    pacs = get_pacs(pacs_arg, &n_pacs, &pacs_array);
    if (pacs == NULL) {
        return NULL;
    }

    /* Create the array for the scores */
    res_dims[0] = n_pacs;
    res = (PyArrayObject *) PyArray_ZEROS(1, res_dims, SCORE_TYPE, 0);
    res_array = (Score *) PyArray_DATA(res);

    /* Run the tournament. */
    run_tour_core(n_pacs, pacs_array, res_array);

    Py_DECREF(pacs);
    return (PyObject *) res;
}

PyDoc_STRVAR(run_tour__doc__,
"Run tournament among the given Pac-mite genes.\n\n"
"The genes can be stored in a Nx50 byte numpy array in C format.  The results "
"will be given as a numpy unsigned integer array holding the scores from the "
"tournament.\n"
);


/*
 * Python module
 * -------------
 */


static PyMethodDef tour_methods[] = {
    {"run_tournament", run_tour, METH_VARARGS, run_tour__doc__},
    {NULL, NULL}           /* sentinel */
};

PyDoc_STRVAR(tour__doc__,
"The extension module for running tournaments among Pac-mites.\n\n"
"Here a group of Pac-mites are going to be given as Nx50 byte arrays in "
"numpy.  Then their tournament will be run with C efficiency.\n"
);

static int
tour_exec(PyObject *m)
{
    import_array();
    return 0;
}


static struct PyModuleDef_Slot tour_slots[] = {
    {Py_mod_exec, tour_exec},
    {0, NULL},
};

static struct PyModuleDef tour_module = {
    PyModuleDef_HEAD_INIT,
    "evolpac.duel.tournament",
    tour__doc__,
    0,
    tour_methods,
    tour_slots,
    NULL,
    NULL,
    NULL
};


PyMODINIT_FUNC
PyInit_tournament(void)
{
    return PyModuleDef_Init(&tour_module);
}

