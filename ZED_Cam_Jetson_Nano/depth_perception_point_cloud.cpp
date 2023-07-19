/* Add Notes 
*/
#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/PointCloud2.h>
#include <geometry_msgs/Point32.h>
#include <std_msgs/Float32.h>
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <depth_recognition/msg_PX.h>

#define midpoint_offset_x  0
#define midpoint_offset_y  0.15
#define midpoint_offset_z  0.10

using namespace message_filters;

geometry_msgs::Point32 coordinates; 
sensor_msgs::PointCloud2 PointCloudData;

uint32_t image_width; 
uint32_t image_height;

std_msgs::Header PointCloudHeader;
std_msgs::Header DepthHeader;

/* Callback function that calculates the x,y and z coordinates of the detected pixel */
void pointcloudCallback(const sensor_msgs::PointCloud2::ConstPtr& msg, const depth_recognition::msg_PX::ConstPtr& detected_pixel){

    PointCloudData = *msg; 
    int x = detected_pixel->xCoord;                
    int y = detected_pixel->yCoord; 


    int arrayPosition = y*PointCloudData.row_step + x*PointCloudData.point_step;
    int arrayPosX = arrayPosition + PointCloudData.fields[0].offset; //offset for x = 0 
    int arrayPosY = arrayPosition + PointCloudData.fields[1].offset; //offset for y = 4
    int arrayPosZ = arrayPosition + PointCloudData.fields[2].offset; //offset for z = 8


    memcpy(&coordinates.x, &PointCloudData.data[arrayPosX], sizeof(float));
    memcpy(&coordinates.y, &PointCloudData.data[arrayPosY], sizeof(float));
    memcpy(&coordinates.z, &PointCloudData.data[arrayPosZ], sizeof(float));

    ROS_INFO("x-coordinate : %g m", coordinates.x);
    ROS_INFO("y-coordinate : %g m", coordinates.y);
    ROS_INFO("z-coordinate : %g m", coordinates.z);

}

int main(int argc, char** argv) {

    ros::init(argc, argv, "depth_per_point_cloud");

    ros::NodeHandle n;

    message_filters::Subscriber<sensor_msgs::PointCloud2> subObjectPointCloud(n, "/zed/zed_node/point_cloud/cloud_registered", 1);    
    message_filters::Subscriber<depth_recognition::msg_PX> subObjectCenterPixel(n, "/centerPixelBB_topic", 1);
    typedef sync_policies::ApproximateTime<sensor_msgs::PointCloud2, depth_recognition::msg_PX> MySyncPolicy;

    Synchronizer<MySyncPolicy> sync(MySyncPolicy(10), subObjectPointCloud, subObjectCenterPixel);
    sync.registerCallback(boost::bind(&pointcloudCallback, _1, _2));

    ros::Publisher pubPointCloud = n.advertise<geometry_msgs::Point32>("point_cloud_coordinates", 10);

    //Run loop monitor callbacks at 10Hz
    ros::Rate loop_rate(10);
    ros::spinOnce();

    while(ros::ok()){

    pubPointCloud.publish(coordinates);
    ros::spinOnce();
    loop_rate.sleep();

    }

    return 0;
}
