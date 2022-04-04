from base_vtk_legacy_converter import BaseVtkLegacyConverter
from data_replace import obj_replace, cell_types_obj_replace


class FugaToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):
        """Need override."""
        with open('C:\\Users\\81805\\data\\teapot.fmt2', mode="r") as obj:
            obj_list = obj.readlines()
            start_point = 3
            end_point = 1
            cells_slice = obj_list.index('[cells]\n')
            cell_types_slice = obj_list.index('[cell_types]\n')
            
            point_obj_list = obj_list[start_point : cells_slice - end_point]
            cells_obj_list = obj_list[cells_slice + start_point : cell_types_slice - end_point]
            cell_types_obj_list = obj_list[cell_types_slice + start_point :]
            

            self.object_3d.points = obj_replace(point_obj_list)
            self.object_3d.cells = obj_replace(cells_obj_list)
            self.object_3d.cell_types = cell_types_obj_replace(cell_types_obj_list)



if __name__ == "__main__":
    # in_bunny_obj_file = "/home/ksato/ExternalSSD1T/dataset/vtk/Stanford_Bunny.stl"
    # out_bunny_obj_file = "/home/ksato/ExternalSSD1T/dataset/vtk/stl_to_vtk_legacy.vtk"
    in_obj_file = 'C:\\Users\\81805\\data\\teapot.fmt2'
    out_obj_file = 'C:\\Users\\81805\\data\\teapot.vtk'

    converter = FugaToVtkLegacyConverter()
    converter.Execute(in_obj_file, out_obj_file)