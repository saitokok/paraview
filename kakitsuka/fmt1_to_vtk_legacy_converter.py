from typing import Final, Iterable, List

from base_vtk_legacy_converter import BaseVtkLegacyConverter

class Fmt1ToVtkLegacyConverter(BaseVtkLegacyConverter):
    SEPARATOR_MARK : Final[List[str]] = ["[points]", "---", "[cells]", "---"] #1行あたりの記述構造が変化する目印

    SEPARATOR_POINTS_HEADER : Final[List[str]] = [",", ",", ","]              # "[points]"以降の構造
    SEPARATOR_POINTS_BODY   : Final[List[str]] = [",", ",", ","]              # "---"     以降の構造
    SEPARATOR_CELLS_HEADER  : Final[List[str]] = [",", ",", ",", ","]         # "[cells]" 以降の構造
    SEPARATOR_CELLS_BODY    : Final[List[str]] = [",", ",", ",", ","]         # "---"     以降の構造

    SEPARATORS : Final[List[List[str]]] = [SEPARATOR_POINTS_HEADER, SEPARATOR_POINTS_BODY, SEPARATOR_CELLS_HEADER, SEPARATOR_CELLS_BODY] # SEPARATOR_ROOT の各目印以降の構造リスト

    def ReadFile(self, in_file_name):
        with open(in_file_name, "r") as f:
            points_header, points_body, cells_header, cells_body = self.Tokenize(f.read().splitlines(), self.SEPARATOR_MARK, self.SEPARATORS)

            #points_header, cells_header は今回使用しない. 明示的に削除する
            del points_header
            del cells_header

            #頂点情報を保持する. points_body には添字情報が含まれるため除去する
            self.object_3d.points = [[x, y, z] for id, x, y, z in points_body]
            self.object_3d.cell_types = [_type for _type, id, point_id_1, point_id_2,point_id_3 in cells_body]
            self.object_3d.cells = [[point_id_1, point_id_2, point_id_3] for _type, cell_id, point_id_1, point_id_2,point_id_3  in cells_body]

        
    def Tokenize(self, data : List[str], marks : List[str], separators : List[List[str]]) -> List[List[List[str]]]:
        """
        異なる構造の集合の集合 data を marks で分割して
        各分割ブロックを separators で更に分割して返します.
        marks[n] 直後から marks[n+1] 番目の直前までを separators[n] で分割します.

        example:
            data : [
                "mark_1", "aXb", "cXd",
                "mark_2", "1P2Q3", "4P5Q6", "7P8Q9"
            ]
            marks : ["marks_1", "mark_2"]
            separators : [
                ["X"], 
                ["P", "Q"]
            ]

            --> return [
                [["a", "b"], ["c", "d"]],
                [["1", "2", "3"], ["4", "5", "6"],["7", "8", "9"]]
            ]


        Args:
            data (List[str]): 異なる構造の集合の集合
            marks (List[str]): 異なる構造を隔てるマーカー
            separators (List[List[str]]): 各構造毎の分割文字列

        Returns:
            List[List[List[str]]]: 複数の異なる2次元構造の集合の集合
        """
        blocks : List[List[List[str]]] = []         #複数の2次元配列構造の集合の集合. 
                                                    # List[str] が 単一行を指す
                                                    # List[List[str]] が同じ構造の行集合
                                                    # List[List[List[str]]] が異なる構造の行集合の集合
        block  : List[List[str]] = []               #blocks における List[List[str]]部分

        lines_iter = data.__iter__()                #各行を返す Iterator
        marks_iter = marks.__iter__()               #構造変化の目印を返す Iterator
        separators_iter = separators.__iter__()     #各構造ごとの区切り文字を返す Iterator

        #mark, separator は一つずつズレて iter を進める(markが先行)
        mark = self.NextIfExists(marks_iter, None)
        separator = None

        while True:
            line = self.NextIfExists(lines_iter, None)
            if line == mark: 
                #構造変化マーカーを検知した
                mark = self.NextIfExists(marks_iter, None)
                separator = self.NextIfExists(separators_iter, None)
                blocks.append(block.copy())
                block.clear()
                #これ以上下行に構造の指定が無い
                if separator is None:
                    break
            elif line is None: 
                #すべての行を読み終えた
                blocks.append(block)
                break       
            elif line == "":
                #該当行が空行である
                continue
            else:
                #いずれかの構造の行である
                block.append(self.SeparateLine(line, separator))
        # blocks 先頭要素は先頭の構造変化マーカーより上行のものなので捨てる
        return blocks[1:]

    def SeparateLine(self, line : str, separators : List[str]) -> List[str]:
        """
        Separate a line by separators
        Args:
            line (str):    Non-tokenized data ( 1 line str data)
            separators (List[str]): Marker for separator
        Returns:
            List[str]: separated strings
        """
        result : List[str] = [] #返り値
        blocks : List[str] = [] # 1回分の分割結果.

        for separator in separators:
            blocks = line.split(sep=separator, maxsplit=1) #セパレータ文字の前後で分割(最も左側のセパレータで分割)
            result.append(blocks[0])                       #分割した文字列の左側を返り値リストに追加
            if(len(blocks) > 1):
                line = blocks[1]                           #セパレートに成功した場合(2つに分割できた場合), それを分割対象の文字列とする.
        result.append(line)
        return result


    def NextIfExists(self, iterable : Iterable, default : any) -> any:
        """
        return next value if exist.
        otherwise return default.
        Args:
            iterable (Iterable): Iterable Object
            default (any): return value if Iterable has not __next__() object

        Returns:
            any: some object
        """
        try:
            return iterable.__next__()
        except StopIteration as e:
            return default

if(__name__=="__main__"):
    ins = Fmt1ToVtkLegacyConverter()
    