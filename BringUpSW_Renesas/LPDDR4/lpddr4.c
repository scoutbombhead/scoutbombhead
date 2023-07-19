#include "lpddr4.h"

int ram_read(int addr) {

	int fd;
    	void *map_base, *virt_addr; 
	unsigned int read_result, writeval;
	off_t target = (unsigned int)addr;
	//int access_type = 32;

	//target = strtoul(addr, 0, 0);

    if((fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1) FATAL;
    printf("/dev/mem opened.\n"); 
    fflush(stdout);
    
    /* Map one page */
    map_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, target & ~MAP_MASK);
    if(map_base == (void *) -1) FATAL;
    printf("Memory mapped at address %p.\n", map_base); 
    fflush(stdout);
    
    virt_addr = map_base + (target & MAP_MASK);
    read_result = *((unsigned int *) virt_addr);


    	printf("Value at address 0x%X (%p): 0x%X\n", target, virt_addr, read_result); 
    	fflush(stdout);

	if(munmap(map_base, MAP_SIZE) == -1) FATAL;
    	close(fd);
   	return read_result; 


}

int ram_write(int addr, int data){

	int fd;
    	void *map_base, *virt_addr; 
	unsigned int read_result, writeval = data;
	off_t target = (unsigned int)addr;
	//int access_type = 32;

	//target = strtoul(addr, 0, 0);
	//writeval = strtoul(data, 0, 0);

	if((fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1) FATAL;
    	printf("/dev/mem opened.\n"); 
    	fflush(stdout);
    
    	/* Map one page */
    	map_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, target & ~MAP_MASK);
    	if(map_base == (void *) -1) FATAL;
    	printf("Memory mapped at address %p.\n", map_base); 
    	fflush(stdout);
    
    	virt_addr = map_base + (target & MAP_MASK);

	*((unsigned int *) virt_addr) = writeval;
	read_result = *((unsigned int *) virt_addr);

	
	printf("Written 0x%X; readback 0x%X\n", writeval, read_result); 
	fflush(stdout);

	if(munmap(map_base, MAP_SIZE) == -1) FATAL;
    	close(fd);
   	return read_result; 

}



