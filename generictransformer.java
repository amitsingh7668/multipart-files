import java.util.Map;
import java.util.HashMap;

// Generic transformation interface
public interface Transformer<T> {
    GenericModel transform(T input);
}

// GenericModel with a single attribute - a map
public class GenericModel {
    private Map<String, String> data;

    public GenericModel() {
        this.data = new HashMap<>();
    }

    public Map<String, String> getData() {
        return data;
    }

    public void setData(Map<String, String> data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "GenericModel{" + "data=" + data + '}';
    }
}

// Abstract base class for common transformation logic
public abstract class BaseTransformer<T> implements Transformer<T> {
    protected GenericModel createGenericModel() {
        return new GenericModel();
    }

    protected void addEntry(GenericModel model, String key, String value) {
        model.getData().put(key, value);
    }
}

// Sample concrete implementation for a specific data model
public class SampleDataModelTransformer extends BaseTransformer<SampleDataModel> {
    @Override
    public GenericModel transform(SampleDataModel input) {
        GenericModel result = createGenericModel();
        addEntry(result, "fullName", input.getFirstName() + " " + input.getLastName());
        addEntry(result, "email", input.getEmail());
        return result;
    }
}

// Sample input data model
public class SampleDataModel {
    private String firstName;
    private String lastName;
    private String email;

    public SampleDataModel(String firstName, String lastName, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }
}

// Main class to test the framework
public class TransformationFramework {
    public static void main(String[] args) {
        SampleDataModel input = new SampleDataModel("John", "Doe", "john.doe@example.com");
        Transformer<SampleDataModel> transformer = new SampleDataModelTransformer();
        GenericModel result = transformer.transform(input);
        System.out.println(result);
    }
}
