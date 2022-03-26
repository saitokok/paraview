from base_vtk_legacy_converter import BaseVtkLegacyConverter


class Fmt2ToVtkLegacyConverter(BaseVtkLegacyConverter):

    def ReadFile(self, in_file_name):

        with open(in_file_name, mode="r") as file_obj:

            point_flg = 1
            cells_flg = 0
            type_flg = 0
            skip_counter = 0

            while True:
                line = file_obj.readline()

                if not line:
                    break

                if line.find('cells') > 0:
                    cells_flg = 1
                    point_flg = 0
                    skip_counter = 0
                elif line.find('cell_types') > 0:
                    type_flg = 1
                    cells_flg = 0
                    skip_counter = 0

                if skip_counter != 3:
                    skip_counter += 1
                    continue

                if line.find(',') > 0:
                    line_splits = line.split('(')[1].replace(')', '')
                    line_splits_2 = line_splits.split(',')
                elif type_flg == 1:
                    line_type = line.replace('\n', '')
                    self.object_3d.cell_types.append(line_type)
                    continue
                else:
                    continue

                if point_flg == 1:
                    self.object_3d.points.append([line_splits_2[0], line_splits_2[1], line_splits_2[2]])
                elif cells_flg == 1:
                    self.object_3d.cells.append([line_splits_2[0], line_splits_2[1], line_splits_2[2]])

        pass


if __name__ == '__main__':
    Fmt2ToVtkLegacyConverter().Execute("../data/Stanford_Bunny.fmt2", "output2.vtk")
