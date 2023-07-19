#include "ros/ros.h"
#include "al5d/Fk.h"
#include "geometry_msgs/Point.h"
#include <kdl/chain.hpp>
#include <kdl/chainfksolver.hpp>
#include <kdl/chainfksolverpos_recursive.hpp>
#include <kdl/frames_io.hpp>
#include <stdio.h>
#include <iostream>

#define H 0.63
#define L1 1.46
#define L2 1.87
#define L3 0.86

using namespace KDL;


bool handle_fk(al5d::Fk::Request &req, al5d::Fk::Response &res)
{
  //Do forward kinematics
  JntArray jointAngles = JntArray(5);
  jointAngles(0) = req.j1;       // Joint 1
	jointAngles(1) = req.j2;        // Joint 2
	jointAngles(2) = req.j3;             // Joint 3
	jointAngles(3) = req.j4;             // Joint 4
	jointAngles(4) = req.j5;             // Joint 5
  //ROS_INFO("request: x=%ld, y=%ld", (long int)req.a, (long int)req.b);
  // ROS_INFO("sending back response: [%ld]", (long int)res.sum);
  
  Chain kdlChain = Chain();
  kdlChain.addSegment(Segment(Joint(Joint::RotZ),Frame::DH(0.0, M_PI/2, H, 0.0)));
	kdlChain.addSegment(Segment(Joint(Joint::RotZ),Frame::DH(L1, 0.0, 0.0, 0.0)));
	kdlChain.addSegment(Segment(Joint(Joint::RotZ),Frame::DH(L2, 0.0, 0.0, 0.0)));
	kdlChain.addSegment(Segment(Joint(Joint::RotZ),Frame::DH(L3, 0.0, 0.0, 0.0)));
	kdlChain.addSegment(Segment(Joint(Joint::RotZ),Frame::DH(0.0, M_PI/2, 0.0, -M_PI/2)));

  ChainFkSolverPos_recursive FKSolver = ChainFkSolverPos_recursive(kdlChain);
	
	// Create the frame that will contain the results
  KDL::Frame cartpos;    
 
  // Calculate forward position kinematics
  bool kinematics_status;
  kinematics_status = FKSolver.JntToCart(jointAngles,cartpos);
  // Set precision for all values
  for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++) {
			double a = cartpos(i, j);
			if (a < 0.0001 && a > -0.001) {
				a = 0.0;
			}
		}
	}

  res.target.x = cartpos(0, 3);
  res.target.y = cartpos(1, 3);
  res.target.z = cartpos(2, 3);

  return(true);

}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "fk_server");
  ros::NodeHandle n;

  ros::ServiceServer service = n.advertiseService("al5d_fk", handle_fk);
  ROS_INFO("Ready to do FK.");
  ros::spin();

  return 0;
}
