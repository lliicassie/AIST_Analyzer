#include <pybind11/embed.h>
#include <Python.h>

namespace py = pybind11;

int main() {
    py::scoped_interpreter guard{}; // 启动解释器
    try {
        py::module::import("pandas");  // 尝试导入 pandas
        std::cout << "Pandas successfully imported!" << std::endl;
    } catch (const py::error_already_set &e) {
        std::cerr << "Error importing pandas: " << e.what() << std::endl;
    }
    return 0;
}
