from re import S
from base_vtk_legacy_converter import BaseVtkLegacyConverter

class Fmt1ToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):
        with open(in_file_name, mode="r") as file_obj:
            tmp = file_obj.readlines()
        line_str_list=[]
        for item in tmp:
            tmp2 = item.replace( '\n' , '' )
            if(tmp2!=""):
                line_str_list.append(tmp2)
        # self.PrintListItems(line_str_list)
        print(self.object_3d.points)

        cells_position = line_str_list.index("[cells]")
        points = line_str_list[0:cells_position-1]
        del points[0:3]
        cells = line_str_list[cells_position:-1]
        del cells[0:3]

        for i,point in enumerate(points):
            tmp = point.split(',')
            self.object_3d.points.append([tmp[1],tmp[2],tmp[3]])

        for i,cell in enumerate(cells):
            tmp = cell.split(',')
            self.object_3d.cells.append([tmp[2],tmp[3],tmp[4]])
            self.object_3d.cell_types.append(tmp[0])

        self.PrintListItems(self.object_3d.points)        
        self.PrintListItems(self.object_3d.cells)

    def PrintListItems(self, list):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        for item in list:
            print(item)
        print("__________________________________________________")