from base_vtk_legacy_converter import BaseVtkLegacyConverter


class Fmt2ToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):
        """Need override."""

        data_mode: str = ""  # "points" or "cells" (or "cell_types")
        find_partition_mode: bool = False
        partition: str = "==="  # ヘッダ情報と本データの分け目

        with open(in_file_name, "r") as f:
            lines = f.readlines()

        for line in lines:
            line: str = line.strip()  # 末尾に改行が付いているので除去

            if line == "":
                continue

            # partitionが見つかるまでcontinue
            if find_partition_mode:
                if line == partition:
                    find_partition_mode = False
                continue

            if "[points]" in line:
                data_mode = "points"
                find_partition_mode = True
                # print('data_mode:', data_mode)
                continue
            if "[cells]" in line:
                data_mode = "cells"
                find_partition_mode = True
                # print('data_mode:', data_mode)
                continue
            if "[cell_types]" in line:
                data_mode = "cell_types"
                find_partition_mode = True
                # print('data_mode:', data_mode)
                continue

            # data_mode が決まり、find_partition_mode がFalseになったらデータ取得スタート
            # いったん全て入れる → idを基にsort → 必要部分切り出し▼▼▼▼▼▼
            if data_mode == "points":  # line構成 "point_id:(x,y,z)"
                self.object_3d.points.append(line.split(":"))

            if data_mode == "cells":  # line構成 "cell_id:(p_id0,p_id1,...)"
                self.object_3d.cells.append(line.split(":"))

            if data_mode == "cell_types":  # line構成 "cell_type"
                self.object_3d.cell_types.append(line)

        self.object_3d.points.sort(key=lambda x: int(x[0]))
        self.object_3d.points = [self._convert_str_to_list(li[1]) for li in self.object_3d.points]

        self.object_3d.cells.sort(key=lambda x: int(x[0]))
        self.object_3d.cells = [self._convert_str_to_list(li[1]) for li in self.object_3d.cells]
        # いったん全て入れる → idを基にsort → 必要部分切り出し▲▲▲▲▲▲▲▲

        # self.PrintListItems(self.object_3d.points)
        # self.PrintListItems(self.object_3d.cells)
        # self.PrintListItems(self.object_3d.cell_types)

    @staticmethod
    def _convert_str_to_list(s: str):
        """str型"(***,***,***)" をevalでタプルに変換 → リストに変換"""
        return list(eval(s))

    @staticmethod
    def PrintListItems(lst: list):
        """デバッグ用。リスト渡すと途中を省略して表示してくれるよ"""
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        for i, item in enumerate(lst):
            if i <= 10:
                print(item)
            if i == 11:
                print("...")
            if i >= len(lst) - 10:
                print(item)
        print("__________________________________________________")


if __name__ == "__main__":
    in_bunny_obj_file = "Stanford_Bunny.fmt2"
    out_bunny_obj_file = "Stanford_Bunny2.vtk"
    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_bunny_obj_file, out_bunny_obj_file)

    in_teapot_obj_file = "teapot.fmt2"
    out_teapot_obj_file = "teapot2.vtk"
    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_teapot_obj_file, out_teapot_obj_file)

    in_tetra_mesh = "Stanford_Bunny.fmt2.random"
    out_tetra_mesh = "Stanford_Bunny.fmt2.random.vtk"
    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_tetra_mesh, out_tetra_mesh)

    in_mixed_mesh1 = "mixed_mesh1.fmt2"
    out_mixed_mesh1 = "mixed_mesh1.fmt2.vtk"
    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_mixed_mesh1, out_mixed_mesh1)

    in_mixed_mesh2 = "mixed_mesh2.fmt2"
    out_mixed_mesh2 = "mixed_mesh2.fmt2.vtk"
    converter = Fmt2ToVtkLegacyConverter()
    converter.Execute(in_mixed_mesh2, out_mixed_mesh2)
