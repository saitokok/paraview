package vtkConverter;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collector;
import java.util.stream.Collector.Characteristics;

class HogeToVtkLegacyConverter extends BaseVtkLegacyConverter{


	@Override
	protected Object3D readFile(Path inputPath) throws IOException{
		if (!Files.exists(inputPath)) {
		 	throw new RuntimeException("ファイルが存在しません");
		}

		Object3D output3DObject = new Object3D();

		// read Points
		Files.lines(inputPath)
			.filter(FromToPredicate.fromTo("[points]"::equals, ""::equals))
			// skip header
			.skip(3)
			.collect(Collector.of(
				output3DObject,
				this::readPoints,
				(o1, o2) -> {
					o1.getPoints().putAll(o2.getPoints());
					return o1;
				},
				Characteristics.IDENTITY_FINISH)
			);

		// read Cells
 		Files.lines(inputPath)
			.filter(FromToPredicate.fromTo("[cells]"::equals, ""::equals))
			// skip header
			.skip(3)
			.collect(Collector.of(
				output3DObject,
				this::readCells,
				(o1, o2) -> {
					o1.getCells().putAll(o2.getCells());
					o1.getCellTypes().putAll(o2.getCellTypes());
					return o1;
				},
				Characteristics.IDENTITY_FINISH)
	 		);

 	 	return output3DObject;

 	}

	private void readPoints(Object3D output,String line) {
		 String[] splitLines = line.split(",");
 	 	 Integer pointId =  Integer.valueOf(splitLines[0]);
 	 	 double x = Double.valueOf(splitLines[1]);
 	 	 double y = Double.valueOf(splitLines[2]);
 	 	 double z = Double.valueOf(splitLines[3]);
 	 	 ((Object3D) output).getPoints().put(pointId, new double[]{x,y,z});
	}

	private void readCells(Object3D output,String line) {
		List<String> splitLines = Arrays.asList(line.split(","));
		String type = splitLines.get(0);

		int cellId = Integer.valueOf(splitLines.get(1));
		int[] pointIds = splitLines.stream().skip(2)
			.mapToInt(Integer::parseInt).toArray();
		output.getCells().put(cellId, pointIds);
		output.getCellTypes().put(cellId, type);
	}
}
