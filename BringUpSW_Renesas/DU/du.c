/* DU.bg_color(R, G, B)   
   DU.pattern( test_number)

*/

#include "/usr/include/python3.5m/Python.h"
#include "du_fb.h"

static PyObject* bg_color(PyObject* self, PyObject* args)
{	
    int r, g, b; 	
    if (!PyArg_ParseTuple(args, "iii", &r, &g, &b)) {
    return NULL;
   }
    	
    bg(r, g, b); 
 
    return Py_None;
}

static PyObject* pattern(PyObject* self, PyObject* args)
{
   int test_nr; 
     	
    if (!PyArg_ParseTuple(args, "i", &test_nr)) {
    return NULL;
   }
    	
    switch(test_nr){

	case 1: chess(); 
	break; 
	
	case 2: color_gradient1();
	break; 

	case 3: color_gradient2();
	break; 	
	
	case 4: color_gradient3();
	break; 

	case 5: check();
	break; 
	
	default: 
	printf("Please enter a valid test pattern number 1 - 5");
 
	} 
    
    return Py_None;
   }


// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "bg_color", bg_color, METH_VARARGS, "Changes the background color of the display" },
    { "pattern", pattern, METH_VARARGS, "Displays a pattern" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef DU = {
    PyModuleDef_HEAD_INIT,
    "du",
    "du",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_DU(void)
{
    return PyModule_Create(&DU);
}
