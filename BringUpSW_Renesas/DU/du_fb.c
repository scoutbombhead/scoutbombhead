#include "du_fb.h"

uint32_t pixel_color(uint8_t r, uint8_t g, uint8_t b, struct fb_var_screeninfo *vinfo)
{
	return (r<<vinfo->red.offset) | (g<<vinfo->green.offset) | (b<<vinfo->blue.offset);
}

void bg(uint8_t r_val, uint8_t g_val, uint8_t b_val) {


	fb_fd = open("/dev/fb0",O_RDWR);

	//Get variable screen information
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);
	vinfo.grayscale=0;
	vinfo.bits_per_pixel=32;
	ioctl(fb_fd, FBIOPUT_VSCREENINFO, &vinfo);
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);

	ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo);

	screensize = vinfo.yres_virtual * finfo.line_length;

	 uint8_t *fbp = mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, (off_t)0);

	int x,y;

	for (x=0;x<vinfo.xres;x++)
		for (y=0;y<vinfo.yres;y++)
		{
			location = (x+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (y+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
		}

}

void chess(void){


	fb_fd = open("/dev/fb0",O_RDWR);

	//Get variable screen information
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);
	vinfo.grayscale=0;
	vinfo.bits_per_pixel=32;
	ioctl(fb_fd, FBIOPUT_VSCREENINFO, &vinfo);
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);

	ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo);

	screensize = vinfo.yres_virtual * finfo.line_length;

	uint8_t *fbp = mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, (off_t)0);

   	//int row, col, i, j, color=1, 
	
	int color = 1, row_count=0, col_count=0;

   
  for(i=1; i<9; i++){
       for(col=col_count; col<i*(vinfo.xres/8); col++){
	if(col%(vinfo.xres/10)==0){
	  color=1-color; 
		}//end if 	
           for(j=1; j<9; j++){
               for(row=row_count; row<j*(vinfo.yres/8); row++){
                   switch (color){
                    case 0: 
			location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(0x00,0x00,0x00, &vinfo);
                    break;
                    case 1:
			location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(0xFF,0xFF,0xFF, &vinfo);
                    break;
                   }//end for switch
               }//end for row
               row_count = row; 
               color=1-color;
           }//end for j
           row_count=0;
       }//end for col
	col_count=col; 
   }//end for i


}

void color_gradient1(void){



	fb_fd = open("/dev/fb0",O_RDWR);

	//Get variable screen information
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);
	vinfo.grayscale=0;
	vinfo.bits_per_pixel=32;
	ioctl(fb_fd, FBIOPUT_VSCREENINFO, &vinfo);
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);

	ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo);

	screensize = vinfo.yres_virtual * finfo.line_length;

	uint8_t *fbp = mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, (off_t)0);
   
    	r_val=0x0, g_val=0x0, b_val=0x0, i=0; 

for(row=i*(vinfo.yres/4); row<i+1*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val++;
            }

        }
         r_val=0;
    }

    for(row=i+1*(vinfo.yres/4); row<i+2*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                g_val++;
            }

        }
         g_val=0;
    }

    for(row=i+2*(vinfo.yres/4); row<i+3*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                b_val++;
            }

        }
         b_val=0;
    }

    for(row=i+3*(vinfo.yres/4); row<i+4*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val++;
                g_val++;
                b_val++;
            }

        }

        r_val=0;
        g_val=0;
        b_val=0;

    }
 }


void color_gradient2 (void) {


	fb_fd = open("/dev/fb0",O_RDWR);

	//Get variable screen information
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);
	vinfo.grayscale=0;
	vinfo.bits_per_pixel=32;
	ioctl(fb_fd, FBIOPUT_VSCREENINFO, &vinfo);
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);

	ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo);

	screensize = vinfo.yres_virtual * finfo.line_length;

	uint8_t *fbp = mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, (off_t)0);

	//int row, col, i=0, r_val=0xFF, g_val=0xFF, b_val=0xFF;  
    	r_val=0xFF, g_val=0xFF, b_val=0xFF, i=0; 

    for(row=i*(vinfo.yres/4); row<i+1*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val--;
            }

        }
         r_val=0xFF;
    }

    for(row=i+1*(vinfo.yres/4); row<i+2*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                g_val--;
            }

        }
         g_val=0xFF;
    }

    for(row=i+2*(vinfo.yres/4); row<i+3*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                b_val--;
            }

        }
         b_val=0xFF;
    }

    for(row=i+3*(vinfo.yres/4); row<i+4*(vinfo.yres/4); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
                        *((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val--;
                g_val--;
                b_val--;
            }

        }

        r_val=0xFF;
        g_val=0xFF;
        b_val=0xFF;

    }

}


void color_gradient3 (void){


	fb_fd = open("/dev/fb0",O_RDWR);

	//Get variable screen information
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);
	vinfo.grayscale=0;
	vinfo.bits_per_pixel=32;
	ioctl(fb_fd, FBIOPUT_VSCREENINFO, &vinfo);
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);

	ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo);

	screensize = vinfo.yres_virtual * finfo.line_length;

	uint8_t *fbp = mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, (off_t)0);

	//int row, col, i=0, r_val=0x0, g_val=0x0, b_val=0x0;  
 	r_val=0x0, g_val=0x0, b_val=0x0, i=0; 
    

    for(row=i*(vinfo.yres/8); row<i+1*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val++; 
            }
            
        }
         r_val=0;
    }

    for(row=i+1*(vinfo.yres/8); row<i+2*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                g_val++; 
            }
            
        }
         g_val=0;
    }

    for(row=i+2*(vinfo.yres/8); row<i+3*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                b_val++; 
            }
            
        }
         b_val=0;
    }

    for(row=i+3*(vinfo.yres/8); row<i+4*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val++; 
		g_val++; 
		b_val++; 
            }
            
        }

        r_val=0;
	g_val=0;
	b_val=0;

    }
	
	g_val=0xFF; b_val=0xFF; 
	
	for(row=i+4*(vinfo.yres/8); row<i+1+5*(vinfo.yres/8); row++){
	     for(col=0; col<vinfo.xres; col++){
	         location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
	         if(col!=0 && col%5==0){
	             r_val--; 
	          }
            
        }
         r_val=0xFF;
    }

    for(row=i+5*(vinfo.yres/8); row<i+6*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                g_val--; 
            }
            
        }
         g_val=0xFF;
    }

    for(row=i+6*(vinfo.yres/8); row<i+7*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                b_val--; 
            }
            
        }
         b_val=0xFF;
    }

    for(row=i+7*(vinfo.yres/8); row<i+8*(vinfo.yres/8); row++){
        for(col=0; col<vinfo.xres; col++){
            location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(r_val, g_val, b_val, &vinfo);
            if(col!=0 && col%5==0){
                r_val--; 
		g_val--; 
		b_val--; 
            }
            
        }

        r_val=0xFF;
	g_val=0xFF;
	b_val=0xFF;

    }

}

void check(void) {


	fb_fd = open("/dev/fb0",O_RDWR);

	//Get variable screen information
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);
	vinfo.grayscale=0;
	vinfo.bits_per_pixel=32;
	ioctl(fb_fd, FBIOPUT_VSCREENINFO, &vinfo);
	ioctl(fb_fd, FBIOGET_VSCREENINFO, &vinfo);

	ioctl(fb_fd, FBIOGET_FSCREENINFO, &finfo);

	screensize = vinfo.yres_virtual * finfo.line_length;

	uint8_t *fbp = mmap(0, screensize, PROT_READ | PROT_WRITE, MAP_SHARED, fb_fd, (off_t)0);

   	//int col, row;

    
    for(row=0; row<vinfo.yres; row++){
        if(row%(vinfo.yres/64)==0){
            for(col=0; col<vinfo.xres; col++){
			location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(0xFF,0xFF,0xFF, &vinfo);
            }//end col
        }//end for if
    }//end for row
    
    for(col=0; col<vinfo.xres; col++){
        if(col%(vinfo.xres/80)==0){
            for(row=0; row<vinfo.yres; row++){
                 	location = (col+vinfo.xoffset) * (vinfo.bits_per_pixel/8) + (row+vinfo.yoffset) * finfo.line_length;
			*((uint32_t*)(fbp + location)) = pixel_color(0xFF,0xFF,0xFF, &vinfo);
            }//end for row
        }//end if
    }//end for col



} 

