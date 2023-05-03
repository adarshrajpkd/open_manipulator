// Generated by gencpp from file moveit_msgs/RenameRobotStateInWarehouse.msg
// DO NOT EDIT!


#ifndef MOVEIT_MSGS_MESSAGE_RENAMEROBOTSTATEINWAREHOUSE_H
#define MOVEIT_MSGS_MESSAGE_RENAMEROBOTSTATEINWAREHOUSE_H

#include <ros/service_traits.h>


#include <moveit_msgs/RenameRobotStateInWarehouseRequest.h>
#include <moveit_msgs/RenameRobotStateInWarehouseResponse.h>


namespace moveit_msgs
{

struct RenameRobotStateInWarehouse
{

typedef RenameRobotStateInWarehouseRequest Request;
typedef RenameRobotStateInWarehouseResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct RenameRobotStateInWarehouse
} // namespace moveit_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouse > {
  static const char* value()
  {
    return "073dc05c3fd313b947cea483c25c46b0";
  }

  static const char* value(const ::moveit_msgs::RenameRobotStateInWarehouse&) { return value(); }
};

template<>
struct DataType< ::moveit_msgs::RenameRobotStateInWarehouse > {
  static const char* value()
  {
    return "moveit_msgs/RenameRobotStateInWarehouse";
  }

  static const char* value(const ::moveit_msgs::RenameRobotStateInWarehouse&) { return value(); }
};


// service_traits::MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouseRequest> should match
// service_traits::MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouse >
template<>
struct MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouseRequest>
{
  static const char* value()
  {
    return MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouse >::value();
  }
  static const char* value(const ::moveit_msgs::RenameRobotStateInWarehouseRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::moveit_msgs::RenameRobotStateInWarehouseRequest> should match
// service_traits::DataType< ::moveit_msgs::RenameRobotStateInWarehouse >
template<>
struct DataType< ::moveit_msgs::RenameRobotStateInWarehouseRequest>
{
  static const char* value()
  {
    return DataType< ::moveit_msgs::RenameRobotStateInWarehouse >::value();
  }
  static const char* value(const ::moveit_msgs::RenameRobotStateInWarehouseRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouseResponse> should match
// service_traits::MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouse >
template<>
struct MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouseResponse>
{
  static const char* value()
  {
    return MD5Sum< ::moveit_msgs::RenameRobotStateInWarehouse >::value();
  }
  static const char* value(const ::moveit_msgs::RenameRobotStateInWarehouseResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::moveit_msgs::RenameRobotStateInWarehouseResponse> should match
// service_traits::DataType< ::moveit_msgs::RenameRobotStateInWarehouse >
template<>
struct DataType< ::moveit_msgs::RenameRobotStateInWarehouseResponse>
{
  static const char* value()
  {
    return DataType< ::moveit_msgs::RenameRobotStateInWarehouse >::value();
  }
  static const char* value(const ::moveit_msgs::RenameRobotStateInWarehouseResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // MOVEIT_MSGS_MESSAGE_RENAMEROBOTSTATEINWAREHOUSE_H