#ifndef PYTHON_INTERFACE_H
#define PYTHON_INTERFACE_H

#pragma once
#include <iostream>  
#include <string>
#pragma push_macro("slots")
#undef slots
#include <pybind11/pybind11.h>
#include <pybind11/eval.h>
#include <pybind11/stl.h>
#pragma pop_macro("slots")


namespace py = pybind11;

class PythonInterface {
public:
    // 构造函数：用于测试 GUI 时不加载 Python 环境
    PythonInterface() {
        // 空构造函数，跳过 Python 初始化
    }

    // 构造函数：用于实际运行时加载 Python 环境
    PythonInterface(bool initialize_python) {
    if (initialize_python) {
        try {
            // Initialize Python main module and set up the path
            py::module sys = py::module::import("sys");
            sys.attr("path").attr("append")("../python_scripts");

            // Import your module directly
            main_module = py::module::import("aist_processor");
        } catch (const py::error_already_set& e) {
            std::cerr << "Python error in constructor: " << e.what() << std::endl;
            throw std::runtime_error("Failed to initialize Python environment");
        }
    }
}

    ~PythonInterface() = default;  // 默认析构函数

    // 用于处理用户输入的数据
    py::dict processData(const std::string& video_url);

private:
    py::module main_module;  // Python 主模块
};

#endif // PYTHON_INTERFACE_H
