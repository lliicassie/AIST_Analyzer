

cmake_policy(SET CMP0148 NEW)

cmake_minimum_required(VERSION 3.10)
project(AIST_Analyzer VERSION 1.0)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 启用 Qt 自动处理
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)




# 使用环境变量设置 Python 路径
if(DEFINED ENV{PYTHON_EXECUTABLE})
    set(Python3_EXECUTABLE $ENV{PYTHON_EXECUTABLE})
endif()

# 查找必要的包
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(Qt5 COMPONENTS Widgets REQUIRED HINTS /opt/homebrew/opt/qt@5)

# 包含目录
set(SOURCES
    src/main.cpp
    src/python_interface/python_interface.cpp
    src/gui/gui_module.cpp 
    src/config_loader.cpp
)

# 添加头文件
set(HEADERS
    include/data_structures.h
    include/config.h
    src/python_interface/python_interface.h
    src/gui/gui_module.h
    src/config_loader.h
)

# 创建可执行文件
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# 设置 include 目录
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
    ${Python3_INCLUDE_DIRS}
)
# 查找Python库
find_library(PYTHON_LIBRARIES NAMES python3.11 PATHS ${CONDA_PREFIX}/lib)
# 链接库
target_link_libraries(${PROJECT_NAME} PRIVATE
    Qt5::Widgets
    ${Python3_LIBRARIES}
    pybind11::embed
    nlohmann_json::nlohmann_json
)

# 复制 Python 脚本到构建目录
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_SOURCE_DIR}/python_scripts $<TARGET_FILE_DIR:${PROJECT_NAME}>/python_scripts
)

# 复制配置文件到构建目录
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
    ${CMAKE_SOURCE_DIR}/resources/config.json $<TARGET_FILE_DIR:${PROJECT_NAME}>/config.json
)

# 设置输出目录
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

# 安装规则
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/python_scripts DESTINATION bin)
install(FILES ${CMAKE_SOURCE_DIR}/resources/config.json DESTINATION bin)

# 打印一些配置信息
message(STATUS "Python libraries: ${Python3_LIBRARIES}")
message(STATUS "Python include dirs: ${Python3_INCLUDE_DIRS}")
message(STATUS "pybind11 include dirs: ${pybind11_INCLUDE_DIRS}")
