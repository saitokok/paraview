package vtkConverter;

import java.util.function.Predicate;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class FromToPredicate<T> implements Predicate<T> {
    boolean started = false;
    Predicate<T> fromTest;
    Predicate<T> toTest;

    public static <T> Predicate<T> fromTo(Predicate<T> fromTest,Predicate<T> toTest) {
    	return new FromToPredicate<>(false, fromTest, toTest);
    }

    public boolean test(T t) {
    	if (toTest.test(t)) {
    		started = false;
    	}
        return started || (started = fromTest.test(t));
    }

}
