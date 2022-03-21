#ifndef CONVERTER_B_H
#define CONVERTER_B_H

#include "base_converter.h"

class ConverterB : public BaseConverter {
 public:
 private:
  void ReadFile(const std::string& out_file_name) override;
};

#endif