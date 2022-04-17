package vtkConverter;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Supplier;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Object3D implements Supplier<Object3D> {
	// key:pointId, value:[x,y,z]
	private Map<Integer, double[]> points;
	// key:cellId, value:[p_id_00, p_id_01, p_id_02,...]
	private Map<Integer, int[]> cells;
	// key:cellId, value:shape
	private Map<Integer, String> cellTypes;

	Object3D(){
		this(new HashMap<>(),new HashMap<>(),new HashMap<>());
	}

	@Override
	public Object3D get() {
		return this;
	}
}