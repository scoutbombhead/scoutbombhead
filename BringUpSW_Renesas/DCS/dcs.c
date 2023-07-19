
#include "/usr/include/python3.5m/Python.h"
#include "video_capture.h"
#include "draw_framebuffer.h"

static PyObject* cam_on(PyObject* self, PyObject* args)
{	
        unsigned char src_image[IM_WIDTH * IM_HEIGHT * 3];
    	init_framebuffer();
	init_video_capture();
	char key = 0;

	for(; ;){
		key = video_capture(src_image);
		if(key == 'q'){
			break;
			}
		}
 
    return Py_None;
}

static PyObject* cam_off(PyObject* self, PyObject* args)
{
    free_video_capture();
	free_framebuffer();
    
    	return Py_None;
   }


// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "cam_om", cam_on, METH_VARARGS, "turns streaming on" },
    { "cam_off", cam_off, METH_VARARGS, "turns streaming off" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef DCS = {
    PyModuleDef_HEAD_INIT,
    "dcs",
    "dcs",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_DCS(void)
{
    return PyModule_Create(&DCS);
}
