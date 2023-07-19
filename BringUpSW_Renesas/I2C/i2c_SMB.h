#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "i2c-dev.h"
//#include <i2c/smbus.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int i2c_read(int chNr, int SlAddr, int accAdd); 
void i2c_write(int chNr, int SlAddr, int accAdd, int data); 
