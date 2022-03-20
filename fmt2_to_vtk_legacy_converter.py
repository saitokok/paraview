from base_vtk_legacy_converter import BaseVtkLegacyConverter

import math

class fmt2_to_vtk_legacy_converter(BaseVtkLegacyConverter):

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
            if(count == 5):
                self.celltypesIn(line)
            if("===\n" == line):
                count += 1

    def pointsIn(self, line):
        liney = line.split('(')
        linev = liney[1].split(',')
        linev[2] = linev[2][0:len(linev[2])-2]
        for i in range(len(linev)):
            linev[i] = round(float(linev[i]), 5)
        self.object_3d.points.append(linev)

    def cellsIn(self, line):
        liney = line.split('(')
        linev = liney[1].split(',')
        linev[2] = linev[2][0:len(linev[2])-2]
        self.object_3d.cells.append(linev)

    def celltypesIn(self, line):
        line = line[0:len(line)-1]
        self.object_3d.cell_types.append(line)

if __name__ == "__main__":
    in_obj_file = "C:\\Users\\xx03d\\Downloads\\data-20220318T064025Z-001\\data.fmt2"
    out_obj_file = "C:\\Users\\xx03d\\Downloads\\data-20220318T064025Z-001\\data2.vtk"

    converter = fmt2_to_vtk_legacy_converter()
    converter.Execute(in_obj_file, out_obj_file)
