#include <QApplication>
#include <QMessageBox>
#pragma push_macro("slots")
#undef slots
#include <pybind11/embed.h>
#pragma pop_macro("slots")
#include "gui/gui_module.h"
#include "python_interface/python_interface.h"
#include "config_loader.h"



int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // 使用空的 PythonInterface，因为我们只是测试 GUI，不需要实际调用 Python
    PythonInterface dummyPythonInterface(false);  // 禁用 Python 环境初始化

    GUIModule mainWindow(dummyPythonInterface);
    mainWindow.setWindowTitle("Test GUI");
    mainWindow.resize(800, 600);  // 设置窗口大小
    mainWindow.show();

    return app.exec();  // 进入 Qt 事件循环
}