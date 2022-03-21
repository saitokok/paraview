#include "base_converter.h"

#include <fstream>

std::vector<std::string> BaseConverter::split_naive(const std::string& s, char delim) {
  std::vector<std::string> elems;
  std::string item;
  for (char ch : s) {
    if (ch == delim) {
      if (!item.empty()) elems.push_back(item);
      item.clear();
    } else {
      item += ch;
    }
  }
  if (!item.empty()) elems.push_back(item);
  return elems;
}

void BaseConverter::Execute(const std::string& in_file_name, const std::string& out_file_name) {
  ReadFile(in_file_name);
  WriteFile(out_file_name);
}

void BaseConverter::WriteFile(const std::string& out_file_name) {
  std::ofstream ofs(out_file_name);
  // Write header
  ofs << "# vtk DataFile Version 4.2" << std::endl;
  ofs << "vtk output" << std::endl;
  ofs << "ASCII" << std::endl;
  ofs << "DATASET UNSTRUCTURED_GRID" << std::endl;

  // Write points section
  const uint32_t num_points = object_3d_.points.size();
  ofs << "POINTS " << num_points << " float" << std::endl;

  for (uint32_t i = 0; i < object_3d_.points.size(); i++) {
    const std::vector<float>& xyz = object_3d_.points[i];
    ofs << xyz[0] << " ";
    ofs << xyz[1] << " ";
    ofs << xyz[2] << " \n"[i % 3 == 2];
  }

  // ofs << std::endl;

  // Write cells section
  const uint32_t num_cells = object_3d_.cells.size();
  uint32_t num_cells_attibutes = 0;
  for (const std::vector<int32_t>& cell : object_3d_.cells) {
    num_cells_attibutes += cell.size();
  }
  num_cells_attibutes += num_cells;

  ofs << "CELLS " << num_cells << " " << num_cells_attibutes << std::endl;

  for (uint32_t i = 0; i < num_cells; i++) {
    const std::vector<int32_t> cell = object_3d_.cells[i];
    ofs << cell.size();
    for (int32_t point_id : cell) {
      ofs << " " << point_id;
    }
    ofs << std::endl;
  }

  // ofs << std::endl;

  ofs << "CELL_TYPES " << num_cells << std::endl;

  auto CellTypeFromStr2Vtk = [&](const std::string& cell_type_str) {
    if (cell_type_str == "tri") {
      return 5;
    } else if (cell_type_str == "tetra") {
      return 10;
    } else {
      return -1;
    }
  };

  for (uint32_t cell_id = 0; cell_id < num_cells; cell_id++) {
    const std::string& cell_type_str = object_3d_.cell_types[cell_id];
    const uint32_t cell_type = CellTypeFromStr2Vtk(cell_type_str);
    ofs << cell_type << std::endl;
  }
}