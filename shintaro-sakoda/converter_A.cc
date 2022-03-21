#include "converter_A.h"

#include <cassert>
#include <fstream>
#include <iostream>

enum ReadMode {
  kInit,
  kReadPoint,
  kReadCell,
};

void ConverterA::ReadFile(const std::string& in_file_name) {
  std::ifstream ifs(in_file_name);
  std::cout << in_file_name << std::endl;
  std::string line;

  ReadMode mode = kInit;

  while (getline(ifs, line)) {
    if (line == "[points]") {
      assert(mode == kInit);
      mode = kReadPoint;
    } else if (line == "[cells]") {
      assert(mode == kReadPoint);
      mode = kReadCell;
    } else if (line == "point_id,x,y,z") {
      assert(mode == kReadPoint);
    } else if (line == "type,cell_id,point_id0,point_id1,...") {
      assert(mode == kReadCell);
    } else if (line == "---" || line.empty()) {
      // 読み飛ばす
      continue;
    } else {
      // 値本体
      if (mode == kReadPoint) {
        const std::vector<std::string> elements = split_naive(line, ',');
        const uint32_t id = std::stoi(elements[0]);
        const float x = std::stof(elements[1]);
        const float y = std::stof(elements[2]);
        const float z = std::stof(elements[3]);
        object_3d_.points.push_back({x, y, z});
      } else if (mode == kReadCell) {
        const std::vector<std::string> elements = split_naive(line, ',');
        const std::string type = elements[0];
        const uint32_t id = stoi(elements[1]);
        object_3d_.cell_types.push_back(type);
        object_3d_.cells.push_back(std::vector<int32_t>());
        for (int i = 2; i < elements.size(); i++) {
          object_3d_.cells.back().push_back(stoi(elements[i]));
        }
      } else {
        // ここに入るはずはない
        std::exit(1);
      }
    }
  }
}
