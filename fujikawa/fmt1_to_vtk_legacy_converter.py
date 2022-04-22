from base_vtk_legacy_converter import BaseVtkLegacyConverter


class Fmt1ToVtkLegacyConverter(BaseVtkLegacyConverter):

    def ReadFile(self, in_file_name):

        with open(in_file_name, mode="r") as file_obj:

            change_flg = 0
            skip_counter = 0

            while True:
                line = file_obj.readline()
                if not line:
                    break

                if line.find('cells') > 0:
                    change_flg = 1
                    skip_counter = 0

                if skip_counter != 3:
                    skip_counter += 1
                    continue

                if line.find(',') > 0:
                    line_splits = line.split(',')
                else:
                    continue

                if change_flg == 0:
                    self.object_3d.points.append([line_splits[1], line_splits[2], line_splits[3]])
                else:
                    self.object_3d.cells.append([line_splits[2], line_splits[3], line_splits[4]])
                    self.object_3d.cell_types.append(line_splits[0])

        pass


if __name__ == '__main__':
    Fmt1ToVtkLegacyConverter().Execute("../data/teapot.fmt1", "output.vtk")
