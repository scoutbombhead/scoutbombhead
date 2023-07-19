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
#define midpoint_offset_y  0.15 // in m
#define midpoint_offset_z  0.10 //in m

using namespace message_filters;

geometry_msgs::Point32 DetectedCoordinates; 
std_msgs::Float32 ObjectDepth;

/* Callback function that calculates the x,y and z coordinates of the detected pixel */
void transformCallback(const geometry_msgs::Point32::ConstPtr& msg){
 
    DetectedCoordinates.x = msg->x;
    DetectedCoordinates.y = msg->y;
    DetectedCoordinates.z = msg->z;

}

void ObjDepthCallback(const std_msgs::Float32::ConstPtr& msg_2){

    ObjectDepth = *msg_2; 

}
int main(int argc, char** argv) {

    ros::init(argc, argv, "depth_transform");

    ros::NodeHandle n;

    ros::Subscriber subObjectCoordinates = n.subscribe("/point_cloud_coordinates", 10, transformCallback);
    ros::Subscriber subObjectDepth = n.subscribe("/depthOfObject_topic", 10, ObjDepthCallback);

    ros::Publisher pubPointCloudDepth = n.advertise<std_msgs::Float32>("point_cloud_depth", 10);
    ros::Publisher pubDepth_robot_center = n.advertise<std_msgs::Float32>("depth_robot_center", 10);
    ros::Publisher pubDepthFromCam = n.advertise<std_msgs::Float32>("depth_distance_from_cam", 10);

    //Run loop monitor callbacks at 10Hz
    ros::Rate loop_rate(10);
    ros::spinOnce();

    while(ros::ok()){
    float PointCloudDepth = sqrt(DetectedCoordinates.x*DetectedCoordinates.x + DetectedCoordinates.y*DetectedCoordinates.y + DetectedCoordinates.z*DetectedCoordinates.z);
    float PointCloudDepthMP = sqrt(pow((DetectedCoordinates.x - midpoint_offset_x), 2) + pow((DetectedCoordinates.y - midpoint_offset_y), 2) + pow((DetectedCoordinates.z - midpoint_offset_z), 2));
    pubPointCloudDepth.publish(PointCloudDepth);
    pubDepth_robot_center.publish(PointCloudDepthMP);
    pubDepthFromCam.publish(ObjectDepth);
    ros::spinOnce();
    loop_rate.sleep();

    }

    return 0;
}
