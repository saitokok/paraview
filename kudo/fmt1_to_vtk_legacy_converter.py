from base_vtk_legacy_converter import BaseVtkLegacyConverter


class Fmt1ToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):
        """Need override."""
        with open(in_file_name, "r") as file_obj:
            data_mode = ""
            find_partition_mode = False
            partition = "---\n"
            for line in file_obj.readlines():
                splited_line = line.split(",")

                if line == "\n":
                    continue

                if find_partition_mode:
                    if line == partition:
                        find_partition_mode = False
                        continue
                    continue
                if "[points]" in line:
                    data_mode = "points"
                    find_partition_mode = True
                    print('data_mode:', data_mode)
                    continue
                if "[cells]" in line:
                    data_mode = "cells"
                    find_partition_mode = True
                    print('data_mode:', data_mode)
                    continue

                if data_mode == "points":
                    self.object_3d.points.append([splited_line[1], splited_line[2], splited_line[3]])

                if data_mode == "cells":
                    self.object_3d.cell_types.append(splited_line[0])
                    self.object_3d.cells.append([splited_line[2], splited_line[3], splited_line[4]])


if __name__ == "__main__":
    in_bunny_obj_file = "Stanford_Bunny.fmt1"
    out_bunny_obj_file = "Stanford_Bunny1.vtk"
    in_teapot_obj_file = "teapot.fmt1"
    out_teapot_obj_file = "teapot1.vtk"

    converter = Fmt1ToVtkLegacyConverter()
    converter.Execute(in_bunny_obj_file, out_bunny_obj_file)
    converter = Fmt1ToVtkLegacyConverter()
    converter.Execute(in_teapot_obj_file, out_teapot_obj_file)
