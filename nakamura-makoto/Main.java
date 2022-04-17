package vtkConverter;
import java.io.IOException;
import java.nio.file.Path;

public class Main{

    /**
     * @param args 実行時引数
     * args[0]:使用するコンバーターのID
     * args[1]:フォーマット変換するファイルのパス
     * args[2]:出力するパス
     * @throws IOException
     */
    public static void main(String[] args)throws IOException{

    	BaseVtkLegacyConverter converter = switch(Integer.valueOf(0)){
            case 0 -> new HogeToVtkLegacyConverter();
            case 1 -> new PiyoToVtkLegacyConverter();
            default-> null;
        };

        Path inputPath = Path.of("C:\\Users\\enjoy\\git\\VtkConverter\\data\\fmt1\\teapot.fmt1");
        Path outputPath = Path.of("C:\\Users\\enjoy\\git\\VtkConverter\\data\\fmt1\\output.vtk");

        converter.execute(inputPath,outputPath);
    }
}
