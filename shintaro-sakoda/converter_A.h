#ifndef CONVERTER_A_H
#define CONVERTER_A_H

#include "base_converter.h"

class ConverterA : public BaseConverter {
 public:
 private:
  void ReadFile(const std::string& out_file_name) override;
};

#endif