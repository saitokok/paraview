from base_vtk_legacy_converter import BaseVtkLegacyConverter
#from stl_to_vtk_legacy_converter import STLToVtkLegacyConverter #STLToVtkLegacyConverter は vtkmodules.all モジュールが解決出来ないためパージする.
from fmt1_to_vtk_legacy_converter import Fmt1ToVtkLegacyConverter
from fmt2_to_vtk_legacy_converter import Fmt2ToVtkLegacyConverter

from enum import Enum


class InputExtType(Enum):
    STL = 1
    FMT1 = 2
    FMT2 = 3


def select_converter(input_ext_type):
    ret_converter = None
    if input_ext_type == InputExtType.STL:
        raise("unsupported converter type.")     #STLToVtkLegacyConverter は vtkmodules.all モジュールが解決出来ないためパージする.
    elif input_ext_type == InputExtType.FMT1:
        ret_converter = Fmt1ToVtkLegacyConverter()
    elif input_ext_type == InputExtType.FMT2:
        ret_converter = Fmt2ToVtkLegacyConverter()
    else:
        raise("unsupported converter type.")
    return ret_converter


if __name__ == "__main__":
    in_path = "./data/Stanford_Bunny.fmt1"
    out_path = "./data/Stanford_Bunny_fmt1.vtk"
    #in_path = "./data/teapot.fmt1"
    #out_path = "./data/teapot_fmt1.vtk"
    input_ext_type = InputExtType.FMT1

    converter = select_converter(input_ext_type)
    converter.Execute(in_file_name=in_path, out_file_name=out_path)
