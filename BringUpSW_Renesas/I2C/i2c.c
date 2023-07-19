/* I2C.read(ChNr, SlAdrr, accAddr)   
   I2C.write(ChNr, SlAdrr, accAddr, data) */

#include "/usr/include/python3.5m/Python.h"
#include "i2c_SMB.h"

static PyObject* rread(PyObject* self, PyObject* args)
{	
    int chNr, slAddr, accAdd; 	
    if (!PyArg_ParseTuple(args, "iii", &chNr, &slAddr, &accAdd)) {
    return NULL;
   }
    	
    int val = i2c_read(chNr, slAddr, accAdd);
 
    return Py_BuildValue("i", val);
}

static PyObject* rwrite(PyObject* self, PyObject* args)
{
   int chNr, slAddr, accAdd, data;
     	
    if (!PyArg_ParseTuple(args, "iiii", &chNr, &slAddr, &accAdd, &data)) {
    return NULL;
   }
    	
    i2c_write(chNr, slAddr, accAdd, data); 
    
    return Py_None;
   }


// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "read", rread, METH_VARARGS, "Reads byte from I2C register" },
    { "write", rwrite, METH_VARARGS, "Writes byte to I2C register" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef I2C = {
    PyModuleDef_HEAD_INIT,
    "i2c",
    "i2c",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_I2C(void)
{
    return PyModule_Create(&I2C);
}
	
