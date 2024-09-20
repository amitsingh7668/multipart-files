import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;
import org.json.JSONObject;
import java.util.HashMap;
import java.util.Map;

public class RestTemplateExample {

    public static void main(String[] args) {
        // Create the payload
        Map<String, Object> jsonData = new HashMap<>();
        jsonData.put("host", "Cribl REST test 13");
        jsonData.put("status", "critical");
        jsonData.put("node", "a-test-node.swissbank.com");
        jsonData.put("timestamp", "1402302570");
        jsonData.put("alert_category", "REST integration");
        jsonData.put("alert_subcategory", "REST integration");
        jsonData.put("alert_key", "OIM integration test");
        jsonData.put("description", "Test alert sent for REST integration");
        jsonData.put("identifier", "Cribl REST test");
        jsonData.put("isac_swci", "");
        jsonData.put("isac_swc_name", "Cribl Stream Dev");
        jsonData.put("isac_swc", "");
        jsonData.put("isac_swc_name", "Cribl Stream");
        jsonData.put("software_id", "");
        jsonData.put("message_key", "1234");
        jsonData.put("sys_country", "UK");
        jsonData.put("external_action", "none");

        // Convert map to JSON string
        JSONObject jsonPayload = new JSONObject(jsonData);

        // Set headers
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");

        // Create HttpEntity with the payload and headers
        HttpEntity<String> requestEntity = new HttpEntity<>(jsonPayload.toString(), headers);

        // Destination URL
        String url = "ht";

        // RestTemplate instance
        RestTemplate restTemplate = new RestTemplate();

        try {
            // Send POST request
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    requestEntity,
                    String.class
            );

            // Check the response
            if (response.getStatusCode().is2xxSuccessful()) {
                System.out.println("Success: " + response.getBody());
            } else {
                System.out.println("Failed with status code: " + response.getStatusCode());
            }
        } catch (Exception e) {
            System.out.println("Connection error: " + e.getMessage());
        }
    }
}
