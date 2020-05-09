#include <ros/ros.h>
#include <vector>
#include <math.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_ros/point_cloud.h>
#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include <pcl/filters/passthrough.h>
#include <pcl/filters/voxel_grid.h>
#include <stdio.h>
#include <boost/foreach.hpp>
#include <pcl/visualization/pcl_visualizer.h>
#include <boost/thread/thread.hpp>
#include <pcl/features/normal_3d.h>
#include <pcl/features/moment_of_inertia_estimation.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <std_msgs/String.h>
#include <sstream>

typedef pcl::PointCloud<pcl::PointXYZ> PointCloud;

boost::shared_ptr<pcl::visualization::PCLVisualizer>
simpleVis(pcl::PointCloud<pcl::PointXYZ>::ConstPtr cloud)
{
  boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer (new pcl::visualization::PCLVisualizer("3D Viewer"));
  viewer->setBackgroundColor(0, 0, 0);
  viewer->addPointCloud<pcl::PointXYZ> (cloud,"sample cloud1");
  viewer->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "sample cloud1");
  viewer->initCameraParameters ();
  return (viewer);
}

void callback(const PointCloud::ConstPtr& msg)
{
  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<std_msgs::String>("/kinect_data",100);
  ROS_INFO("I heard: [%d] [%d]",msg->width, msg->height);
  boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer;
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_pass (new pcl::PointCloud<pcl::PointXYZ>());
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_pass1 (new pcl::PointCloud<pcl::PointXYZ>()); 
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_vox (new pcl::PointCloud<pcl::PointXYZ>());
  pcl::PassThrough<pcl::PointXYZ> pass;
  pcl::PassThrough<pcl::PointXYZ> pass1;
  pass.setInputCloud (msg);
  pass.setFilterFieldName ("y");
  pass.setFilterLimits (0.0, 8.0);
  pass.setFilterLimitsNegative (true);
  pass.filter (*cloud_pass);
  ROS_INFO("I heard: [%d] [%d]",cloud_pass->width, cloud_pass->height);
  //pass1.setInputCloud (cloud_pass);
  //pass1.setFilterFieldName ("y");
  //pass1.setFilterLimits (100.0, 200.0);
  //pass1.setFilterLimitsNegative (true);
  //pass1.filter (*cloud_pass1);
  ROS_INFO("I heard: [%d] [%d]",cloud_pass1->width, cloud_pass1->height);
  std::cout<<"pass done\n";
  pcl::VoxelGrid<pcl::PointXYZ> vox;
  vox.setInputCloud (cloud_pass);
  vox.setLeafSize (0.04f, 0.04f, 0.04f);
  vox.filter (*cloud_vox);
  std::cout<<"vox done\n";
  ROS_INFO("I heard: [%d] [%d]",cloud_vox->width, cloud_vox->height);
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud (cloud_vox);
  std::vector<pcl::PointIndices> cluster_indices;
  pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  ec.setClusterTolerance (0.05); // 2cm
  ec.setMinClusterSize (50);
  ec.setMaxClusterSize (10000);
  ec.setSearchMethod (tree);
  ec.setInputCloud (cloud_vox);
  ec.extract (cluster_indices);  
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
  int j = 0;
  std::vector<std::vector<float> > moi, xcor;
  for (std::vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin (); it != cluster_indices.end (); ++it)
  {
    j++;
    pcl::PointCloud<pcl::PointXYZ>::Ptr clusters (new pcl::PointCloud<pcl::PointXYZ>);
    for (std::vector<int>::const_iterator pit = it->indices.begin (); pit != it->indices.end (); ++pit)
    {
      clusters->points.push_back (cloud_vox->points[*pit]); //*      
      cloud_cluster->points.push_back (cloud_vox->points[*pit]); //*
      //cloud_cluster->width = 0;
      //cloud_cluster->height = 0;
    }
    pcl::MomentOfInertiaEstimation <pcl::PointXYZ> feature_extractor;
    feature_extractor.setInputCloud (clusters);
    feature_extractor.compute ();
    std::vector <float> moment_of_inertia;
    std::vector <float> eccentricity;
    pcl::PointXYZ min_point_AABB;
    pcl::PointXYZ max_point_AABB;
    pcl::PointXYZ min_point_OBB;
    pcl::PointXYZ max_point_OBB;
    pcl::PointXYZ position_OBB;
    Eigen::Matrix3f rotational_matrix_OBB;
    float major_value, middle_value, minor_value;
    Eigen::Vector3f major_vector, middle_vector, minor_vector;
    Eigen::Vector3f mass_center;
    feature_extractor.getMomentOfInertia (moment_of_inertia);
    feature_extractor.getEccentricity (eccentricity);
    feature_extractor.getAABB (min_point_AABB, max_point_AABB);
    feature_extractor.getOBB (min_point_OBB, max_point_OBB, position_OBB, rotational_matrix_OBB);
    feature_extractor.getEigenValues (major_value, middle_value, minor_value);
    feature_extractor.getEigenVectors (major_vector, middle_vector, minor_vector);
    feature_extractor.getMassCenter (mass_center);  
    //for(int i=j-1; i<=j; j++)
    //{
    std::vector<float> row1;
    for(int k=0;k<2;k++)
      row1.push_back(mass_center[k]);
    moi.push_back(row1);
    //}
     //for(int i=j-1; i<=j; j++)
    //{
    std::vector<float> row2;
    row2.push_back(min_point_AABB.x);
    row2.push_back(max_point_AABB.x);
    row2.push_back(min_point_AABB.z);
    row2.push_back(max_point_AABB.z);
    row2.push_back(min_point_AABB.y);
    row2.push_back(max_point_AABB.y);
    xcor.push_back(row2);
    //}
  }
  std::cout<<endl<<j<<endl;
  std::stringstream ss;
  std_msgs::String kin_val;
  //for(int i=0;i<j;i++)
  //std::cout<<moi[i][0]<<" "<<moi[i][1]<<endl;
  for(int i=0; i<j; i++)
      {
        if(xcor[i][2]<2.0 && abs(xcor[i][5]-xcor[i][4]>0.15))
        {
          //std::cout<<moi[i][1]<<" dist = "<<xcor[i][2]<<endl;
          if(moi[i][0]>=0)
	  {
            std::cout<<"left\n";
	    ss << "left";
            kin_val.data = ss.str();
	    goto label;
	  }
          else //if(fabs(xcor[i][0])>fabs(xcor[i][1]))
	  {
            std::cout<<"right\n";
    	    ss << "right";
            kin_val.data = ss.str();
	    goto label;
	  }
        }
	//else
       }
	std::cout<<"straight\n";
	ss << "straight";
  	kin_val.data = ss.str();
      label:
	pub.publish(kin_val);
  /*viewer = simpleVis(cloud_cluster);  
  //viewer = simpleVis(cloud_vox);  
  while(!viewer->wasStopped())
  {
     viewer->spinOnce(100);
     boost::this_thread::sleep(boost::posix_time::microseconds(100000));
  }*/
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "intel");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/camera/depth/color/points", 1, callback);
  ros::spin();
  return 0;
} 

