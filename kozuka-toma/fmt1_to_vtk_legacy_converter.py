from re import S
from base_vtk_legacy_converter import BaseVtkLegacyConverter


class Fmt1ToVtkLegacyConverter(BaseVtkLegacyConverter):
    def ReadFile(self, in_file_name):

        # ファイルを開く
        with open(in_file_name, mode="r") as file_obj:
            raw_data = file_obj.readlines()

        # 改行コードを削除
        processed_line_list = []  # リスト作っておくa

        for line in raw_data:
            lf_deleted_line = line.replace("\n", "")  # 改行コードを削除
            if lf_deleted_line != "":
                processed_line_list.append(lf_deleted_line)  # 空行は無視

        # 以下データ処理
        cells_list_position = processed_line_list.index("[cells]")  # [cells]の行番号

        points_list = processed_line_list[
            0 : cells_list_position - 1
        ]  # [points]から[cells]までの行を取得
        del points_list[0:3]  # ヘッダーとなる先頭3行を削除

        cells_list = processed_line_list[cells_list_position:-1]  # [cells]以降の行を取得
        del cells_list[0:3]  # ヘッダーとなる先頭3行を削除

        # [points]の各行を処理
        for point in points_list:
            tmp = point.split(",")
            self.object_3d.points.append([tmp[1], tmp[2], tmp[3]])  # x,y,zの書式で書き込み

        # [cells_list]の各行を処理
        for cell in cells_list:
            tmp = cell.split(",")
            self.object_3d.cells.append([tmp[2], tmp[3], tmp[4]])  # pointIDのリストを書き込み
            self.object_3d.cell_types.append(tmp[0])  # cellTypeを書き込み

    # デバッグ用。リスト渡すと途中を省略して表示してくれるよ
    def PrintListItems(self, list):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        for i, item in enumerate(list):
            if i <= 10:
                print(item)
            if i == 11:
                print("...")
            if i >= len(list) - 10:
                print(item)
        print("__________________________________________________")
