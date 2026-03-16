cmake_minimum_required(VERSION 3.8)
project(rbe3002_tests)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(ament_cmake_pytest REQUIRED)

find_package(control REQUIRED)

install(DIRECTORY
  test
  DESTINATION share/${PROJECT_NAME}/
)

set(AMENT_LINT_AUTO_EXCLUDE
  ament_flake8
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpklint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
