#pragma once

#include <QMainWindow>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QLabel>
#include <QTableWidget>
#include <QImage>
#include "../python_interface/python_interface.h"

class GUIModule : public QMainWindow {
    Q_OBJECT

public:
    explicit GUIModule(PythonInterface& pyInterface);
    virtual ~GUIModule() = default;  // 虚析构函数

    // 禁用拷贝构造和赋值操作符
    GUIModule(const GUIModule&) = delete;
    GUIModule& operator=(const GUIModule&) = delete;

private slots:
    void onAnalyzeButtonClicked();

private:
    PythonInterface& pythonInterface;
    QPushButton* analyzeButton;
    QLineEdit* urlInput;
    QLabel* resultLabel;
    QTableWidget* statsTable;
    QLabel* histogramLabel;

    void setupUI();
    void displayResults(const py::dict& results);
    
    // 添加这三个方法的声明
    void displayStatistics(const py::dict& stats);
    void displayFilePaths(const py::dict& file_paths);
    void displayHistogram(const QString& histogramPath);
};
