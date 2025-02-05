private SingleOutputStreamOperator<EnrichableItemForAttention> enrichWithCustomTransformation(
        SingleOutputStreamOperator<EnrichableItemForAttention> enrichItemForAttentionStream) {

    // Check if the feature toggle for custom transformation is enabled
    if (config.getFeatureToggle().isCustomTransformationEnabled()) {

        // Create the AsyncLookupFunction with your custom transformation
        AsyncLookupFunction<EnrichableItemForAttention, String, EnrichableItemForAttention> customTransformationFunction =
                createCustomTransformationFunction();

        // Apply async transformation using AsyncDataStream.orderedWait
        return AsyncDataStream
                .orderedWait(
                        enrichItemForAttentionStream,               // Input stream
                        customTransformationFunction,                // The custom async function to transform items
                        5000L,                                      // Timeout of 5000 milliseconds
                        TimeUnit.MILLISECONDS,                      // Time unit for the timeout
                        100,                                        // Capacity of 100 items
                        "async-custom-transformation",              // Unique ID for incoming stream
                        "Log-async-custom-transformation"           // Unique ID for outgoing stream
                );
    }

    // If the custom transformation feature is disabled, return the original stream
    return enrichItemForAttentionStream;
}

// Helper function to create the AsyncLookupFunction for custom transformation
private AsyncLookupFunction<EnrichableItemForAttention, String, EnrichableItemForAttention> createCustomTransformationFunction() {
    // Create the AsyncLookup for custom transformation logic (no cache involved)
    AsyncLookup<String, EnrichableItemForAttention> asyncItemLookup =
            new AsyncItemTransformationLookup(
                    new CustomItemTransformationFunction()  // Your custom transformation logic
            );

    // Setup the AsyncLookupSupport (no cache here, as no caching is required)
    AsyncLookupSupport<EnrichableItemForAttention, String, EnrichableItemForAttention> asyncItemLookupSupport =
            new AsyncItemLookupSupport<>();

    // Return the AsyncLookupFunction for custom transformation
    return new AsyncLookupFunction<>(
            asyncItemLookup,
            asyncItemLookupSupport
    );
}

// Example of an Async Item Transformation Lookup class
class AsyncItemTransformationLookup implements AsyncLookup<String, EnrichableItemForAttention> {

    private final CustomItemTransformationFunction transformationFunction;

    public AsyncItemTransformationLookup(CustomItemTransformationFunction transformationFunction) {
        this.transformationFunction = transformationFunction;
    }

    @Override
    public CompletableFuture<EnrichableItemForAttention> lookup(String key) {
        // Apply the custom transformation asynchronously (e.g., updating some fields of EnrichableItemForAttention)
        return CompletableFuture.supplyAsync(() -> transformationFunction.apply(key));
    }
}

// Custom transformation function for enriching items
class CustomItemTransformationFunction implements Function<String, EnrichableItemForAttention> {

    @Override
    public EnrichableItemForAttention apply(String key) {
        // Logic to transform the EnrichableItemForAttention based on the input key
        EnrichableItemForAttention item = new EnrichableItemForAttention();
        item.setUsername(key + "_transformed");  // Example of custom transformation logic
        item.setStatus(200);  // Example of setting a new status

        // You can perform any custom transformation you need here
        return item;
    }
}
