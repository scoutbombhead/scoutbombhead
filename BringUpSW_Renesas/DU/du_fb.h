#include <linux/fb.h>
#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

struct fb_fix_screeninfo finfo;
struct fb_var_screeninfo vinfo;

int fb_fd; 
long screensize;
uint8_t *fbp; 
long location; 
int row, col, i, j, r_val, g_val, b_val; 


uint32_t pixel_color(uint8_t r, uint8_t g, uint8_t b, struct fb_var_screeninfo *vinfo); 
void bg(uint8_t r_val, uint8_t g_val, uint8_t b_val); 
void chess(void);
void color_gradient1(void); 
void color_gradient2(void); 
void color_gradient3(void); 
void check(void); 

 
 
