from base_vtk_legacy_converter import BaseVtkLegacyConverter

import math

class fmt1_to_vtk_legacy_converter(BaseVtkLegacyConverter):

    def ReadFile(self, in_file_name):
        f = open(in_file_name, 'r')

        lines = f.readlines()

        count = 0

        for line in lines:
            if("\n" == line):
                count += 1
            if(count == 1):
                self.pointsIn(line)
            if(count == 3):
                self.cellsIn(line)
            if("---\n"  == line):
                count += 1

    def pointsIn(self, line):
        liney = line.split(',')
        liney.pop(0)
        for i in range(len(liney)):
            liney[i] = round(float(liney[i]), 5)
        self.object_3d.points.append(liney)

    def cellsIn(self, line):
        liney = line.split(',')
        self.object_3d.cell_types.append(liney.pop(0))
        liney.pop(0)
        liney[2] = liney[2][0:len(liney[2])-1]
        self.object_3d.cells.append(liney)

if __name__ == "__main__":
    in_obj_file = "C:\\Users\\xx03d\\Downloads\\data-20220318T064025Z-001\\data.fmt1"
    out_obj_file = "C:\\Users\\xx03d\\Downloads\\data-20220318T064025Z-001\\data.vtk"

    converter = fmt1_to_vtk_legacy_converter()
    converter.Execute(in_obj_file, out_obj_file)
