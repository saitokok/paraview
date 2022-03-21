#include <iostream>

#include "converter_A.h"
#include "converter_B.h"

int main() {
  ConverterA converter_a;
  ConverterB converter_b;

  for (const std::string file : {"Stanford_Bunny", "teapot"}) {
    std::cout << file << std::endl;
    std::cout << "start convert fmt1" << std::endl;
    converter_a.Execute("../data/" + file + ".fmt1", "../data/" + file + "_from_A.vtk");
    std::cout << "start convert fmt2" << std::endl;
    converter_b.Execute("../data/" + file + ".fmt2", "../data/" + file + "_from_B.vtk");
  }
}