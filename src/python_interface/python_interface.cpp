#include "python_interface.h"
#include <iostream>
#include "config_loader.h"


py::dict PythonInterface::processData(const std::string& video_url) {
    try {
        // 加载 config.json
        auto config = load_config();
        std::string aist_motion_url = config["data"]["aist_motion_url"];  // 从配置文件中获取 aist_motion_url
        std::string output_path = config["data"]["output_path"];  // 从配置文件中获取输出路径

        // 创建 AISTDataProcessor 实例，并传递输出路径
        py::object AISTDataProcessor = main_module.attr("AISTDataProcessor");
        py::object processor = AISTDataProcessor(output_path);

        // 调用 process_data 方法，传递用户输入的视频 URL 和从配置中获取的 aist_motion_url
        py::object result = processor.attr("process_data")(video_url, aist_motion_url);

        // 检查返回的结果是否是一个字典
        if (!py::isinstance<py::dict>(result)) {
            throw std::runtime_error("Python function 'process_data' did not return a dictionary.");
        }

        // 返回结果
        return result.cast<py::dict>();
    } catch (const py::error_already_set& e) {
        std::cerr << "Python error in processData: " << e.what() << std::endl;
        throw std::runtime_error("Failed to process data from URL: " + video_url);
    } catch (const std::exception& e) {
        std::cerr << "Error in processData: " << e.what() << std::endl;
        throw;
    }
}
