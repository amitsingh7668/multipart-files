import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class TransformerFactory {
    private static final Map<String, Transformer<?>> transformerRegistry = new ConcurrentHashMap<>();

    static {
        // Register built-in transformers
        transformerRegistry.put("etd", new SampleDataModelTransformer());
        transformerRegistry.put("etc", new AnotherDataModelTransformer());
    }

    public static <T> Transformer<T> getTransformer(String key) {
        Transformer<?> transformer = transformerRegistry.get(key);
        if (transformer == null) {
            throw new IllegalArgumentException("No transformer found for key: " + key);
        }
        return (Transformer<T>) transformer;
    }

    public static void registerTransformer(String key, Transformer<?> transformer) {
        transformerRegistry.put(key, transformer);
    }
}
