import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class TransformerFactoryTest {

    @BeforeEach
    void setUp() {
        // Reset the factory before each test to ensure a clean state
        TransformerFactory.registerTransformer("etd", new SampleDataModelTransformer());
        TransformerFactory.registerTransformer("etc", new AnotherDataModelTransformer());
    }

    @Test
    void testRetrieveExistingTransformer() {
        Transformer<SampleDataModel> transformer = TransformerFactory.getTransformer("etd");
        assertNotNull(transformer, "Transformer for 'etd' should not be null");
    }

    @Test
    void testRetrieveNonExistentTransformer() {
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            TransformerFactory.getTransformer("nonexistent");
        });
        assertEquals("No transformer found for key: nonexistent", exception.getMessage());
    }

    @Test
    void testSampleDataModelTransformation() {
        Transformer<SampleDataModel> transformer = TransformerFactory.getTransformer("etd");
        SampleDataModel input = new SampleDataModel("John", "Doe", "john.doe@example.com");
        GenericIdentifier result = transformer.transform(input);

        assertNotNull(result);
        assertEquals(2, result.getData().length);
        assertEquals("John Doe", result.getData()[0].getValue());
        assertEquals("john.doe@example.com", result.getData()[1].getValue());
    }

    @Test
    void testAnotherDataModelTransformation() {
        Transformer<AnotherDataModel> transformer = TransformerFactory.getTransformer("etc");
        AnotherDataModel input = new AnotherDataModel("Alice", "Wonderland");
        GenericIdentifier result = transformer.transform(input);

        assertNotNull(result);
        assertEquals(2, result.getData().length);
        assertEquals("Alice", result.getData()[0].getValue());
        assertEquals("Wonderland", result.getData()[1].getValue());
    }

    @Test
    void testDynamicTransformerRegistration() {
        // Register a new transformer at runtime
        TransformerFactory.registerTransformer("custom", new CustomDataModelTransformer());

        Transformer<CustomDataModel> transformer = TransformerFactory.getTransformer("custom");
        assertNotNull(transformer, "Dynamically registered transformer should not be null");

        CustomDataModel input = new CustomDataModel("Dynamic", "Transformer");
        GenericIdentifier result = transformer.transform(input);

        assertNotNull(result);
        assertEquals(2, result.getData().length);
        assertEquals("Dynamic", result.getData()[0].getValue());
        assertEquals("Transformer", result.getData()[1].getValue
