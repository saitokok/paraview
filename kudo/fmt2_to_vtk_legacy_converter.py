from base_vtk_legacy_converter import BaseVtkLegacyConverter


class Fmt2ToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):
        """Need override."""
        def split_line(line):
            return line.split(":")[1].replace('(', '').replace(')', '').split(',')

        with open(in_file_name, "r") as file_obj:
            data_mode = ""
            find_partition_mode = False
            partition = "===\n"
            for line in file_obj.readlines():
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
                if "[cell_types]" in line:
                    data_mode = "cell_types"
                    find_partition_mode = True
                    print('data_mode:', data_mode)
                    continue

                if data_mode == "points":
                    splited_line = split_line(line)
                    self.object_3d.points.append([splited_line[0], splited_line[1], splited_line[2]])

                if data_mode == "cells":
                    splited_line = split_line(line)
                    self.object_3d.cells.append([splited_line[0], splited_line[1], splited_line[2]])

                if data_mode == "cell_types":
                    self.object_3d.cell_types.append(line.replace('\n', ''))


if __name__ == "__main__":
    in_bunny_obj_file = "Stanford_Bunny.fmt2"
    out_bunny_obj_file = "Stanford_Bunny2.vtk"
    in_teapot_obj_file = "teapot.fmt2"
    out_teapot_obj_file = "teapot2.vtk"

    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_bunny_obj_file, out_bunny_obj_file)
    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_teapot_obj_file, out_teapot_obj_file)
