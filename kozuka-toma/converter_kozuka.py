from fmt1_to_vtk_legacy_converter import Fmt1ToVtkLegacyConverter

file_name = input("input file name without expand: ")
Fmt1Converter = Fmt1ToVtkLegacyConverter()
Fmt1Converter.Execute('./data/'+file_name+'.fmt1','./output/'+file_name+'.vtk')