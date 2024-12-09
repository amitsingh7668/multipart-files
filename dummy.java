private void sendPostRequest(String url, Object gedsRequestEntity) {
    ResponseEntity<String> responseEntity = doWithRetry(() -> restTemplate.postForEntity(url, getEntity(gedsRequestEntity), String.class));
    
    // Check if the response is a successful 2xx status code
    if (responseEntity.getStatusCode().is2xxSuccessful()) {
        String responseBody = responseEntity.getBody();

        // Check for specific message indicating redirection
        if (responseBody != null && responseBody.contains("You will be forwarded to complete the authorization")) {
            // Handle redirection logic here
            String redirectUrl = extractRedirectUrl(responseBody); // A method to parse and extract the redirect URL
            sendPostRequest(redirectUrl, gedsRequestEntity); // Recursively call the method with the new URL
        } else {
            // Proceed normally if no redirection is indicated
            throw new RestClientException(String.format(EXCEPTION_DURING_CALL_TO_GCDS_WITH_DETAILS, responseBody));
        }
    }
}

private <T> T doWithRetry(Supplier<T> operation) {
    for (var retries = 0; retries < MAX_RETRIES; retries++) {
        try {
            return operation.get();
        } catch (Exception e) {
            log.info("Request being retried", e);
        }
    }
    throw new RestClientException(EXCEPTION_DURING_CALL_TO_GCDS);
}

// Helper method to extract redirect URL from the response body
private String extractRedirectUrl(String responseBody) {
    // Example logic for extracting a URL (customize as per your response format)
    Pattern pattern = Pattern.compile("https?://[\\w./-]+");
    Matcher matcher = pattern.matcher(responseBody);
    if (matcher.find()) {
        return matcher.group();
    }
    throw new IllegalArgumentException("Redirect URL not found in response");
}
