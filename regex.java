import java.util.*;
import java.util.regex.*;

public class StringToMap {
    public static void main(String[] args) {
        String input = "eu:a,b,c,d;ind:a,b,c";

        // Create the Map to store the results
        Map<String, List<String>> map = new HashMap<>();

        // Regex pattern to match key:value pairs (key: list of comma-separated values)
        String regex = "(\\w+):([a-zA-Z,]+)";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(input);

        // Iterate through all the key-value pairs
        while (matcher.find()) {
            String key = matcher.group(1);  // the key (e.g., "eu", "ind")
            String[] values = matcher.group(2).split(",");  // the values as a list (e.g., ["a", "b", "c"])

            // Convert array to list and put it in the map
            map.put(key, Arrays.asList(values));
        }

        // Print the map to check the result
        for (Map.Entry<String, List<String>> entry : map.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }
    }
}
