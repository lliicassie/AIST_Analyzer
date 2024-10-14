#include "config_loader.h"
#include <fstream>

nlohmann::json load_config() {
    std::ifstream config_file("../resources/config.json");
    if (!config_file.is_open()) {
        throw std::runtime_error("Failed to open config.json");
    }
    return nlohmann::json::parse(config_file);
}