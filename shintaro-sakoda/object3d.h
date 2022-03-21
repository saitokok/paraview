#ifndef OBJECT_3D_H
#define OBJECT_3D_H

#include <string>
#include <vector>

struct Object3D {
  std::vector<std::vector<float>> points;
  std::vector<std::vector<int32_t>> cells;
  std::vector<std::string> cell_types;
};

#endif