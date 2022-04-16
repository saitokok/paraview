from base_vtk_legacy_converter import BaseVtkLegacyConverter


class HogeToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):
        """Need override."""
        with open(in_file_name) as f:
            lines = f.read().splitlines()
        self.object_3d.points = self.create_points(lines)
        self.object_3d.cells = self.create_cells(lines)
        self.object_3d.cell_types = ["tri" for _ in self.object_3d.cells]

    def create_points(self, lines):
        return [self.convert_xyz(l) for l in lines[3:self.get_cells_index(lines) - 1]]

    def create_cells(self, lines):
        return [self.convert_cells(l) for l in lines[self.get_cells_index(lines) + 3:-1]]

    @staticmethod
    def convert_cells(l):
        _, _, p1, p2, p3 = l.split(",")
        return [p1, p2, p3]

    @staticmethod
    def convert_xyz(l):
        _, x, y, z = l.split(",")
        return [x, y, z]

    @staticmethod
    def get_cells_index(lines):
        for i, line in enumerate(lines):
            if line == "[cells]":
                return i
        return -1


if __name__ == '__main__':
    HogeToVtkLegacyConverter().Execute("teapot.fmt1", "output.vtk")
