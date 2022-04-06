from typing import Final, Iterable, Iterator, List

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
            self.object_3d.cell_types = [_type for _type, id, x, y, z in cells_body]
            self.object_3d.cells = [[x, y, z] for _type, id, x, y, z in cells_body]
        
        
    def Tokenize(self, data : List[str], marks : List[str], separators : List[List[str]]) -> List[List[str]]:
        blocks : List[List[List[str]]] = []         #複数の異なる2次元構造の list
        block :List[List[str]] = []                 #blocks を構成する二次元構造の1つ.

        _marks : Iterator[str] = marks.__iter__()           #行のデータ構造が変化する目印(Iterator化)
        _separators : Iterator[str] = separators.__iter__() #上記目標ごとに変化する構造の定義(Iterator化)

        current_mark : str = _marks.__next__()      #各ブロックを隔てる識別子. current_separators より1要素先に iter を進める. 先に終端に到達する
        current_separators : List[str] = None       #各ブロック内で繰り返される要素の分割文字. current_mark より1要素ずつ遅れて iter をすすめる.

        for line in data:                
            #現在行が最下端のブロックではない, かつ 現在行がブロックの切り替え行である
            if((not(current_mark is None)) and (current_mark in line)):
                #最上端の構造変化目印より上のデータは無視する.
                if(not(current_separators is None)):
                    #行毎に分割した構造の集合( block )を返り値 blocks に追加する
                    blocks.append(block.copy())
                    block.clear()
                current_mark = self.nextIfExists(_marks, None)
                current_separators = self.nextIfExists(_separators, None)
                if(current_separators is None):
                    break
            #現在行がブロックの途中であり, それは最初の識別子より後である
            elif(not(current_separators is None)):
                b = self.SeparateBlock(line, current_separators)
                #空白は無視する
                if(not line == ""):
                    block.append(self.SeparateBlock(line, current_separators))
        #最終ブロック分を追加
        blocks.append(block.copy())
        del block
        return blocks

    def SeparateBlock(self, data : str, separators : List[str]) -> List[str]:
        """

        Args:
            data (List[str]):    Non-tokenized data
            separators (List[str]): Marker for separator
                example: ["[points]", "---", "[cells]", "---"]

        Returns:
            List[str]: separated strings
        """
        result : List[str] = [] #返り値
        blocks : List[str] = [] # 1回分の分割結果.

        for separator in separators:
            blocks = data.split(sep=separator, maxsplit=1) #セパレータ文字の前後で分割(最も左側のセパレータで分割)
            result.append(blocks[0])                       #分割した文字列の左側を返り値リストに追加
            if(len(blocks) > 1):
                data = blocks[1]                           #セパレートに成功した場合(2つに分割できた場合), それを分割対象の文字列とする.
        result.append(data)
        return result


    def nextIfExists(self, iterable : Iterable, default : any) -> any:
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
    pass
