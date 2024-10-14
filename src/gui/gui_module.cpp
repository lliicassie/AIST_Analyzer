#include "gui_module.h"
#include <QVBoxLayout>
#include <QMessageBox>
#include "config_loader.h"




GUIModule::GUIModule(PythonInterface& pyInterface)
    : pythonInterface(pyInterface)
{
    setupUI();
}

void GUIModule::setupUI() {
    QWidget* centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    QVBoxLayout* layout = new QVBoxLayout(centralWidget);

    urlInput = new QLineEdit(this);
    layout->addWidget(urlInput);

    analyzeButton = new QPushButton("Analyze", this);
    layout->addWidget(analyzeButton);

    resultLabel = new QLabel(this);
    layout->addWidget(resultLabel);

    statsTable = new QTableWidget(this);
    layout->addWidget(statsTable);

    histogramLabel = new QLabel(this);
    layout->addWidget(histogramLabel);

    connect(analyzeButton, &QPushButton::clicked, this, &GUIModule::onAnalyzeButtonClicked);
}


void GUIModule::onAnalyzeButtonClicked() {
    QString url = urlInput->text();
    if (url.isEmpty()) {
        QMessageBox::warning(this, "Error", "Please enter a valid URL");
        return;
    }

    try {
        py::dict results = pythonInterface.processData(url.toStdString());
        displayResults(results);
    } catch (const std::exception& e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void GUIModule::displayResults(const py::dict& results) {
    try {
        // 显示统计信息
        py::dict stats = results["statistics"].cast<py::dict>();
        displayStatistics(stats);

        // 显示文件路径
        py::dict file_paths = results["file_paths"].cast<py::dict>();
        displayFilePaths(file_paths);

        // 加载并显示直方图
        std::string histogramPath = file_paths["histogram"].cast<std::string>();
        displayHistogram(QString::fromStdString(histogramPath));

    } catch (const std::exception& e) {
        QMessageBox::critical(this, "Error", QString("Failed to display results: %1").arg(e.what()));
    }
}

void GUIModule::displayStatistics(const py::dict& stats) {
    statsTable->setRowCount(static_cast<int>(stats.size()));
    statsTable->setColumnCount(2);
    statsTable->setHorizontalHeaderLabels({"Statistic", "Value"});

    int row = 0;
    for (const auto& item : stats) {
        QString key = QString::fromStdString(py::str(item.first));
        QString value = QString::fromStdString(py::str(item.second));
        statsTable->setItem(row, 0, new QTableWidgetItem(key));
        statsTable->setItem(row, 1, new QTableWidgetItem(value));
        row++;
    }

    statsTable->resizeColumnsToContents();
}

void GUIModule::displayFilePaths(const py::dict& file_paths) {
    QString pathsText;
    for (const auto& item : file_paths) {
        QString key = QString::fromStdString(py::str(item.first));
        QString value = QString::fromStdString(py::str(item.second));
        pathsText += QString("%1: %2\n").arg(key).arg(value);
    }
    resultLabel->setText(pathsText);
}

void GUIModule::displayHistogram(const QString& histogramPath) {
    QImage histImage;
    if (histImage.load(histogramPath)) {
        histogramLabel->setPixmap(QPixmap::fromImage(histImage));
    } else {
        QMessageBox::warning(this, "Error", "Failed to load histogram image from file");
    }
}