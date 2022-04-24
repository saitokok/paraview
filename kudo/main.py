# from base_vtk_legacy_converter import BaseVtkLegacyConverter
# from fmt1_to_vtk_legacy_converter import Fmt1ToVtkLegacyConverter
# from fmt2_to_vtk_legacy_converter import Fmt2ToVtkLegacyConverter
# # from stl_to_vtk_legacy_converter import STLToVtkLegacyConverter

# from enum import Enum


# class InputExtType(Enum):
#     STL = 1
#     FMT1 = 2
#     FMT2 = 3


# def select_converter(input_ext_type):
#     ret_converter = None
#     # if input_ext_type == InputExtType.STL:
#     #     ret_converter = STLToVtkLegacyConverter()
#     if input_ext_type == InputExtType.FMT1:
#         ret_converter = Fmt1ToVtkLegacyConverter()
#     elif input_ext_type == InputExtType.FMT2:
#         ret_converter = Fmt2ToVtkLegacyConverter()

#     return ret_converter


# if __name__ == "__main__":
#     in_bunny_obj_file = "Stanford_Bunny.fmt1"
#     out_bunny_obj_file = "Stanford_Bunny1.vtk"
#     in_teapot_obj_file = "teapot.fmt1"
#     out_teapot_obj_file = "teapot1.vtk"
    
#     # in_bunny_obj_file = "Stanford_Bunny.fmt2"
#     # out_bunny_obj_file = "Stanford_Bunny2.vtk"
#     # in_teapot_obj_file = "teapot.fmt2"
#     # out_teapot_obj_file = "teapot2.vtk"
    
#     # input_ext_type = InputExtType.FMT2
    
#     import os
#     if os.path.splitext(in_bunny_obj_file)[1] == '.fmt1':
#         print('Process for fmt1')
#         input_ext_type = InputExtType.FMT1
#     elif os.path.splitext(in_bunny_obj_file)[1] == '.fmt2':
#         print('Process for fmt2')
#         input_ext_type = InputExtType.FMT2
#     else:
#         input_ext_type = None
#         raise Exception()

#     converter = select_converter(input_ext_type)
#     converter.Execute(in_bunny_obj_file, out_bunny_obj_file)
#     converter = select_converter(input_ext_type)
#     converter.Execute(in_teapot_obj_file, out_teapot_obj_file)
