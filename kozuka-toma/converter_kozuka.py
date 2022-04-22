from fmt1_to_vtk_legacy_converter import Fmt1ToVtkLegacyConverter
from fmt2_to_vtk_legacy_converter import Fmt2ToVtkLegacyConverter

file_name = input("Enter target file name in data directory (fmt1|fmt2): ")
Fmt1Converter = Fmt1ToVtkLegacyConverter()
Fmt2Converter = Fmt2ToVtkLegacyConverter()

if ".fmt1" in file_name:
    Fmt1Converter.Execute("./data/" + file_name, "./output/" + file_name + ".vtk")
elif ".fmt2" in file_name:
    Fmt2Converter.Execute("./data/" + file_name, "./output/" + file_name + ".vtk")
else:
    print("ERROR: allowed file type is only (.fmt1|.fmt2) ")
