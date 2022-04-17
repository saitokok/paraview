package vtkConverter;

import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.DoubleStream;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public abstract class BaseVtkLegacyConverter{
    public void execute(Path inputPath,Path outputPath) throws IOException {

    	Object3D output3DObject = this.readFile(inputPath);
    	this.writeFile(output3DObject, outputPath);
    }

    abstract protected Object3D readFile(Path inputPath) throws IOException;

    private void writeFile(Object3D output3DObject, Path outputPath) throws IOException {
        if (!Files.exists(outputPath)) {
            Files.createFile(outputPath);
        }
        //write header
        List<String> header = Arrays.asList(
        		"# vtk DataFile Version 4.2",
        		"vtk output",
        		"ASCII",
        		"DATASET UNSTRUCTURED_GRID");

        //write points section
        List<String> pointsSection = new ArrayList<>();

        int numPoints = output3DObject.getPoints().size();
        pointsSection.add("POINTS " + String.valueOf(numPoints) + " float");

        for(int i = 0; i < numPoints; i += 3) {
            double[] xyz = output3DObject.getPoints().get(i);
            double[] xyz2 = output3DObject.getPoints().get(i + 1);
            double[] xyz3 = output3DObject.getPoints().get(i + 2);
            String xyzStr = Stream.of(xyz,xyz2,xyz3).flatMapToDouble(e-> Optional.ofNullable(e)
          		  .map(DoubleStream::of).orElse(DoubleStream.empty())
          		  ).boxed()
          		.map(e->{
          			BigDecimal bd = new BigDecimal(String.valueOf(e));
          			int scale = 6 - (bd.precision() - bd.scale());
          			bd = bd.setScale(scale, RoundingMode.HALF_UP);
          			return bd.toPlainString();
          		}).collect(Collectors.joining(" "));

          pointsSection.add(xyzStr + " ");
        }

        // write cells section
        List<String> cellsSection = new ArrayList<>();

        int numCells = output3DObject.getCells().size();
        long numCellsAttributes = output3DObject.getCells().values().stream()
        		.flatMapToInt(e-> Optional.ofNullable(e)
            		  .map(IntStream::of).orElse(IntStream.empty())
            		  ).boxed().count();
        numCellsAttributes += numCells;
        System.out.println(numCellsAttributes);
        cellsSection.add("CELLS " + String.valueOf(numCells)
        		+ " " + String.valueOf(numCellsAttributes) + " ");

        for(int i = 0;i < numCells;i++) {
        	int[] cell = output3DObject.getCells().get(i);
        	String cellStr = IntStream.of(cell).boxed().map(s->s.toString())
        			.collect(Collectors.joining(" "));

            String cellInfoStr = String.valueOf(cell.length) + " " + cellStr + " ";
            cellsSection.add(cellInfoStr);
        }
        cellsSection.add("");

        // write cellTypes section
        List<String> cellTypesSection = new ArrayList<>();
        cellTypesSection.add("CELL_TYPES " + String.valueOf(numCells));
        for(int i = 0;i < numCells; i++) {
        	String cellTypeStr = output3DObject.getCellTypes().get(i);
        	int cellType = this.cellTypeFromStr2Vtk(cellTypeStr);
        	cellTypesSection.add(String.valueOf(cellType));
        }

        cellTypesSection.add("");

        List<String> allSection = new ArrayList<>() {
        	{
        		addAll(header);
        		addAll(pointsSection);
        		addAll(cellsSection);
        		addAll(cellTypesSection);
        	}
        };
        Files.write(outputPath, allSection, Charset.forName("UTF-8"), StandardOpenOption.WRITE);
    }

    private int cellTypeFromStr2Vtk(String cellTypeStr) {
        int retCellType = -1;

        if (cellTypeStr.equals("tri")) {
        	retCellType = 5;
        }else if(cellTypeStr.equals("tetra")) {
        	retCellType = 10;
        }
        return retCellType;
    }
}