/* DDR4.read(size, address)   
   DDR4.write(address, data)
   DDR4.erase(addr)
 */

#include "/usr/include/python3.5m/Python.h"
#include "lpddr4.h"

static PyObject* rread(PyObject* self, PyObject* args)
{	
    int addr; 	
    if (!PyArg_ParseTuple(args, "i", &addr)) {
    return NULL;
   }
    	
    int val = ram_read(addr);
 
    return Py_BuildValue("i", val);
}

static PyObject* rwrite(PyObject* self, PyObject* args)
{
    int addr, data;
     	
    if (!PyArg_ParseTuple(args, "ii", &addr, &data)) {
    return NULL;
   }
    	
    ram_write(addr, data); 
    
    return Py_None;
   }

static PyObject* erase(PyObject* self, PyObject* args)
{
    int addr;
     	
    if (!PyArg_ParseTuple(args, "i", &addr)) {
    return NULL;
   }
    	
    ram_write(addr, 0x0000); 
    
    return Py_None;
   }

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "read", rread, METH_VARARGS, "Reads an LPDDR4 address" },
    { "write", rwrite, METH_VARARGS, "Writes to an LPDDR4 address" },
    { "erase", erase, METH_VARARGS, "Erases the LPDDR4 data at the given address" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef DDR4 = {
    PyModuleDef_HEAD_INIT,
    "DDR4",
    "DDR4",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_DDR4(void)
{
    return PyModule_Create(&DDR4);
}
	
