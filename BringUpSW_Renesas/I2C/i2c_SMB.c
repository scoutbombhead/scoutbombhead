#include "i2c_SMB.h"

int i2c_read(int chNr, int SlAddr, int accAdd) {

	int file;
	int adapter_nr; 
	if(chNr == 0x1){
	adapter_nr = 4;
	}
	
	else {
	printf("Wrong I2C_Channel Nr\n");
	printf("Default I2C_Channel 4 selected\n");
	adapter_nr = 4;
	}	
	
	char filename[20];

	snprintf(filename, 19, "/dev/i2c-%d", adapter_nr);
 	file = open(filename, O_RDWR);
 	if (file < 0) {
	/* ERROR HANDLING; you can check errno to see what went wrong */
	exit(1);
  	}	

	if (ioctl(file, I2C_SLAVE, SlAddr) < 0) {
	/* ERROR HANDLING; you can check errno to see what went wrong */
	exit(1);
	}

	__u8 reg = accAdd; /* Device register to access */
	__s32 res;
	//char buf[10];
	
 	/* Using SMBus commands */
  	res = i2c_smbus_read_byte_data(file, reg);
  	if (res < 0) {
    	/* ERROR HANDLING: i2c transaction failed */
  	} else {
    	/* res contains the read word */
  	}
	

}

void i2c_write(int chNr, int SlAddr, int accAdd, int data) {

	int file;
	int adapter_nr; 
	if(chNr == 0x1){
	adapter_nr = 4;
	}
	
	else {
	printf("Wrong I2C_Channel Nr\n");
	printf("Default I2C_Channel 4 selected\n");
	adapter_nr = 4;
	}	
	
	char filename[20];

	snprintf(filename, 19, "/dev/i2c-%d", adapter_nr);
 	file = open(filename, O_RDWR);
 	if (file < 0) {
	/* ERROR HANDLING; you can check errno to see what went wrong */
	exit(1);
  	}	

	if (ioctl(file, I2C_SLAVE, SlAddr) < 0) {
	/* ERROR HANDLING; you can check errno to see what went wrong */
	exit(1);
	}

	__u8 reg = accAdd; /* Device register to access */
	//char buf[10];
	
 	/* Using SMBus commands */
  	int succ = i2c_smbus_write_byte_data(file, reg, data);
  	if (succ < 0) {
    	/* ERROR HANDLING: i2c transaction failed */
	printf("I2C write failed\n");
  	} else {
    	/* res contains the read word */
	//printf("Byte written: 0x%X\n", byte_written);
  	}






}

