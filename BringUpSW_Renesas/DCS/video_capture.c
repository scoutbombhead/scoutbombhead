#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <fcntl.h>             
#include <errno.h>
#include <string.h>             
#include <sys/stat.h>          
#include <linux/videodev2.h>    
#include <sys/mman.h>          
#include <unistd.h>             
#include <sys/time.h>           
#include <limits.h>             
#include "video_capture.h"


static char* dev_name = "/dev/video0";
static int fd = -1; /* vidoe0 file descriptor*/

FILE *fout; 	
char out_name[256]; 

/* Queried image buffers! */
struct buffer* buffers = NULL;
static unsigned int n_buffers = 0;
struct v4l2_buffer buf_in_while_loop;
static fd_set fds;
struct timeval tv;

/* wrapped errno display function by v4l2 API */
static void errno_exit(const char * s) {
	fprintf(stderr, "%s error %d, %s\n", s, errno, strerror(errno));
	exit(EXIT_FAILURE);
}

/* wrapped ioctrl function by v4l2 API */
static int xioctl(int fd, int request, void * arg) {
	int r;
	do{
		r = ioctl(fd, request, arg);
	}
	while(-1 == r && EINTR == errno);
	return r;
}

static void open_device() {
	struct stat st;
	if (-1 == stat(dev_name, &st)) {
		fprintf(stderr, "Cannot identify '%s': %d, %s\n", dev_name, errno, strerror(errno));
		exit(EXIT_FAILURE);
	}
	if (!S_ISCHR(st.st_mode)) {
		fprintf(stderr, "%s is no device\n", dev_name);
		exit(EXIT_FAILURE);
	}
	fd = open(dev_name, O_RDWR | O_NONBLOCK, 0);
	if (-1 == fd) {
		fprintf(stderr, "Cannot open '%s': %d, %s\n", dev_name, errno, strerror(errno));
		exit(EXIT_FAILURE);
	}
}

/*
 * 1. Memory mapped buffers are located in device memory and must be allocated with this ioctl
 * 	  before they can be mapped into the application's address space
 * 2. set four images in buffer
 */
static void init_mmap() {
	struct v4l2_requestbuffers req;
	CLEAR(req);
	req.count = 4;
	req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	req.memory = V4L2_MEMORY_MMAP;
	/* Initiate Memory Mapping */
	if (-1 == xioctl(fd, VIDIOC_REQBUFS, &req)) {
		if (EINVAL == errno) {
			fprintf(stderr, "%s does not support memory mapping\n", dev_name);
			exit(EXIT_FAILURE);
		} else {
			errno_exit("VIDIOC_REQBUFS");
		}
	}
	/* video output requires at least two buffers, one displayed and one filled by the application */
	if (req.count < 2) {
		fprintf(stderr, "Insufficient buffer memory on %s\n", dev_name);
		exit(EXIT_FAILURE);
	}
	buffers = calloc(req.count, sizeof(*buffers));

	if (!buffers) {
		fprintf(stderr, "Out of memory\n");
		exit(EXIT_FAILURE);
	}
	for (n_buffers = 0; n_buffers < req.count; ++n_buffers) {
		struct v4l2_buffer buf;
		CLEAR(buf);
		buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		buf.memory = V4L2_MEMORY_MMAP;
		buf.index = n_buffers;
		/* Query the status of a buffer */
		if (-1 == xioctl(fd, VIDIOC_QUERYBUF, &buf)){
			errno_exit("VIDIOC_QUERYBUF");
		}
		buffers[n_buffers].length = buf.length; //640 * 480 * 2 = 614400
		buffers[n_buffers].start = mmap(NULL /* start anywhere */, buf.length,
		PROT_READ | PROT_WRITE /* required */,
		MAP_SHARED /* recommended */, fd, buf.m.offset);

		if (MAP_FAILED == buffers[n_buffers].start){
			errno_exit("mmap");
		}
	}
}

/* set video streaming format here(width, height, pixel format, cropping, scaling) */
static void init_device() {
	struct v4l2_capability cap;
	struct v4l2_format fmt;
	unsigned int min;
	if (-1 == xioctl(fd, VIDIOC_QUERYCAP, &cap)) {
		if (EINVAL == errno) {
			fprintf(stderr, "%s is no V4L2 device\n", dev_name);
			exit(EXIT_FAILURE);
		} else {
			errno_exit("VIDIOC_QUERYCAP");
		}
	}
	if (!(cap.capabilities & V4L2_CAP_VIDEO_CAPTURE)) {
		fprintf(stderr, "%s is no video capture device\n", dev_name);
		exit(EXIT_FAILURE);
	}
	if (!(cap.capabilities & V4L2_CAP_STREAMING)) {
		fprintf(stderr, "%s does not support streaming i/o\n", dev_name);
		exit(EXIT_FAILURE);
	}
	CLEAR(fmt);
	fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	fmt.fmt.pix.width = IM_WIDTH;
	fmt.fmt.pix.height = IM_HEIGHT;
	fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_ABGR32;
	fmt.fmt.pix.field = V4L2_FIELD_INTERLACED;
	if (-1 == xioctl(fd, VIDIOC_S_FMT, &fmt)){
		errno_exit("VIDIOC_S_FMT");
	}
	/* YUYV sampling 4 2 2, so bytes per pixel is 2*/
	min = fmt.fmt.pix.width * 2;
	if (fmt.fmt.pix.bytesperline < min){
		fmt.fmt.pix.bytesperline = min;
	}
	min = fmt.fmt.pix.bytesperline * fmt.fmt.pix.height;
	if (fmt.fmt.pix.sizeimage < min){
		fmt.fmt.pix.sizeimage = min;
	}
	init_mmap();
}

static void start_capturing() {
	unsigned int i;
	enum v4l2_buf_type type;
	for (i = 0; i < n_buffers; ++i) {
		struct v4l2_buffer buf;
		CLEAR(buf);
		buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		buf.memory = V4L2_MEMORY_MMAP;
		buf.index = i;
		/* enqueue an empty (capturing) or filled (output) buffer in the driver's incoming queue */
		if (-1 == xioctl(fd, VIDIOC_QBUF, &buf)){
			errno_exit("VIDIOC_QBUF");
		}
	}
	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	/* Start streaming I/O */
	if (-1 == xioctl(fd, VIDIOC_STREAMON, &type)){
		errno_exit("VIDIOC_STREAMON");
	}
}

static void close_device() {
	if (-1 == close(fd))
		errno_exit("close");
	fd = -1;
}

static void stop_capturing() {
	enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	if (-1 == xioctl(fd, VIDIOC_STREAMOFF, &type)){
		errno_exit("VIDIOC_STREAMOFF");
	}
}

static void uninit_device() {
	unsigned int i;
	for (i = 0; i < n_buffers; ++i){
		if (-1 == munmap(buffers[i].start, buffers[i].length)){
			errno_exit("munmap");
		}
	}
	free(buffers);
}


void init_video_capture(){
	open_device();
	init_device();
	start_capturing();
}

char video_capture(unsigned char* dst){
	struct v4l2_buffer buf;
	char key = 0;
	FD_ZERO(&fds);
	FD_SET(fd, &fds);
	FD_SET(fileno(stdin), &fds);
	/* Timeout. */
	tv.tv_sec = 2;
	tv.tv_usec = 0;
	select(fd + 1, &fds, NULL, NULL, &tv);

	if(FD_ISSET(fileno(stdin), &fds)){
		read(fileno(stdin), &key, 1);
		printf("key: %c\n", key);
		return key;
	}

	if(FD_ISSET(fd, &fds)){
		CLEAR(buf_in_while_loop);
		buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		buf.memory = V4L2_MEMORY_MMAP;
		/* dequeue from buffer */
		if(-1 == xioctl(fd, VIDIOC_DQBUF, &buf_in_while_loop)){
			switch(errno){
			case EAGAIN:
				return 0;
			default:
				errno_exit("VIDIOC_DQBUF");
			}
		}
		
		sprintf(out_name, "/dev/fb%d", 0);
                fout = fopen(out_name, "w");
                if (!fout) {
                        perror("Cannot open image");
                        exit(EXIT_FAILURE);
                }
                
                fwrite(buffers[buf.index].start, buf.bytesused, 1, fout);
                fclose(fout);
				
		/* queue-in buffer */
		if(-1 == xioctl(fd, VIDIOC_QBUF, &buf_in_while_loop)){
			errno_exit("VIDIOC_QBUF");
		}
		
		
	
	}
	return 0;
}

void free_video_capture(){
	stop_capturing();
	uninit_device();
	close_device();
}
