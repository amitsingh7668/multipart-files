import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.util.Base64Utils;
import org.springframework.web.client.RestTemplate;
 
public class RestTemplateBasicAuthExample {
 
    public static void main(String[] args) {
        // Define the username and password
        String username = "your_username";
        String password = "your_password";
 
        // URL of the API you want to call
        String url = "https://api.example.com/your-endpoint";
 
        // Prepare Basic Auth header
        HttpHeaders headers = createBasicAuthHeaders(username, password);
 
        // If you need to send a body with your POST request
        String requestBody = "{\"key\":\"value\"}"; // Example request body (in JSON)
 
        // Create HttpEntity with headers and request body
        HttpEntity<String> requestEntity = new HttpEntity<>(requestBody, headers);
 
        // Create a RestTemplate instance
        RestTemplate restTemplate = new RestTemplate(new HttpComponentsClientHttpRequestFactory());
 
        // Execute the POST request
        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, requestEntity, String.class);
 
        // Check the response
        if (response.getStatusCode() == HttpStatus.OK) {
            System.out.println("Response: " + response.getBody());
        } else {
            System.out.println("Error: " + response.getStatusCode());
        }
    }
 
    // Method to create Basic Auth headers
    private static HttpHeaders createBasicAuthHeaders(String username, String password) {
        HttpHeaders headers = new HttpHeaders();
        String auth = username + ":" + password;
        byte[] encodedAuth = Base64Utils.encode(auth.getBytes());
        String authHeader = "Basic " + new String(encodedAuth);
 
        headers.set("Authorization", authHeader);
        headers.set("Content-Type", "application/json"); // Set content type as per your API requirement
        return headers;
    }
}
