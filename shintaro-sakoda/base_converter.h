#ifndef BASE_CONVERTER_H
#define BASE_CONVERTER_H

#include "object3d.h"

class BaseConverter {
 public:
  void Execute(const std::string& in_file_name, const std::string& out_file_name);

 protected:
  Object3D object_3d_;
  static std::vector<std::string> split_naive(const std::string& s, char delim);

 private:
  virtual void ReadFile(const std::string& in_file_name) = 0;
  void WriteFile(const std::string& out_file_name);
};

#endif