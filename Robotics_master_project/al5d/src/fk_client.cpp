#include "ros/ros.h"
#include "al5d/Fk.h"
#include <cstdlib>
#include "geometry_msgs/Point.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "fk_client");
  if (argc != 6)
  {
    ROS_INFO("usage: Please give the 5 joint angles for FK: j1 j2 j3 j4 j5");
    return 1;
  }

  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<al5d::Fk>("al5d_fk");
  al5d::Fk srv;
  srv.request.j1 = std::stof(argv[1]);
  srv.request.j2 = std::stof(argv[2]);
  srv.request.j3 = std::stof(argv[3]);
  srv.request.j4 = std::stof(argv[4]);
  srv.request.j5 = std::stof(argv[5]);

  if (client.call(srv))
  {
    //ROS_INFO("Sum: %ld", (long int)srv.response.sum);
    ROS_INFO("Doing FK..");
    ROS_INFO("x: %f, y: %f, z: %f", srv.response.target.x, 
    srv.response.target.y, srv.response.target.z);
  }
  else
  {
    ROS_ERROR("Failed to call service");
    return 1;
  }

  return 0;
}
