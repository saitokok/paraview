#include "converter_B.h"

#include <cassert>
#include <fstream>
#include <iostream>

enum ReadMode {
  kInit,
  kReadPoint,
  kReadCell,
  kReadCellType,
};

void ConverterB::ReadFile(const std::string& in_file_name) {
  std::ifstream ifs(in_file_name);
  std::string line;

  ReadMode mode = kInit;

  while (getline(ifs, line)) {
    if (line == "[points]") {
      assert(mode == kInit);
      mode = kReadPoint;
    } else if (line == "[cells]") {
      assert(mode == kReadPoint);
      mode = kReadCell;
    } else if (line == "[cell_types]") {
      assert(mode == kReadCell);
      mode = kReadCellType;
    } else if (line == "point_id:(x,y,z)") {
      assert(mode == kReadPoint);
    } else if (line == "cell_id:(point_id0,point_id1,...)") {
      assert(mode == kReadCell);
    } else if (line == "cell_type") {
      assert(mode == kReadCellType);
    } else if (line == "===" || line.empty()) {
      // 読み飛ばす
      continue;
    } else {
      // 値本体
      if (mode == kReadPoint) {
        const std::vector<std::string> elements = split_naive(line, ':');
        const uint32_t id = std::stoi(elements[0]);
        std::string values = elements[1].substr(1);
        values.pop_back();
        const std::vector<std::string> v = split_naive(values, ',');
        const float x = std::stof(v[0]);
        const float y = std::stof(v[1]);
        const float z = std::stof(v[2]);
        object_3d_.points.push_back({x, y, z});
      } else if (mode == kReadCell) {
        const std::vector<std::string> elements = split_naive(line, ':');
        const uint32_t id = std::stoi(elements[0]);
        std::string values = elements[1].substr(1);
        values.pop_back();
        const std::vector<std::string> v = split_naive(values, ',');
        object_3d_.cells.push_back(std::vector<int32_t>());
        for (int i = 0; i < v.size(); i++) {
          object_3d_.cells.back().push_back(stoi(v[i]));
        }
      } else if (mode == kReadCellType) {
        object_3d_.cell_types.push_back(line);
      } else {
        // ここに入るはずはない
        std::exit(1);
      }
    }
  }
}
