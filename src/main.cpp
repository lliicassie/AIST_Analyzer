#include <QApplication>
#include <QMessageBox>
#pragma push_macro("slots")
#undef slots
#include <pybind11/embed.h>
#pragma pop_macro("slots")
#include "gui/gui_module.h"
#include "python_interface/python_interface.h"
#include "config_loader.h"

namespace py = pybind11;

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    try {
        // 初始化Qt应用

        // 启动Python解释器，只需构造一次，不需要重新赋值
        py::scoped_interpreter guard{}; // 这里初始化解释器，注意 guard 不需要再赋值

        // 加载配置
        auto config = load_config();

        // 创建Python接口
        PythonInterface pyInterface(true);

        // 创建并显示主窗口
        GUIModule mainWindow(pyInterface);
        mainWindow.setWindowTitle(QString::fromStdString(config["gui"]["window_title"]));
        mainWindow.resize(
            config["gui"]["window_size"]["width"],
            config["gui"]["window_size"]["height"]
        );
        mainWindow.show();

        // 运行应用程序事件循环
        return app.exec();
    } catch (const std::exception& e) {
        QMessageBox::critical(nullptr, "Error", QString("An error occurred: %1").arg(e.what()));
        return 1;
    }
}
