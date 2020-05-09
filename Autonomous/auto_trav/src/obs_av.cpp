#include <ros/ros.h>
#include <vector>
#include <math.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_ros/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/sample_consensus/ransac.h>
#include <pcl/sample_consensus/sac_model_plane.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <boost/foreach.hpp>
#include <pcl/visualization/pcl_visualizer.h>
#include <boost/thread/thread.hpp>
#include <pcl/ModelCoefficients.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/features/normal_3d.h>
#include <pcl/features/moment_of_inertia_estimation.h>
#include <pcl/kdtree/kdtree.h>
#include <std_msgs/String.h>
#include <sstream>

typedef pcl::PointCloud<pcl::PointXYZRGB> PointCloud;

void callback(const PointCloud::ConstPtr& msg)
{
  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<std_msgs::String>("/kinect_data",100);
  ROS_INFO("I heard: [%d] [%d]",msg->width, msg->height);
  boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer;
  pcl::VoxelGrid<pcl::PointXYZRGB> vg;
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr filtered (new pcl::PointCloud<pcl::PointXYZRGB>());
  vg.setInputCloud(msg);
  vg.setLeafSize(0.03f, 0.03f, 0.03f);
  vg.filter(*filtered);
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZRGB>);
  std::vector<int> inl;
  pcl::SampleConsensusModelPlane<pcl::PointXYZRGB>::Ptr model_p(new pcl::SampleConsensusModelPlane<pcl::PointXYZRGB> (filtered));
  pcl::RandomSampleConsensus<pcl::PointXYZRGB> ransac(model_p);
  ransac.setDistanceThreshold(0.05);
  ransac.computeModel();
  ransac.getInliers(inl);
  pcl::copyPointCloud<pcl::PointXYZRGB>(*filtered, inl, *cloud);
  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
  pcl::SACSegmentation<pcl::PointXYZRGB> seg;
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_plane (new pcl::PointCloud<pcl::PointXYZRGB> ()), cloud_f (new pcl::PointCloud<pcl::PointXYZRGB>);
  seg.setOptimizeCoefficients(true);
  seg.setModelType(pcl::SACMODEL_PLANE);
  seg.setMethodType(pcl::SAC_RANSAC);
  //seg.setMaxIterations (100);
  seg.setDistanceThreshold(0.05);
  int i = 0, nr_points = (int)filtered->points.size();
  while(filtered->points.size() > 0.4*nr_points)
  {
    seg.setInputCloud(filtered);
    seg.segment(*inliers, *coefficients);
    pcl::ExtractIndices<pcl::PointXYZRGB> extract;
    extract.setInputCloud(filtered);
    extract.setIndices(inliers);
    extract.setNegative(false);
    extract.filter (*cloud_plane);
    extract.setNegative (true);
    extract.filter (*cloud_f);
    *filtered = *cloud_f;    
  }
  // Creating the KdTree object for the search method of the extraction
  pcl::search::KdTree<pcl::PointXYZRGB>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZRGB>);
  tree->setInputCloud (filtered);
  std::vector<pcl::PointIndices> cluster_indices;
  pcl::EuclideanClusterExtraction<pcl::PointXYZRGB> ec;
  ec.setClusterTolerance (0.03); // 2cm
  ec.setMinClusterSize (50);
  ec.setMaxClusterSize (10000);
  ec.setSearchMethod (tree);
  ec.setInputCloud (filtered);
  ec.extract (cluster_indices);  
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZRGB>);
  int j = 0;
  std::vector<std::vector<float> > moi, xcor;
  for (std::vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin (); it != cluster_indices.end (); ++it)
  {
    j++;
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr clusters (new pcl::PointCloud<pcl::PointXYZRGB>);
    for (std::vector<int>::const_iterator pit = it->indices.begin (); pit != it->indices.end (); ++pit)
    {
      clusters->points.push_back (filtered->points[*pit]); //*      
      cloud_cluster->points.push_back (filtered->points[*pit]); //*
    }
    pcl::MomentOfInertiaEstimation <pcl::PointXYZRGB> feature_extractor;
    feature_extractor.setInputCloud (clusters);
    feature_extractor.compute ();
    std::vector <float> moment_of_inertia;
    std::vector <float> eccentricity;
    pcl::PointXYZRGB min_point_AABB;
    pcl::PointXYZRGB max_point_AABB;
    pcl::PointXYZRGB min_point_OBB;
    pcl::PointXYZRGB max_point_OBB;
    pcl::PointXYZRGB position_OBB;
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
    std::vector<float> row1;
    for(int k=0;k<2;k++)
      row1.push_back(mass_center[k]);
    moi.push_back(row1);
    std::vector<float> row2;
    row2.push_back(min_point_AABB.x);
    row2.push_back(max_point_AABB.x);
    row2.push_back(min_point_AABB.z);
    row2.push_back(max_point_AABB.z);
    row2.push_back(min_point_AABB.y);
    row2.push_back(max_point_AABB.y);
    xcor.push_back(row2);
  }
  std::cout<<endl<<j<<endl;
  std::stringstream ss;
  std_msgs::String kin_val;
  for(int i=0; i<j; i++)
      {
        if(xcor[i][2]<2.0 && xcor[i][5]-xcor[i][4]>0.15)
        {
          if(moi[i][0]>=0)
	  {
            std::cout<<"left\n";
	    ss << "left";
            kin_val.data = ss.str();
	    goto label;
	  }
          else 
	  {
            std::cout<<"right\n";
	    ss << "right";
            kin_val.data = ss.str();
	    goto label;
	  }
        }
       }
	std::cout<<"straight\n";
	ss << "straight";
  	kin_val.data = ss.str();
      label:
	pub.publish(kin_val);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "obs_av");
  ros::NodeHandle n;
  ros::Subscriber sub = n.subscribe("/camera/depth/color/points", 1, callback);
  ros::spin();
  return 0;
}
